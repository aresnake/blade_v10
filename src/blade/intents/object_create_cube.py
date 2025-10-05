# -*- coding: utf-8 -*-
"""
Intent: object.create_cube
Entrées:
  - radius: float (taille = 2*radius)
  - collection: str (optionnel) -> nom de la collection à assurer + lier

DoD (Definition of Done):
  - ❌ Pas de bpy.ops -> ✅ Data API uniquement
  - Références explicites (objets/collections)
  - Lien explicite à une collection (ou à la scene collection)
  - Logs: start / ensure / created / linked / ok / fail
  - Aucune dépendance à active/selected
"""

from __future__ import annotations
import bpy
import os
from datetime import datetime
from typing import Dict, Any, Optional


# ---------- Utils: logs ------------------------------------------------------
def _logs_dir() -> str:
    # Repo: D:\blade_v10\logs par convention (runner/CONTRIBUTING)
    # Si le cwd est ailleurs, on tente ./logs relatif.
    base = os.getcwd()
    p = os.path.join(base, "logs")
    try:
        os.makedirs(p, exist_ok=True)
    except Exception:
        pass
    return p


def _log(line: str) -> None:
    try:
        stamp = datetime.now().strftime("%Y-%m-%d")
        logfile = os.path.join(_logs_dir(), f"intent_{stamp}.log")
        with open(logfile, "a", encoding="utf-8") as f:
            f.write(line.rstrip() + "\n")
    except Exception:
        # En dernier recours on imprime
        print(line)


# ---------- Utils: collections ----------------------------------------------
def ensure_collection(col_name: Optional[str]) -> bpy.types.Collection:
    """
    Retourne une collection prête (créée si nécessaire) et
    assurée dans la scène courante.
    """
    if not col_name:
        # Fallback -> Scene Collection (racine)
        return bpy.context.scene.collection

    col = bpy.data.collections.get(col_name)
    if col is None:
        col = bpy.data.collections.new(col_name)

    # S'assurer qu'elle est liée à la Scene (si pas déjà)
    scene = bpy.context.scene
    if col.name not in scene.collection.children.keys():
        scene.collection.children.link(col)

    # Visibilité basique (EEVEE/world reste pour un intent dédié)
    col.hide_viewport = False
    col.hide_render = False
    return col


# ---------- Core: create cube via data API -----------------------------------
def create_cube_object(name: str, radius: float) -> bpy.types.Object:
    """
    Crée un mesh cube centré à l'origine via data API (pas de bpy.ops).
    Taille = 2*radius.
    """
    r = float(radius)
    if r <= 0.0:
        raise ValueError("radius must be > 0")

    # Sommets et faces d'un cube centré
    verts = [
        (-r, -r, -r),
        ( r, -r, -r),
        ( r,  r, -r),
        (-r,  r, -r),
        (-r, -r,  r),
        ( r, -r,  r),
        ( r,  r,  r),
        (-r,  r,  r),
    ]
    faces = [
        (0, 1, 2, 3),  # bas
        (4, 5, 6, 7),  # haut
        (0, 1, 5, 4),  # côté -Y
        (1, 2, 6, 5),  # côté +X
        (2, 3, 7, 6),  # côté +Y
        (3, 0, 4, 7),  # côté -X
    ]

    mesh = bpy.data.meshes.new(f"{name}_mesh")
    mesh.from_pydata(verts, [], faces)
    mesh.update(calc_edges=True)

    obj = bpy.data.objects.new(name, mesh)
    # Ne touche pas active/selected ; on renvoie l'object pour un lien explicite
    return obj


# ---------- Intent runner -----------------------------------------------------
def run(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Exécution de l’intent:
      - crée un cube (radius)
      - le lie à une collection (optionnelle) ou à la scène
    Retour:
      - dict avec infos utiles (nom objet, collection, status, messages)
    """
    t0 = datetime.now().isoformat(timespec="seconds")
    log_prefix = "[intent:object.create_cube]"

    try:
        radius = float(params.get("radius", 1.0))
        col_name = params.get("collection")  # None/str
        _log(f"{log_prefix} start ts={t0} radius={radius} collection={col_name!r}")

        col = ensure_collection(col_name)
        _log(f"{log_prefix} ensure collection='{col.name}' ok")

        obj_name = f"Cube_{int(datetime.now().timestamp())}"
        obj = create_cube_object(obj_name, radius)
        _log(f"{log_prefix} created object='{obj.name}' mesh='{obj.data.name}'")

        # Lier explicitement l’objet à la collection visée
        if obj.name not in col.objects.keys():
            col.objects.link(obj)

        # S’il a été automatiquement linké ailleurs, on ne cherche pas à unlink globalement :
        # on reste non-destructif (FixBook s’occupera des nettoyages si nécessaire).

        _log(f"{log_prefix} linked object='{obj.name}' to collection='{col.name}' ok")

        result = {
            "status": "ok",
            "object": obj.name,
            "collection": col.name,
            "radius": radius,
            "ts": t0,
        }
        _log(f"{log_prefix} ok -> {result}")
        return result

    except Exception as ex:
        msg = f"{log_prefix} FAIL: {repr(ex)}"
        _log(msg)
        return {"status": "fail", "error": str(ex), "ts": t0}
