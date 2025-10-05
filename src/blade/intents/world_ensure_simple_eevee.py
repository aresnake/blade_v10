# Blade v10 — intent: world.ensure_simple_eevee

import bpy

def run(ao: bool = True, bloom: bool = True, soft_shadows: bool = True, world_color=(0.02,0.02,0.02,1.0)):
    print(f"[Blade v10] world_ensure_simple_eevee.run start ao={ao} bloom={bloom} soft={soft_shadows}")
    scene = bpy.context.scene
    # EEVEE safe setup
    ee = scene.eevee
    ee.use_gtao = bool(ao)
    ee.use_bloom = bool(bloom)
    ee.use_soft_shadows = bool(soft_shadows)

    # World ensure
    if not scene.world:
        scene.world = bpy.data.worlds.new("BL10_World")
    w = scene.world
    w.use_nodes = False
    w.color = world_color[:3]

    print("[Blade v10] world_ensure_simple_eevee ok")
    return {"ok": True, "eevee": {"ao": ee.use_gtao, "bloom": ee.use_bloom, "soft_shadows": ee.use_soft_shadows}, "world": w.name}
