# v11 — Sélection des 10 intents (robustes, data-API, no-ops)

1) object.create_cube(radius)
2) object.create_uv_sphere(radius)
3) object.create_plane(size)
4) material.ensure_and_assign(object, material_name, base_color)
5) modifier.add_subsurf(object, levels)
6) camera.ensure_and_frame(target, distance, height, track_to=TRACK_NEGATIVE_Z/UP_Y)
7) light.ensure_sun(strength, angle_deg) + light.ensure_area(fill_strength)
8) world.ensure_simple_eevee(AO, Bloom, SoftShadows)  # safe_set props
9) scene.render_background_mp4(output_path, fps, duration)
10) collection.ensure_visible_and_link(object, collection_name)

## Principes
- **API Data only** (éviter bpy.ops; si usage, récupérer la ref direct et ne plus dépendre d’active/selected)
- **No-ops robuste** par défaut ; link via `scene.collection.objects.link`
- **Materials** via helpers ensure_material()/assign_material()
- **TrackTo strict**: TRACK_NEGATIVE_Z, UP_Y
- **EEVEE only** (jamais EEVEE_NEXT), safe_set pour props instables
