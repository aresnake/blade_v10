# -*- coding: utf-8 -*-
"""
Intent: scene.render_background_mp4
Configure un rendu MP4 (H.264) sans lancer l'anim par défaut.
"""
import bpy
import os
from math import floor

def _log(msg): print(f"[Blade v10] scene_render_background_mp4: {msg}")

def _rgb3(col):
    # Accepte 3 ou 4 composantes, renvoie toujours 3 (RGB)
    if col is None: return (0.0, 0.0, 0.0)
    try:
        return (float(col[0]), float(col[1]), float(col[2]))
    except Exception:
        return (0.0, 0.0, 0.0)

def run(output_path: str = "",
        fps: int = 30,
        duration_sec: float = 2.0,
        background_color=(0.0, 0.0, 0.0, 1.0),
        do_render: bool = False):
    sc = bpy.context.scene

    if not output_path:
        base = os.path.join(os.path.expanduser("~"), "Videos")
        os.makedirs(base, exist_ok=True)
        output_path = os.path.join(base, "blade_v10_bg.mp4")

    fps = max(1, int(fps))
    sc.render.fps = fps
    sc.frame_start = 1
    sc.frame_end = max(1, floor(fps * max(0.01, float(duration_sec))))

    # EEVEE Next si possible, sinon EEVEE
    try:
        sc.render.engine = "BLENDER_EEVEE_NEXT"
    except Exception:
        sc.render.engine = "BLENDER_EEVEE"

    sc.render.image_settings.file_format = 'FFMPEG'
    sc.render.ffmpeg.format = 'MPEG4'
    sc.render.ffmpeg.codec = 'H264'
    sc.render.ffmpeg.constant_rate_factor = 'MEDIUM'
    sc.render.ffmpeg.audio_codec = 'AAC'
    sc.render.ffmpeg.video_bitrate = 6000
    sc.render.ffmpeg.minrate = 0
    sc.render.ffmpeg.maxrate = 9000
    sc.render.ffmpeg.buffersize = 224 * 8

    if sc.world is None:
        sc.world = bpy.data.worlds.new("World")
    sc.world.color = _rgb3(background_color)  # ⚠️ 3 floats, pas 4

    sc.render.filepath = output_path

    _log(f"configured {output_path} {fps}fps {sc.frame_end} frames (render={do_render})")
    if do_render:
        bpy.ops.render.render(animation=True)

    return {"ok": True, "filepath": output_path, "fps": fps, "frames": sc.frame_end}
