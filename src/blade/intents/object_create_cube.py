# Blade v10 — intent: object.create_cube (no-ops, data API)
import bpy
import bmesh
from mathutils import Matrix

def _ensure_collection(name: str):
    coll = bpy.data.collections.get(name)
    if coll is None:
        coll = bpy.data.collections.new(name)
    # s’assurer qu’elle est liée à la scène
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

def run(radius: float = 1.0, collection: str | None = None, name: str = "BL10_Cube"):
    print(f"[Blade v10] object_create_cube.run start radius={radius} collection={collection!r}")

    # Mesh par data API (BMesh)
    mesh = bpy.data.meshes.new(name + "_MESH")
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=2.0 * float(radius))
    bm.to_mesh(mesh)
    bm.free()

    # Objet + lien explicite
    obj = bpy.data.objects.new(name, mesh)
    linked_coll = _link_object(obj, collection)

    # Pose neutre
    obj.matrix_world = Matrix.Identity(4)

    print(f"[Blade v10] object_create_cube.run ok obj={obj.name} coll={linked_coll.name}")
    return {"ok": True, "object": obj.name, "collection": linked_coll.name}
