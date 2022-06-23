bl_info = {
    "name": "ToonUp",
    "author": "SpectralVectors",
    "version": (0, 0, 1),
    "blender": (3, 0, 40),
    "location": "View 3D > Sidebar (N-Panel)",
    "description": "Toon shades and outlines the selected object",
    "category": "Object",
}


import bpy

def toonup():
    object = bpy.context.object
    bpy.ops.object.shade_smooth()


    if object.type == 'MESH':
        
        toon_shader = bpy.data.materials.new(name='Toon Shader')
        toon_shader.use_nodes = True
        toon_shader.node_tree.nodes.clear()
        
        nodes = toon_shader.node_tree.nodes
        
        output = nodes.new(type='ShaderNodeOutputMaterial')
        
        color_ramp = nodes.new(type='ShaderNodeValToRGB')
        color_ramp.color_ramp.interpolation = 'CONSTANT'
        color_ramp.color_ramp.elements[1].position = 0.9
        color_ramp.color_ramp.elements.new(position = 0.2)
        color_ramp.color_ramp.elements[1].color = (0.158747, 0.158747, 0.158747, 1)
        
        diffuse = nodes.new(type="ShaderNodeBsdfDiffuse")

        shader_to_rgb = nodes.new(type="ShaderNodeShaderToRGB")
        
        links = toon_shader.node_tree.links
        
        links.new(color_ramp.outputs[0], output.inputs[0])
        links.new(shader_to_rgb.outputs[0], color_ramp.inputs[0])
        links.new(diffuse.outputs[0], shader_to_rgb.inputs[0])
        

        outline = bpy.data.materials.new(name='Outline')
        outline.use_nodes = True
        outline.use_backface_culling = True
        outline.node_tree.nodes.clear()
        
        nodes = outline.node_tree.nodes
        
        output = nodes.new(type='ShaderNodeOutputMaterial')
        emission = nodes.new(type='ShaderNodeEmission')
        emission.inputs[0].default_value = (0, 0, 0, 1)
        
        links = outline.node_tree.links
        
        links.new(emission.outputs[0], output.inputs[0])
        
        object.data.materials.append(toon_shader)
        object.data.materials.append(outline)
        
        bpy.ops.object.modifier_add(type='SOLIDIFY')
        solidify = object.modifiers['Solidify']
        solidify.use_flip_normals = True
        solidify.material_offset = 1

        bpy.context.space_data.shading.type = 'RENDERED'

class ToonUpOperator(bpy.types.Operator):
    """Adds a Toon Shader and Outline to the selected Object"""
    bl_idname = "object.toonup_operator"
    bl_label = "ToonUp"

    def execute(self, context):        
        toonup()       
        return {'FINISHED'}


class ToonUpPanel(bpy.types.Panel):
    """ToonUp UI Panel"""

    bl_label = "ToonUp"
    bl_idname = "VIEW_3D_PT_toonup"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI' 
    bl_category = "ToonUp"

    def draw(self, context):

        layout = self.layout

        row = layout.row()
        row.operator('object.toonup_operator')


classes = [
ToonUpPanel,
ToonUpOperator,
]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()


