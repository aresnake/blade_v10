# src/blade/intents/scene_clear_startup_defaults.py
import bpy

def _log(msg): print(f"[Blade v10] scene_clear_startup_defaults: {msg}")

def run(names=("Cube", "Light", "Camera")):
    """
    Remove Blender's default startup objects if present.
    - No selection / context ops.
    - Safe no-op if objects are already gone or renamed.
    """
    sc = bpy.context.scene
    removed = []
    for name in names:
        obj = bpy.data.objects.get(name)
        if obj:
            # unlink from all collections first (data API)
            for coll in list(obj.users_collection):
                coll.objects.unlink(obj)
            bpy.data.objects.remove(obj, do_unlink=True)
            removed.append(name)
    _log(f"removed={removed or 'none'}")
    return {"ok": True, "removed": removed}
