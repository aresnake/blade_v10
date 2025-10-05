# Blade v10 — intent: object.create_plane (no-ops, data API)
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

def run(size: float = 2.0, collection: str | None = None, name: str = "BL10_Plane"):
    print(f"[Blade v10] object_create_plane.run start size={size} collection={collection!r}")

    mesh = bpy.data.meshes.new(name + "_MESH")
    bm = bmesh.new()
    half = float(size) / 2.0
    # 4 sommets + 1 face
    v1 = bm.verts.new((-half, -half, 0.0))
    v2 = bm.verts.new(( half, -half, 0.0))
    v3 = bm.verts.new(( half,  half, 0.0))
    v4 = bm.verts.new((-half,  half, 0.0))
    bm.faces.new((v1, v2, v3, v4))
    bm.normal_update()
    bm.to_mesh(mesh)
    bm.free()

    obj = bpy.data.objects.new(name, mesh)
    linked_coll = _link_object(obj, collection)
    obj.matrix_world = Matrix.Identity(4)

    print(f"[Blade v10] object_create_plane.run ok obj={obj.name} coll={linked_coll.name}")
    return {"ok": True, "object": obj.name, "collection": linked_coll.name}
