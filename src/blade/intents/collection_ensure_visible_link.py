# Blade v10 — intent: collection.ensure_visible_link

import bpy

def _ensure_collection(name: str, scene: bpy.types.Scene) -> bpy.types.Collection:
    coll = bpy.data.collections.get(name)
    if not coll:
        coll = bpy.data.collections.new(name)
    if coll.name not in scene.collection.children:
        scene.collection.children.link(coll)
    coll.hide_viewport = False
    coll.hide_render = False
    return coll

def run(object_name: str, collection_name: str):
    print(f"[Blade v10] collection_ensure_visible_link.run start obj={object_name} coll={collection_name}")
    scene = bpy.context.scene
    obj = bpy.data.objects.get(object_name)
    if not obj:
        return {"ok": False, "error": f"object '{object_name}' not found"}

    coll = _ensure_collection(collection_name, scene)
    if obj.name not in coll.objects:
        coll.objects.link(obj)

    print(f"[Blade v10] collection_ensure_visible_link ok obj={obj.name} coll={coll.name}")
    return {"ok": True, "object": obj.name, "collection": coll.name}
