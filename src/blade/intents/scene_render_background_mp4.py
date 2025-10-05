# Blade v10 — intent: scene.render_background_mp4
# Set EEVEE-safe render settings and MP4 output. (No auto-render here.)

import bpy
import os

def run(output_path: str, fps: int = 24, duration_sec: float = 3.0, resolution_x: int = 1920, resolution_y: int = 1080):
    print(f"[Blade v10] scene_render_background_mp4.run start out={output_path} fps={fps} dur={duration_sec}s")
    scene = bpy.context.scene

    # Frame range from fps/duration
    fps = max(1, int(fps))
    total_frames = max(1, int(round(duration_sec * fps)))
    scene.render.fps = fps
    scene.frame_start = 1
    scene.frame_end = total_frames

    # Resolution
    scene.render.resolution_x = int(resolution_x)
    scene.render.resolution_y = int(resolution_y)
    scene.render.resolution_percentage = 100

    # EEVEE (safe bits)
    scene.render.engine = 'BLENDER_EEVEE'
    ee = scene.eevee
    ee.use_gtao = True
    ee.use_bloom = True
    ee.use_soft_shadows = True

    # Output format MP4 (H.264/AAC)
    r = scene.render
    r.filepath = os.path.normpath(output_path)
    r.image_settings.file_format = 'FFMPEG'
    r.ffmpeg.format = 'MPEG4'
    r.ffmpeg.codec = 'H264'
    r.ffmpeg.constant_rate_factor = 'MEDIUM'
    r.ffmpeg.audio_codec = 'AAC'

    print(f"[Blade v10] scene_render_background_mp4 ok frames=1..{total_frames} -> {r.filepath}")
    return {"ok": True, "frames": [scene.frame_start, scene.frame_end], "output": r.filepath}
