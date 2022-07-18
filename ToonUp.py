bl_info = {
    "name": "ToonUp",
    "author": "SpectralVectors",
    "version": (0, 1, 2),
    "blender": (3, 0, 40),
    "location": "View 3D > Sidebar (N-Panel)",
    "description": "Toon shades and outlines the selected object",
    "category": "Object",
}


import bpy

class ToonUpProperties(bpy.types.PropertyGroup):

    shadow_color : bpy.props.FloatVectorProperty(
        name = 'Shadow',
        default = (0, 0, 0, 1),
        min = 0,
        max = 1,
        size = 4,
        subtype = 'COLOR',
    )

    midtone_color : bpy.props.FloatVectorProperty(
        name = 'Midtone',
        default = (0.5, 0.5, 0.5, 1),
        min = 0,
        max = 1,
        size = 4,
        subtype = 'COLOR',
    )    

    highlight_color : bpy.props.FloatVectorProperty(
        name = 'Highlight',
        default = (0.9, 0.9, 0.9, 1),
        min = 0,
        max = 1,
        size = 4,
        subtype = 'COLOR',
    )

    outline_color : bpy.props.FloatVectorProperty(
        name = 'Outline',
        default = (0, 0, 0, 1),
        min = 0,
        max = 1,
        size = 4,
        subtype = 'COLOR',
    )

def toonup():

    toonup_properties = bpy.context.scene.toonup_properties

    object = bpy.context.object
    bpy.ops.object.shade_smooth()

    if object.type == 'MESH':
        
        # Creating our Toon Shader Material
        toon_shader = bpy.data.materials.new(name='Toon Shader')
        toon_shader.use_nodes = True
        toon_shader.node_tree.nodes.clear()
        
        nodes = toon_shader.node_tree.nodes
        
        output = nodes.new(type='ShaderNodeOutputMaterial')
        
        color_ramp = nodes.new(type='ShaderNodeValToRGB')
        color_ramp.color_ramp.interpolation = 'CONSTANT'
        color_ramp.color_ramp.elements[1].position = 0.9
        color_ramp.color_ramp.elements.new(position = 0.2)
        color_ramp.color_ramp.elements[0].color = toonup_properties.shadow_color
        color_ramp.color_ramp.elements[1].color = toonup_properties.midtone_color
        color_ramp.color_ramp.elements[2].color = toonup_properties.highlight_color
        
        diffuse = nodes.new(type="ShaderNodeBsdfDiffuse")

        shader_to_rgb = nodes.new(type="ShaderNodeShaderToRGB")
        
        links = toon_shader.node_tree.links
        
        links.new(color_ramp.outputs[0], output.inputs[0])
        links.new(shader_to_rgb.outputs[0], color_ramp.inputs[0])
        links.new(diffuse.outputs[0], shader_to_rgb.inputs[0])
        
        # Creating our Outline Material
        outline = bpy.data.materials.new(name='Outline')
        outline.use_nodes = True
        outline.use_backface_culling = True
        outline.node_tree.nodes.clear()
        
        nodes = outline.node_tree.nodes
        
        output = nodes.new(type='ShaderNodeOutputMaterial')
        emission = nodes.new(type='ShaderNodeEmission')
        # Outline Color
        emission.inputs[0].default_value = toonup_properties.outline_color
        
        links = outline.node_tree.links
        
        links.new(emission.outputs[0], output.inputs[0])
        
        object.data.materials.append(toon_shader)
        object.data.materials.append(outline)
        
        # Adding a solidify modifier
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

        toonup_properties = bpy.context.scene.toonup_properties

        layout = self.layout

        column = layout.column()
        box = column.box()
        box.prop(toonup_properties, 'highlight_color')
        box.prop(toonup_properties, 'midtone_color')
        box.prop(toonup_properties, 'shadow_color')
        box.prop(toonup_properties, 'outline_color')
        box = column.box()
        box.label(text = 'Operator:')
        box.operator('object.toonup_operator', text= 'Toon Up!')


classes = [
ToonUpPanel,
ToonUpOperator,
ToonUpProperties,
]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    
    bpy.types.Scene.toonup_properties = bpy.props.PointerProperty(type=ToonUpProperties)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()


