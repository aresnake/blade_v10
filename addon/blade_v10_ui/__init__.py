bl_info = {
    "name": "Blade v10 UI",
    "author": "Adrien / ARES",
    "version": (0, 1, 0),
    "blender": (4, 5, 0),
    "location": "N-Panel > Blade v10",
    "category": "3D View",
}

import bpy
import importlib

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
        # Import *à l'exécution* pour éviter erreurs si src pas dans sys.path
        mod = importlib.import_module("blade.intents.object_create_cube")
        # Signature attendue: run(radius: float=1.0, collection: Optional[str]=None, name='Cube')
        return _safe_call(mod.run, radius=self.radius,
                          collection=(self.collection or None),
                          name="BL10_Cube")

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
        box.operator("blade_v10.create_cube", text="Create Cube")
        box.separator()
        box2 = layout.box()
        box2.label(text="Soon", icon="TOOL_SETTINGS")
        col = box2.column()
        col.enabled = False
        col.operator("wm.call_menu", text="Create Plane (WIP)")
        col.operator("wm.call_menu", text="Create UV Sphere (WIP)")

classes = (BLADEV10_OT_create_cube, BLADEV10_PT_panel)

def register():
    for c in classes:
        bpy.utils.register_class(c)
    print("[Blade v10 UI] registered")

def unregister():
    for c in reversed(classes):
        try: bpy.utils.unregister_class(c)
        except: pass
    print("[Blade v10 UI] unregistered")
