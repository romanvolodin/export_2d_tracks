from .templates import nuke


def get_active_movieclip_in_current_context(context):
    area = context.area
    spaces = [space for space in area.spaces if space.type == "CLIP_EDITOR"]
    if not spaces:
        return
    space = spaces[0]
    active_clip = space.clip
    if active_clip:
        return active_clip


def fill_nuke_template(clip, blend_path, scale=1.0):
    width, height = clip.size
    track_obj = clip.tracking.objects.active
    selected_tracks = [track for track in track_obj.tracks if track.select]
    tracks = []
    for track in selected_tracks:
        enabled_markers = [marker for marker in track.markers if not marker.mute]
        x_positions = [str(m.co.x * width * scale) for m in enabled_markers]
        y_positions = [str(m.co.y * height * scale) for m in enabled_markers]
        tracks.append(
            nuke.track.substitute(
                track_name=track.name,
                start_frame=enabled_markers[0].frame,
                x_positions=" ".join(x_positions),
                y_positions=" ".join(y_positions),
            )
        )
    return nuke.node.substitute(
        tracks_count=len(selected_tracks),
        tracks="\n".join(tracks),
        reference_frame=clip.export_reference_frame,
        center=f"{width / 2} {height / 2}",
        node_name=f"Blend_Tracker_{track_obj.name}",
        label=f"\"...[python {{'{blend_path}'[-35:]}}]\"",
    )


def main(context, target):
    clip = get_active_movieclip_in_current_context(context)

    if target == "nuke":
        nuke_node = fill_nuke_template(clip, context.blend_data.filepath)
    context.window_manager.clipboard = nuke_node
