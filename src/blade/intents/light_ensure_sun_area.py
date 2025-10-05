# -*- coding: utf-8 -*-
"""
Intent: light.ensure_sun_area
Crée/paramètre un SUN + une AREA dans une collection dédiée.
"""
import bpy
import math

def _log(msg): print(f"[Blade v10] light_ensure_sun_area: {msg}")

def _ensure_collection(name: str):
    col = bpy.data.collections.get(name) or bpy.data.collections.new(name)
    sc = bpy.context.scene
    if col.name not in sc.collection.children:
        sc.collection.children.link(col)
    return col

def _ensure_light(name: str, kind: str, collection):
    obj = bpy.data.objects.get(name)
    if not obj:
        data = bpy.data.lights.new(name=name, type=kind)
        obj = bpy.data.objects.new(name, data)
        collection.objects.link(obj)
    return obj

def run(sun_strength: float = 3.0,
        sun_angle_deg: float = 35.0,
        area_strength: float = 1000.0,
        area_size: float = 4.0,
        collection_name: str = "ENV_Lights"):
    _log(f"start sun={sun_strength}@{sun_angle_deg}deg area={area_strength}")

    col = _ensure_collection(collection_name)

    sun = _ensure_light("BL10_Sun", "SUN", col)
    sun.data.energy = max(0.0, float(sun_strength))
    sun.data.angle = math.radians(max(0.0, float(sun_angle_deg)))
    sun.location = (6.0, -6.0, 6.0)

    area = _ensure_light("BL10_Area", "AREA", col)
    area.data.energy = max(0.0, float(area_strength))
    area.data.shape = 'SQUARE'
    area.data.size = max(0.01, float(area_size))
    area.location = (-4.0, 4.0, 3.0)

    _log("ok")
    return {"ok": True, "sun": sun.name, "area": area.name, "collection": col.name}
