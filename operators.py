import bpy

from .functions import main


class TRACK_OT_export_to_clipboard(bpy.types.Operator):
    """Export 2d tracking data to clipboard"""

    bl_idname = "track.export_to_clipboard"
    bl_label = "Export 2D tracks to clipboard"
    bl_options = {"REGISTER", "UNDO"}

    target: bpy.props.StringProperty()

    def execute(self, context):
        main(context, self.target)
        return {"FINISHED"}
