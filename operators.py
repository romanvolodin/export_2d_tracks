import bpy

from .functions import get_active_movieclip_in_current_context
from .functions import main


class TRACK_OT_export_to_clipboard(bpy.types.Operator):
    """Export 2d tracking data to clipboard"""

    bl_idname = "track.export_to_clipboard"
    bl_label = "Export 2D tracks to clipboard"
    bl_options = {"REGISTER", "UNDO"}

    target: bpy.props.StringProperty()
    scale: bpy.props.FloatProperty(default=1.0)

    def execute(self, context):
        main(context, self.target, self.scale)
        return {"FINISHED"}


class TRACK_OT_export_to_file(bpy.types.Operator):
    bl_idname = "track.export_to_file"
    bl_label = "Export 2D Tracks"

    filepath: bpy.props.StringProperty(
        name="File Path",
        description="Путь к файлу",
        subtype='FILE_PATH'
    )

    def execute(self, context):
        data_to_write = "2D track data will be here.\n"

        try:
            with open(self.filepath, 'w', encoding='utf-8') as file:
                file.write(data_to_write)
        except Exception as e:
            self.report({'ERROR'}, f"Error: {str(e)}")
        
        return {'FINISHED'}

    def invoke(self, context, event):
        if not self.filepath:
            self.filepath = "export.nk"

        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}


class TRACK_OT_set_export_ref_frame(bpy.types.Operator):
    """Set current frame as export reference frame"""

    bl_idname = "track.set_export_reference_frame"
    bl_label = "Set ref frame"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        clip = get_active_movieclip_in_current_context(context)
        clip.export_reference_frame = context.scene.frame_current
        return {"FINISHED"}
