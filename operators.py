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


class TRACK_OT_set_export_ref_frame(bpy.types.Operator):
    """Set current frame as export reference frame"""

    bl_idname = "track.set_export_reference_frame"
    bl_label = "Set ref frame"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        clip = get_active_movieclip_in_current_context(context)
        clip.export_reference_frame = context.scene.frame_current
        return {"FINISHED"}
