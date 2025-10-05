bl_info = {
    "name": "Blade v10 UI",
    "author": "Adrien / ARES",
    "version": (0, 2, 1),
    "blender": (4, 5, 0),
    "location": "3D View > N-Panel > Blade v10",
    "category": "3D View",
    "description": "UI minimaliste pour piloter les intents Blade v10",
}

import bpy
import importlib
import os
import sys

# ---------- util ----------
def _safe_call(fn, **kwargs):
    try:
        ret = fn(**kwargs)
        print("[Blade v10 UI] OK:", ret)
        return {"FINISHED"}
    except Exception as e:
        print("[Blade v10 UI] ERROR:", e)
        import traceback; traceback.print_exc()
        return {"CANCELLED"}

def _ensure_src_on_path():
    # 1) BLADE_SRC si défini ; 2) fallback dev path (adapter au besoin)
    candidates = []
    env = os.environ.get("BLADE_SRC")
    if env:
        candidates.append(env)
    candidates.append(r"D:\blade_v10\src")
    for p in candidates:
        if p and os.path.isdir(p) and p not in sys.path:
            sys.path.insert(0, p)
            print("[Blade v10 UI] blade import OK from:", p)
            break

# ---------- operators ----------
class BLADEV10_OT_clear_defaults(bpy.types.Operator):
    bl_idname = "blade_v10.clear_defaults"
    bl_label  = "Clear Startup Defaults"
    bl_description = "Remove default Cube/Light/Camera safely"
    def execute(self, _ctx):
        mod = importlib.import_module("blade.intents.scene_clear_startup_defaults")
        return _safe_call(mod.run)

class BLADEV10_OT_create_cube(bpy.types.Operator):
    bl_idname = "blade_v10.create_cube"
    bl_label  = "Create Cube"
    radius: bpy.props.FloatProperty(name="Radius", default=1.0, min=0.0)
    collection: bpy.props.StringProperty(name="Collection", default="")
    def execute(self, _):
        mod = importlib.import_module("blade.intents.object_create_cube")
        return _safe_call(mod.run, radius=self.radius, collection=(self.collection or None), name="BL10_Cube")

class BLADEV10_OT_assign_mat(bpy.types.Operator):
    bl_idname = "blade_v10.assign_mat"
    bl_label  = "Assign Material"
    object_name: bpy.props.StringProperty(name="Object", default="BL10_Cube")
    material_name: bpy.props.StringProperty(name="Material", default="BL10_Mat")
    base_r: bpy.props.FloatProperty(name="R", default=0.8, min=0, max=1)
    base_g: bpy.props.FloatProperty(name="G", default=0.2, min=0, max=1)
    base_b: bpy.props.FloatProperty(name="B", default=0.2, min=0, max=1)
    collection: bpy.props.StringProperty(name="Collection", default="")
    def execute(self, _):
        mod = importlib.import_module("blade.intents.material_ensure_assign")
        return _safe_call(mod.run,
            object_name=self.object_name,
            material_name=self.material_name,
            base_color=(self.base_r, self.base_g, self.base_b, 1.0),
            collection=(self.collection or None)
        )

class BLADEV10_OT_add_subsurf(bpy.types.Operator):
    bl_idname = "blade_v10.add_subsurf"
    bl_label  = "Add Subsurf"
    object_name: bpy.props.StringProperty(name="Object", default="BL10_Cube")
    levels: bpy.props.IntProperty(name="Levels", default=2, min=0, max=6)
    render_levels: bpy.props.IntProperty(name="Render Levels", default=2, min=0, max=6)
    use_simple: bpy.props.BoolProperty(name="Simple", default=False)
    def execute(self, _):
        mod = importlib.import_module("blade.intents.modifier_add_subsurf")
        return _safe_call(mod.run,
            object_name=self.object_name,
            levels=self.levels,
            render_levels=self.render_levels,
            use_simple=self.use_simple
        )

class BLADEV10_OT_link_to_collection(bpy.types.Operator):
    bl_idname = "blade_v10.link_to_collection"
    bl_label  = "Link To Collection"
    object_name: bpy.props.StringProperty(name="Object", default="BL10_Cube")
    collection_name: bpy.props.StringProperty(name="Collection", default="ENV_Objects")
    def execute(self, _):
        mod = importlib.import_module("blade.intents.collection_ensure_visible_link")
        return _safe_call(mod.run, object_name=self.object_name, collection_name=self.collection_name)

