# Blade v10 — intent: object.create_uv_sphere
# Data-API only via bmesh

import bpy
import bmesh

def _ensure_collection(name: str | None, scene: bpy.types.Scene) -> bpy.types.Collection:
    if not name:
        return scene.collection
    coll = bpy.data.collections.get(name)
    if not coll:
        coll = bpy.data.collections.new(name)
    if coll.name not in scene.collection.children:
        scene.collection.children.link(coll)
    return coll

def run(radius: float = 0.5, segments: int = 32, rings: int = 16,
        collection: str | None = None, name: str = "BL10_UVSphere"):
    print(f"[Blade v10] object_create_uv_sphere.run start r={radius} seg={segments} rings={rings} coll={collection}")
    scene = bpy.context.scene

    mesh = bpy.data.meshes.new(name + "_ME")
    bm = bmesh.new()
    bmesh.ops.create_uvsphere(bm, u_segments=max(8, int(segments)), v_segments=max(4, int(rings)), diameter=radius*2.0)
    bm.to_mesh(mesh)
    bm.free()

    obj = bpy.data.objects.new(name, mesh)
    coll = _ensure_collection(collection, scene)
    if obj.name not in coll.objects:
        coll.objects.link(obj)

    print(f"[Blade v10] object_create_uv_sphere.run ok obj={obj.name} coll={coll.name}")
    return {"ok": True, "object": obj.name, "collection": coll.name}
