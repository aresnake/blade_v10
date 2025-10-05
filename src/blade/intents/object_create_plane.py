# Blade v10 — intent: object.create_plane
# Data-API only, no active/selected

import bpy
import bmesh
from mathutils import Matrix

def _ensure_collection(name: str | None, scene: bpy.types.Scene) -> bpy.types.Collection:
    if not name:
        return scene.collection
    coll = bpy.data.collections.get(name)
    if not coll:
        coll = bpy.data.collections.new(name)
    if coll.name not in scene.collection.children:
        scene.collection.children.link(coll)
    return coll

def run(size: float = 2.0, collection: str | None = None, name: str = "BL10_Plane"):
    print(f"[Blade v10] object_create_plane.run start size={size} collection={collection}")
    scene = bpy.context.scene

    mesh = bpy.data.meshes.new(name + "_ME")
    bm = bmesh.new()
    bmesh.ops.create_grid(bm, x_segments=1, y_segments=1, size=size*0.5, matrix=Matrix.Identity(4))
    bm.to_mesh(mesh)
    bm.free()

    obj = bpy.data.objects.new(name, mesh)
    coll = _ensure_collection(collection, scene)
    if obj.name not in coll.objects:
        coll.objects.link(obj)

    print(f"[Blade v10] object_create_plane.run ok obj={obj.name} coll={coll.name}")
    return {"ok": True, "object": obj.name, "collection": coll.name}
