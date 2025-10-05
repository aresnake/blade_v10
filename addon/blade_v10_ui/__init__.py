bl_info = {
    "name": "Blade v10 UI",
    "author": "Adrien / ARES",
    "version": (0, 2, 0),
    "blender": (4, 5, 0),
    "location": "N-Panel > Blade v10",
    "category": "3D View",
}

import bpy, importlib, os, sys

def _bootstrap_src():
    # 1) ENV
    p = os.environ.get("BLADE_SRC")
    if p and p not in sys.path and os.path.isdir(p):
        sys.path.insert(0, p); return p
    # 2) Fallback repo path used in this project
    p = r"D:\blade_v10\src"
    if p not in sys.path and os.path.isdir(p):
        sys.path.insert(0, p); return p
    return None

_SRC = _bootstrap_src()
if _SRC:
    print(f"[Blade v10 UI] blade import OK from: {_SRC}")

def _safe_call(fn, **kwargs):
    try:
        ret = fn(**kwargs)
        print("[Blade v10 UI] OK:", ret)
        return {'FINISHED'}
    except Exception as e:
        print("[Blade v10 UI] ERROR:", e)
        import traceback; traceback.print_exc()
        return {'CANCELLED'}

class BLADEV10_OT_create_cube(bpy.types.Operator):
    bl_idname = "blade_v10.create_cube"
    bl_label  = "Create Cube"
    radius: bpy.props.FloatProperty(name="Radius", default=1.0)
    collection: bpy.props.StringProperty(name="Collection", default="")
    def execute(self, context):
        mod = importlib.import_module("blade.intents.object_create_cube")
        return _safe_call(mod.run, radius=self.radius, collection=(self.collection or None), name="BL10_Cube")

class BLADEV10_OT_create_plane(bpy.types.Operator):
    bl_idname = "blade_v10.create_plane"
    bl_label  = "Create Plane"
    size: bpy.props.FloatProperty(name="Size", default=2.0)
    collection: bpy.props.StringProperty(name="Collection", default="")
    def execute(self, context):
        mod = importlib.import_module("blade.intents.object_create_plane")
        return _safe_call(mod.run, size=self.size, collection=(self.collection or None), name="BL10_Plane")

class BLADEV10_OT_create_uvsphere(bpy.types.Operator):
    bl_idname = "blade_v10.create_uvsphere"
    bl_label  = "Create UV Sphere"
    radius: bpy.props.FloatProperty(name="Radius", default=0.5)
    segments: bpy.props.IntProperty(name="Segments", default=32, min=8)
    rings: bpy.props.IntProperty(name="Rings", default=16, min=4)
    collection: bpy.props.StringProperty(name="Collection", default="")
    def execute(self, context):
        mod = importlib.import_module("blade.intents.object_create_uv_sphere")
        return _safe_call(mod.run, radius=self.radius, segments=self.segments, rings=self.rings,
                          collection=(self.collection or None), name="BL10_UVSphere")

class BLADEV10_PT_panel(bpy.types.Panel):
    bl_label = "Blade v10"
    bl_idname = "BLADEV10_PT_panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Blade v10"

    def draw(self, context):
        layout = self.layout

        box = layout.box()
        box.label(text="Objects", icon="OUTLINER_OB_MESH")
        row = box.row(align=True)
        row.operator("blade_v10.create_cube", text="Cube")
        row.operator("blade_v10.create_plane", text="Plane")
        row.operator("blade_v10.create_uvsphere", text="UV Sphere")

        # (Les autres intents pourront être ajoutés ici après test)

classes = (
    BLADEV10_OT_create_cube,
    BLADEV10_OT_create_plane,
    BLADEV10_OT_create_uvsphere,
    BLADEV10_PT_panel,
)

def register():
    for c in classes:
        bpy.utils.register_class(c)
    print("[Blade v10 UI] registered")

def unregister():
    for c in reversed(classes):
        try: bpy.utils.unregister_class(c)
        except: pass
    print("[Blade v10 UI] unregistered")
