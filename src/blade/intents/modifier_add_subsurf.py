# Blade v10 — intent: modifier.add_subsurf

import bpy

def run(object_name: str, levels: int = 2, render_levels: int | None = None):
    print(f"[Blade v10] modifier_add_subsurf.run start obj={object_name} levels={levels}")
    obj = bpy.data.objects.get(object_name)
    if not obj:
        return {"ok": False, "error": f"object '{object_name}' not found"}

    mod = obj.modifiers.get("BL10_Subsurf")
    if not mod:
        mod = obj.modifiers.new("BL10_Subsurf", type='SUBSURF')
    mod.levels = max(0, int(levels))
    mod.render_levels = max(0, int(render_levels if render_levels is not None else levels))

    print(f"[Blade v10] modifier_add_subsurf ok obj={obj.name} levels={mod.levels}/{mod.render_levels}")
    return {"ok": True, "object": obj.name, "levels": mod.levels, "render_levels": mod.render_levels}
