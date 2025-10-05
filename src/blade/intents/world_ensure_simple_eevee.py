# -*- coding: utf-8 -*-
"""
Intent: world.ensure_simple_eevee
Active EEVEE + AO/Bloom/SoftShadows, crée World si absent.
"""
import bpy

def _log(msg): print(f"[Blade v10] world_ensure_simple_eevee: {msg}")

def run(ambient_occlusion: bool = True,
        bloom: bool = True,
        soft_shadows: bool = True):
    sc = bpy.context.scene

    if sc.world is None:
        sc.world = bpy.data.worlds.new("World")

    # EEVEE Next si possible, sinon EEVEE
    try:
        sc.render.engine = "BLENDER_EEVEE_NEXT"
    except Exception:
        sc.render.engine = "BLENDER_EEVEE"

    ee = sc.eevee
    ee.use_gtao = bool(ambient_occlusion)
    ee.use_bloom = bool(bloom)
    ee.use_soft_shadows = bool(soft_shadows)

    _log(f"ok AO={ee.use_gtao} Bloom={ee.use_bloom} Soft={ee.use_soft_shadows}")
    return {"ok": True, "engine": sc.render.engine, "AO": ee.use_gtao,
            "Bloom": ee.use_bloom, "SoftShadows": ee.use_soft_shadows}
