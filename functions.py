from pathlib import Path

import math

from .templates import fusion
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


def length(a, b):
    return math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)


def track_path_len(position):
    full_leng = 0
    for i, j in enumerate(position[:-1]):
        x_position, y_position = j
        x_position_next, y_position_next = position[i + 1]
        leng = length([x_position, y_position], [x_position_next, y_position_next])
        full_leng += leng
    return full_leng


def marker_relative_pos(position, full_leng):
    otn_leng = 0
    relative_position = [0]
    for i, j in enumerate(position[:-1]):
        x_position, y_position = j
        x_position_next, y_position_next = position[i + 1]
        leng = length([x_position, y_position], [x_position_next, y_position_next])
        otn_leng += leng
        otn_position = otn_leng / full_leng
        relative_position.append(otn_position)
    return relative_position


def fill_nuke_template(clip, blend_path, scale=1.0):
    posix_blend_path = Path(blend_path).as_posix()
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
        label=f"\"...[python {{'{posix_blend_path}'[-35:]}}]\"",
    )


def fill_fusion_template(clip, blend_path):
    track_obj = clip.tracking.objects.active
    # time_step = 1 / (clip.frame_duration - 1)
    data = []
    selected_tracks = [track for track in track_obj.tracks if track.select]

    tracks_count = range(1, len(selected_tracks) + 1)

    data.append(fusion.fusion_tpl_start)

    for _ in tracks_count:
        data.append(
            fusion.fusion_tpl_pattern.substitute(
                reference_frame=clip.export_reference_frame,
                first_frame_x=0,
                first_frame_y=0,
            )
        )

    data.append(fusion.fusion_tpl_mid_01)

    for counter, track in enumerate(selected_tracks, 1):
        name = track.name.replace(".", "_") + "_"
        data.append(
            fusion.fusion_tlp_tracker.format(
                counter=counter, track_name=name, path_name=name
            )
        )

    data.append(fusion.fusion_tpl_mid_02)

    for counter, track in enumerate(selected_tracks, 1):
        name = track.name.replace(".", "_") + "_"
        data.append(
            fusion.fusion_tpl_polypath_start.format(counter=counter, path_name=name)
        )
        markers = track.markers[1:-1]
        markers_position = []
        for m in markers:
            data.append(
                fusion.fusion_tpl_polypath_position.format(
                    pos_x=m.co.x - 0.5, pos_y=m.co.y - 0.5
                )
            )
            markers_position.append((m.co.x, m.co.y))
        full_leng = track_path_len(markers_position)
        relative_pos = marker_relative_pos(markers_position, full_leng)
        data.append(fusion.fusion_tpl_polypath_end)
        data.append(
            fusion.fusion_tpl_pathdisplace_start.format(counter=counter, path_name=name)
        )
        for index, m in enumerate(markers):
            data.append(
                fusion.fusion_tpl_pathdisplace_frame.format(
                    frame=m.frame - 1, displace=relative_pos[index]
                )
            )
        data.append(fusion.fusion_tpl_pathdisplace_end)

    data.append(fusion.fusion_tpl_end)

    return "".join(data)


def main(context, target, scale):
    clip = get_active_movieclip_in_current_context(context)

    if target == "NU":
        nuke_node = fill_nuke_template(clip, context.blend_data.filepath, scale)
        context.window_manager.clipboard = nuke_node

    if target == "FU":
        fusion_node = fill_fusion_template(clip, context.blend_data.filepath)
        context.window_manager.clipboard = fusion_node
