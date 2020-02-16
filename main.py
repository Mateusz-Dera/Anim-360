# Anim 360
# Copyright © 2020 Mateusz Dera

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>

bl_info = {
    "name": "Anim 360",
    "description": "Plugin saves rotation animation as AVI file.",
    "author": "Mateusz Dera",
    "version": (1, 0),
    "tracker_url": "",
    "category": "Render"
}
 
import bpy
from math import radians
from mathutils import Euler

class create(bpy.types.Operator):
    bl_idname = 'anim360.create'
    bl_label = 'Create presentation'

    def execute(self, context):
        
        obj = None
        
        obj = bpy.context.scene.objects.active
            
        obj.animation_data_clear()
        
        bpy.context.scene.frame_set(1)
        obj.rotation_euler = Euler((0.0, 0.0, 0.0), 'XYZ')
        bpy.ops.anim.keyframe_insert_menu(type='LocRotScale')
        
        bpy.context.scene.frame_set(context.scene.anim360frames)
        obj.rotation_euler = Euler((0.0, 0.0, radians(context.scene.anim360degrees)), 'XYZ')
        bpy.ops.anim.keyframe_insert_menu(type='LocRotScale')
        
        context.scene.render.resolution_x = context.scene.anim360width
        context.scene.render.resolution_y = context.scene.anim360height
        context.scene.frame_end = context.scene.anim360frames
        
        if context.scene.anim360samples == "DISABLED":
            bpy.context.scene.render.use_antialiasing = False
        else:
            bpy.context.scene.render.use_antialiasing = True
            bpy.context.scene.render.antialiasing_samples = context.scene.anim360samples
        
        bpy.context.scene.render.fps = context.scene.anim360fps 
        bpy.context.scene.render.fps_base = 1
        
        context.scene.render.filepath = context.scene.anim360path
        context.scene.render.image_settings.file_format="AVI_RAW"
        bpy.ops.render.render(animation=True)
        
        return {"FINISHED"}
 
class main_panel(bpy.types.Panel):
    bl_idname = "panel.main_panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_label = "Anim 360"
    bl_category = "Anim 360"

    def draw(self, context):
        layout = self.layout
        col1 = layout.column(align = True)
        col2 = layout.column(align = True)
        col3 = layout.column(align = True)
        col4 = layout.column(align = True)
        col5 = layout.column(align = True)
        col6 = layout.column(align = True)

        col1.prop(context.scene, "anim360degrees")
        col2.prop(context.scene, "anim360frames")

        col3.prop(context.scene, "anim360width")
        col3.prop(context.scene, "anim360height")
        
        col4.prop(context.scene, "anim360fps")
        
        col5.prop(context.scene, "anim360samples")

        col6.prop(context.scene, "anim360path")

        layout.operator("anim360.create", text="Create presentation")
 
def register() :
    samples = [("16", "16", "16 samples"),("11", "11", "11 samples"),("8", "8", "8 samples"),("5", "5", "5 samples"),("DISABLED", "Disabled", "Disabled Anti-Aliasing")]
    
    bpy.utils.register_class(create)
    bpy.utils.register_class(main_panel)
    bpy.types.Scene.anim360degrees = bpy.props.FloatProperty \
      (
        name = "Degrees",
        description = "Object rotation in degrees",
        default = 360,
        min=0,
        step=100
      )
    bpy.types.Scene.anim360frames = bpy.props.IntProperty \
      (
        name = "Frames",
        description = "Number of animation frames",
        default = 240,
        min=0
      )
    bpy.types.Scene.anim360width = bpy.props.IntProperty \
      (
        name = "Width",
        description = "Render width.",
        default = 1920,
        min=1
      )
    bpy.types.Scene.anim360height = bpy.props.IntProperty \
      (
        name = "Height",
        description = "Render height.",
        default = 1080,
        min=1
      )
    bpy.types.Scene.anim360fps = bpy.props.IntProperty \
      (
        name = "FPS",
        description = "Animation FPS.",
        default = 60,
        min=24,
        max=240
      )
    bpy.types.Scene.anim360samples = bpy.props.EnumProperty \
      (
        name = "", 
        description = "Anti-Aliasing samples",
        items=samples
      )
    bpy.types.Scene.anim360path = bpy.props.StringProperty \
      (
        name = "",
        description = "Output path.",
        default = "/tmp\\",
        subtype="FILE_PATH"
      )
    
def unregister() :
    bpy.utils.unregister_class(create)
    bpy.utils.unregister_class(main_panel)
    del bpy.types.Scene.anim360degrees
    del bpy.types.Scene.anim360frames
    del bpy.types.Scene.anim360width
    del bpy.types.Scene.anim360height
    del bpy.types.Scene.anim360fps
    del bpy.types.Scene.anim360samples
    del bpy.types.Scene.anim360path

if __name__ == "__main__" :
    register()