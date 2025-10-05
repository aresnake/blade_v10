# Blade v10 — intent: camera.ensure_frame
# Create or reuse a camera, place at distance/height from target, add Track To.

import bpy
from mathutils import Vector

def _bbox_center(obj: bpy.types.Object) -> Vector:
    m = obj.matrix_world
    pts = [m @ Vector(corner) for corner in obj.bound_box]
    return sum(pts, Vector()) / 8.0

def _ensure_camera(name="BL10_Camera") -> bpy.types.Object:
    cam = bpy.data.objects.get(name)
    if cam and cam.type == 'CAMERA':
        return cam
    cam_data = bpy.data.cameras.new(name + "_DATA")
    cam = bpy.data.objects.new(name, cam_data)
    bpy.context.scene.collection.objects.link(cam)
    return cam

def run(target_name: str, distance: float = 5.0, height: float = 2.0):
    print(f"[Blade v10] camera_ensure_frame.run start target={target_name} dist={distance} h={height}")
    scene = bpy.context.scene
    tgt = bpy.data.objects.get(target_name)
    if not tgt:
        return {"ok": False, "error": f"target '{target_name}' not found"}

    cam = _ensure_camera()
    center = _bbox_center(tgt)

    # Place camera on -Y axis relative to target, at given distance/height
    cam.location = center + Vector((0.0, -abs(distance), abs(height)))

    # Track To constraint (strict)
    c = next((c for c in cam.constraints if c.type == 'TRACK_TO' and c.name == "BL10_TrackTo"), None)
    if not c:
        c = cam.constraints.new(type='TRACK_TO')
        c.name = "BL10_TrackTo"
    c.target = tgt
    c.track_axis = 'TRACK_NEGATIVE_Z'
    c.up_axis = 'UP_Y'

    scene.camera = cam
    print(f"[Blade v10] camera_ensure_frame ok cam={cam.name} -> {tgt.name}")
    return {"ok": True, "camera": cam.name, "target": tgt.name}
