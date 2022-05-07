import bpy

from .functions import get_active_movieclip_in_current_context


class TRACK_PT_export_panel(bpy.types.Panel):
    bl_label = "Export 2D track"
    bl_space_type = "CLIP_EDITOR"
    bl_region_type = "TOOLS"
    bl_category = "Export"

    def draw(self, context):
        clip = get_active_movieclip_in_current_context(context)
        layout = self.layout
        col = layout.column(align=True)

        if not clip:
            col.label(text="No Clip opened")
            return

        col.prop(clip, "export_to")
        col.prop(clip, "export_reference_frame", text="Ref frame")
        col.prop(clip, "export_scale", text="Scale")

        row = layout.row(align=True)
        row.scale_y = 1.5
        operator = row.operator("track.export_to_clipboard", text="Export")
        operator.target = "nuke"
        operator.scale = clip.export_scale
