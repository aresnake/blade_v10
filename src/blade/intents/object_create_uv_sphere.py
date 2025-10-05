"""
Intent: object.create_uv_sphere
Entrées: radius: float, segments?: int, rings?: int, collection?: str
Étapes: mesh data, object, link, logs
DoD: data API only, refs explicites, tests OK+correction
"""
# Blade v10 — intent: object.create_uv_sphere (no-ops, data API)
import bpy
import bmesh
from mathutils import Matrix

def _ensure_collection(name: str):
    coll = bpy.data.collections.get(name)
    if coll is None:
        coll = bpy.data.collections.new(name)
    scene_coll = bpy.context.scene.collection
    if coll.name not in [c.name for c in scene_coll.children]:
        scene_coll.children.link(coll)
    return coll

def _link_object(obj: bpy.types.Object, collection: str | None):
    if collection:
        coll = _ensure_collection(collection)
    else:
        coll = bpy.context.scene.collection
    if obj.name not in [o.name for o in coll.objects]:
        coll.objects.link(obj)
    return coll

def run(radius: float = 0.5, segments: int = 32, rings: int = 16,
        collection: str | None = None, name: str = "BL10_UVSphere"):
    print(f"[Blade v10] object_create_uv_sphere.run start r={radius} seg={segments} rings={rings} collection={collection!r}")

    mesh = bpy.data.meshes.new(name + "_MESH")
    bm = bmesh.new()
    bmesh.ops.create_uvsphere(
        bm,
        u_segments=int(segments),
        v_segments=int(rings),
        radius=float(radius),
    )
    bm.to_mesh(mesh)
    bm.free()

    obj = bpy.data.objects.new(name, mesh)
    linked_coll = _link_object(obj, collection)
    obj.matrix_world = Matrix.Identity(4)

    print(f"[Blade v10] object_create_uv_sphere.run ok obj={obj.name} coll={linked_coll.name}")
    return {"ok": True, "object": obj.name, "collection": linked_coll.name}
