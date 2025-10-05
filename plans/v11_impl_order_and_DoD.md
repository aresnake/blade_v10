# v11 — Ordre d’implémentation + Definition of Done

## Ordre
1) object_create_cube.py
2) object_create_plane.py
3) object_create_uv_sphere.py
4) material_ensure_assign.py
5) modifier_add_subsurf.py
6) collection_ensure_visible_link.py
7) camera_ensure_frame.py
8) light_ensure_sun_area.py
9) world_ensure_simple_eevee.py
10) scene_render_background_mp4.py

## DoD (commun)
- API data (no-ops), pas d’usage d’active/selected après ops
- Réfs explicites, liens à la scène/collection garantis
- FixBook: corrections appliquées (EEVEE, TrackTo, ensure material output, safe_set)
- Logs: start/ok/fail + corrections
- 1 test OK + 1 test avec correction (via runner YAML)
