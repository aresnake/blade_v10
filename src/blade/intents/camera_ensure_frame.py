# -*- coding: utf-8 -*-
"""
Intent: camera.ensure_frame
Data API only, pas d'active/selected.
"""
import bpy
from mathutils import Vector

def _log(msg): print(f"[Blade v10] camera_ensure_frame: {msg}")

def _ensure_collection(name: str):
    col = bpy.data.collections.get(name) or bpy.data.collections.new(name)
    scn = bpy.context.scene
    if col.name not in scn.collection.children:
        scn.collection.children.link(col)
    return col

def run(target_name: str = "BL10_Cube",
        distance: float = 6.0,
        height: float = 3.0,
        name: str = "BL10_Camera",
        collection_name: str = "ENV_Cameras"):
    _log(f"start target={target_name} dist={distance} height={height}")

    scene = bpy.context.scene
    tgt = bpy.data.objects.get(target_name)
    if not tgt:
        raise ValueError(f"target object not found: {target_name}")

    cam = bpy.data.objects.get(name)
    if not cam:
        cam_data = bpy.data.cameras.new(name)
        cam = bpy.data.objects.new(name, cam_data)
        _ensure_collection(collection_name).objects.link(cam)

    cam.location = tgt.location + Vector((0.0, -abs(distance), abs(height)))

    tr = next((c for c in cam.constraints if c.type == 'TRACK_TO'), None)
    if not tr:
        tr = cam.constraints.new(type='TRACK_TO')
    tr.target = tgt
    tr.track_axis = 'TRACK_NEGATIVE_Z'
    tr.up_axis = 'UP_Y'

    if scene.camera != cam:
        scene.camera = cam

    _log(f"ok camera={cam.name} -> target={tgt.name}")
    return {"ok": True, "camera": cam.name, "target": tgt.name}
