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


def split_on_dropped_frames(markers):
    splitted_sequence = [[]]
    for index, marker in enumerate(markers[:-1]):
        next_frame = markers[index + 1].frame
        splitted_sequence[-1].append(marker)
        if next_frame != marker.frame + 1:
            splitted_sequence.append([])
    splitted_sequence[-1].append(markers[-1])
    return splitted_sequence


def fill_nuke_template(clip, blend_path, scale=1.0):
    frame_offset = clip.frame_start - 1
    width, height = clip.size
    track_obj = clip.tracking.objects.active
    clean_track_obj_name = track_obj.name.replace(".", "_")
    selected_tracks = [track for track in track_obj.tracks if track.select]
    tracks = []
    for track in selected_tracks:
        enabled_markers = [marker for marker in track.markers if not marker.mute]
        chunked_markers = split_on_dropped_frames(enabled_markers)
        first_chunk, *rest_chunks = chunked_markers
        x_positions = [
            nuke.first_chunk.substitute(
                start_frame=first_chunk[0].frame + frame_offset,
                positions=" ".join([str(m.co.x * width * scale) for m in first_chunk]),
            )
        ]
        y_positions = [
            nuke.first_chunk.substitute(
                start_frame=first_chunk[0].frame + frame_offset,
                positions=" ".join([str(m.co.y * height * scale) for m in first_chunk]),
            )
        ]
        for chunk in rest_chunks:
            x_positions.append(
                nuke.chunk.substitute(
                    first_frame=chunk[0].frame + frame_offset,
                    first_position=chunk[0].co.x * width * scale,
                    second_frame=chunk[1].frame + frame_offset,
                    positions=" ".join(
                        [str(m.co.x * width * scale) for m in chunk[1:]]
                    ),
                )
            )
            y_positions.append(
                nuke.chunk.substitute(
                    first_frame=chunk[0].frame + frame_offset,
                    first_position=chunk[0].co.y * height * scale,
                    second_frame=chunk[1].frame + frame_offset,
                    positions=" ".join(
                        [str(m.co.y * height * scale) for m in chunk[1:]]
                    ),
                )
            )
        tracks.append(
            nuke.track.substitute(
                track_name=track.name.replace(".", "_"),
                start_frame=first_chunk[0].frame + frame_offset,
                x_positions=" ".join(x_positions),
                y_positions=" ".join(y_positions),
            )
        )
    return nuke.node.substitute(
        tracks_count=len(selected_tracks),
        tracks="\n".join(tracks),
        reference_frame=clip.export_reference_frame,
        center=f"{width / 2} {height / 2}",
        node_name=f"Blend_Tracker_{clean_track_obj_name}",
        label=f"\"...[python {{'{blend_path}'[-35:]}}]\"",
    )


def main(context, target, scale):
    clip = get_active_movieclip_in_current_context(context)

    if target == "nuke":
        nuke_node = fill_nuke_template(clip, context.blend_data.filepath, scale)
    context.window_manager.clipboard = nuke_node
