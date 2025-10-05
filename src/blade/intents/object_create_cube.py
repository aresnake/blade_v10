"""
Intent: object.create_cube
Entrées: radius: float, collection?: str
Étapes:
  - create Mesh (cube) via data API
  - create Object, link to scene or ensured collection
  - logs: start/ensure/created/linked/ok ; catch fail
DoD:
  - no-ops, no active/selected
  - refs explicites
  - tests: OK + correction (collection)
"""
