# Blade v10 — intent: material.ensure_assign

import bpy

def _ensure_material(name: str, base_color=(0.8,0.8,0.8,1.0)) -> bpy.types.Material:
    mat = bpy.data.materials.get(name)
    if not mat:
        mat = bpy.data.materials.new(name=name)
        mat.use_nodes = True
        bsdf = mat.node_tree.nodes.get("Principled BSDF")
        if bsdf:
            bsdf.inputs["Base Color"].default_value = base_color
    else:
        if mat.use_nodes:
            bsdf = mat.node_tree.nodes.get("Principled BSDF")
            if bsdf:
                bsdf.inputs["Base Color"].default_value = base_color
    return mat

def run(object_name: str, material_name: str, base_color=(0.8,0.8,0.8,1.0)):
    print(f"[Blade v10] material_ensure_assign.run start obj={object_name} mat={material_name}")
    obj = bpy.data.objects.get(object_name)
    if not obj:
        return {"ok": False, "error": f"object '{object_name}' not found"}

    mat = _ensure_material(material_name, base_color)
    if obj.data is None or not hasattr(obj.data, "materials"):
        return {"ok": False, "error": "object has no material slots"}

    if len(obj.data.materials) == 0:
        obj.data.materials.append(mat)
    else:
        obj.data.materials[0] = mat

    print(f"[Blade v10] material_ensure_assign ok obj={obj.name} mat={mat.name}")
    return {"ok": True, "object": obj.name, "material": mat.name}