class BLADEV10_OT_camera_frame(bpy.types.Operator):
    bl_idname = "blade_v10.camera_frame"
    bl_label  = "Frame Camera"
    target: bpy.props.StringProperty(name="Target", default="BL10_Cube")
    distance: bpy.props.FloatProperty(name="Distance", default=6.0)
    height: bpy.props.FloatProperty(name="Height", default=3.0)
    def execute(self, _):
        mod = importlib.import_module("blade.intents.camera_ensure_frame")
        return _safe_call(mod.run, target_name=self.target, distance=self.distance, height=self.height)

class BLADEV10_OT_lights_setup(bpy.types.Operator):
    bl_idname = "blade_v10.lights_setup"
    bl_label  = "Ensure Sun+Area"
    def execute(self, _):
        mod = importlib.import_module("blade.intents.light_ensure_sun_area")
        return _safe_call(mod.run)

class BLADEV10_OT_world_simple(bpy.types.Operator):
    bl_idname = "blade_v10.world_simple"
    bl_label  = "EEVEE Simple"
    ao: bpy.props.BoolProperty(default=True); bloom: bpy.props.BoolProperty(default=True); soft: bpy.props.BoolProperty(default=True)
    def execute(self, _):
        mod = importlib.import_module("blade.intents.world_ensure_simple_eevee")
        return _safe_call(mod.run, ambient_occlusion=self.ao, bloom=self.bloom, soft_shadows=self.soft)

class BLADEV10_OT_render_cfg(bpy.types.Operator):
    bl_idname = "blade_v10.render_cfg"
    bl_label  = "Configure MP4"
    def execute(self, _):
        mod = importlib.import_module("blade.intents.scene_render_background_mp4")
        return _safe_call(mod.run, do_render=False)

# ---------- panel ----------
class BLADEV10_PT_panel(bpy.types.Panel):
    bl_label = "Blade v10"
    bl_idname = "BLADEV10_PT_panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Blade v10"
    def draw(self, _ctx):
        layout = self.layout

        box = layout.box(); box.label(text="Scene", icon="SCENE_DATA")
        box.operator("blade_v10.clear_defaults", text="Clear Cube/Light/Camera")

        box = layout.box(); box.label(text="Objects", icon="OUTLINER_OB_MESH")
        box.operator("blade_v10.create_cube", text="Create Cube")

        box = layout.box(); box.label(text="Materials", icon="MATERIAL")
        box.operator("blade_v10.assign_mat", text="Assign Material")

        box = layout.box(); box.label(text="Modifiers", icon="MOD_SUBSURF")
        box.operator("blade_v10.add_subsurf", text="Add Subsurf")

        box = layout.box(); box.label(text="Collections", icon="OUTLINER_COLLECTION")
        box.operator("blade_v10.link_to_collection", text="Link To Collection")

        box = layout.box(); box.label(text="Camera", icon="CAMERA_DATA")
        box.operator("blade_v10.camera_frame", text="Frame Camera")

        box = layout.box(); box.label(text="Lights", icon="LIGHT")
        box.operator("blade_v10.lights_setup", text="Ensure Sun + Area")

        box = layout.box(); box.label(text="World", icon="WORLD_DATA")
        box.operator("blade_v10.world_simple", text="EEVEE Simple")

        box = layout.box(); box.label(text="Render", icon="RENDER_ANIMATION")
        box.operator("blade_v10.render_cfg", text="Config MP4")

# ---------- register ----------
classes = (
    BLADEV10_OT_clear_defaults,
    BLADEV10_OT_create_cube,
    BLADEV10_OT_assign_mat,
    BLADEV10_OT_add_subsurf,
    BLADEV10_OT_link_to_collection,
    BLADEV10_OT_camera_frame,
    BLADEV10_OT_lights_setup,
    BLADEV10_OT_world_simple,
    BLADEV10_OT_render_cfg,
    BLADEV10_PT_panel,
)

def register():
    _ensure_src_on_path()
    for c in classes:
        bpy.utils.register_class(c)
    print("[Blade v10 UI] registered")

def unregister():
    for c in reversed(classes):
        try: bpy.utils.unregister_class(c)
        except: pass
    print("[Blade v10 UI] unregistered")
