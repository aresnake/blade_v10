# v11 — FixBook Core (10 règles)

1) Engine: forcer BLENDER_EEVEE si possible (sinon fallback stable).
2) Post-ops: **jamais** dépendre de active_object/selected ; récupérer la ref ou API Data.
3) Materials: ensure_material(name) + assign_material(object, mat) ; éviter références supprimées.
4) Nodes: ne jamais réassigner scene.node_tree ; scene.use_nodes = True puis modifier l’existant.
5) Liens Nodes: Output → Input uniquement (garde-fou).
6) Track To: axes stricts (TRACK_NEGATIVE_Z, UP_Y).
7) World EEVEE: AO/Bloom/Soft Shadows via safe_set(obj, prop, val).
8) Collections: always link et ensure visible (pas d’objets orphelins).
9) Export/Render: chemins sûrs, extensions valides, fps/duration bornés.
10) Helpers safe_set(): ignorer silencieusement props absentes ; logs des correctifs appliqués.

## Hooks
- preflight(intent) → vérifie/construit contexte minimal
- postflight(intent) → log des corrections et des refs créées
