# -*- coding: utf-8 -*-
"""
Intent: world.ensure_simple_eevee
Active EEVEE/EEVEE Next et règle AO/Bloom/SoftShadows si dispo.
Data API only, no active/selected.
"""
import bpy

def _log(msg): print(f"[Blade v10] world_ensure_simple_eevee: {msg}")

def _set_flag(obj, names, value):
    """Essaie plusieurs noms d'attribut selon versions Blender."""
    for n in names:
        if hasattr(obj, n):
            setattr(obj, n, bool(value))
            return n
    return None

def run(ambient_occlusion: bool = True,
        bloom: bool = True,
        soft_shadows: bool = True):
    sc = bpy.context.scene

    if sc.world is None:
        sc.world = bpy.data.worlds.new("World")

    # EEVEE Next si possible, sinon EEVEE 'classique'
    try:
        sc.render.engine = "BLENDER_EEVEE_NEXT"
    except Exception:
        sc.render.engine = "BLENDER_EEVEE"

    ee = sc.eevee

    # AO: selon versions -> use_gtao ou use_ambient_occlusion
    ao_attr = _set_flag(ee, ("use_gtao", "use_ambient_occlusion"), ambient_occlusion)
    # Bloom: certaines builds n'ont pas use_bloom
    bloom_attr = _set_flag(ee, ("use_bloom",), bloom)
    # Soft shadows: garde-fou idem
    soft_attr = _set_flag(ee, ("use_soft_shadows",), soft_shadows)

    _log(f"ok engine={sc.render.engine} AO={ao_attr} Bloom={bloom_attr} Soft={soft_attr}")
    return {
        "ok": True,
        "engine": sc.render.engine,
        "AO_attr": ao_attr,
        "Bloom_attr": bloom_attr,
        "Soft_attr": soft_attr,
    }
