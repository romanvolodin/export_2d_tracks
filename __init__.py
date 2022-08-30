import bpy

from .operators import TRACK_OT_export_to_clipboard
from .operators import TRACK_OT_set_export_ref_frame
from .panel import TRACK_PT_export_panel

bl_info = {
    "name": "Export 2D Tracks",
    "author": "Roman Volodin, roman.volodin@gmail.com",
    "version": (1, 0, 0),
    "blender": (2, 83, 0),
    "location": "Movie Clip Editor > Tool Panel",
    "description": "Export 2d tracking data to Nuke, Fusion, AE and TXT file",
    "category": "Import-Export",
}

classes = (
    TRACK_PT_export_panel,
    TRACK_OT_export_to_clipboard,
    TRACK_OT_set_export_ref_frame,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.MovieClip.export_to = bpy.props.EnumProperty(
        items=[
            ("NU", "Nuke", "Export to Nuke"),
            ("FU", "Fusion", "Export to Fusion"),
            ("AE", "AfterEffects", "Export to AfterEffects"),
            ("TX", "Plain text", "Export as a plain text"),
        ],
        name="To",
        default="NU",
    )
    bpy.types.MovieClip.export_reference_frame = bpy.props.IntProperty(default=1)
    bpy.types.MovieClip.export_scale = bpy.props.FloatProperty(default=1)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    del bpy.types.MovieClip.export_to
    del bpy.types.MovieClip.export_reference_frame
    del bpy.types.MovieClip.export_scale


if __name__ == "__main__":
    register()
