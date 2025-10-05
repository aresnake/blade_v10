# Blade v10 — intent: light.ensure_sun_area

import bpy

def _ensure_light(name: str, kind: str) -> bpy.types.Object:
    obj = bpy.data.objects.get(name)
    if obj and obj.type == 'LIGHT' and obj.data.type == kind:
        return obj
    light_data = bpy.data.lights.new(name=name + "_DATA", type=kind)
    obj = bpy.data.objects.new(name, light_data)
    bpy.context.scene.collection.objects.link(obj)
    return obj

def run(sun_strength: float = 3.0, sun_angle_deg: float = 2.0, area_strength: float = 500.0, area_size: float = 4.0):
    print(f"[Blade v10] light_ensure_sun_area.run start sun={sun_strength}@{sun_angle_deg}deg area={area_strength}")
    scene = bpy.context.scene

    sun = _ensure_light("BL10_Sun", "SUN")
    sun.data.energy = max(0.0, float(sun_strength))
    sun.data.angle = max(0.0, float(sun_angle_deg)) * 3.14159265/180.0

    area = _ensure_light("BL10_Area", "AREA")
    area.data.energy = max(0.0, float(area_strength))
    area.data.size = max(0.01, float(area_size))
    area.location = (5.0, -5.0, 5.0)

    print("[Blade v10] light_ensure_sun_area ok")
    return {"ok": True, "sun": sun.name, "area": area.name}
