from string import Template


first_chunk = Template("x$start_frame $positions")
chunk = Template("x$first_frame $first_position x$second_frame $positions")

track = Template(
    """ { {curve K x$start_frame 1} "$track_name"
 {curve $x_positions}
 {curve $y_positions}
 {curve K x$start_frame 0}
 {curve K x$start_frame 0} 1 1 1
 {curve x$start_frame 0} 0 0 -32 -32 32 32 -22 -22 22 22
 {}
 {}
 {}
 {}
 {}
 {}
 {}
 {}
 {}
 {}
 {}
 }
"""
)

node = Template(
    """
Tracker4 {
tracks { { 1 31 $tracks_count }
{ { 5 1 20 enable e 1 }
{ 3 1 75 name name 1 }
{ 2 1 58 track_x track_x 1 }
{ 2 1 58 track_y track_y 1 }
{ 2 1 63 offset_x offset_x 1 }
{ 2 1 63 offset_y offset_y 1 }
{ 4 1 27 T T 1 }
{ 4 1 27 R R 1 }
{ 4 1 27 S S 1 }
{ 2 0 45 error error 1 }
{ 1 1 0 error_min error_min 1 }
{ 1 1 0 error_max error_max 1 }
{ 1 1 0 pattern_x pattern_x 1 }
{ 1 1 0 pattern_y pattern_y 1 }
{ 1 1 0 pattern_r pattern_r 1 }
{ 1 1 0 pattern_t pattern_t 1 }
{ 1 1 0 search_x search_x 1 }
{ 1 1 0 search_y search_y 1 }
{ 1 1 0 search_r search_r 1 }
{ 1 1 0 search_t search_t 1 }
{ 2 1 0 key_track key_track 1 }
{ 2 1 0 key_search_x key_search_x 1 }
{ 2 1 0 key_search_y key_search_y 1 }
{ 2 1 0 key_search_r key_search_r 1 }
{ 2 1 0 key_search_t key_search_t 1 }
{ 2 1 0 key_track_x key_track_x 1 }
{ 2 1 0 key_track_y key_track_y 1 }
{ 2 1 0 key_track_r key_track_r 1 }
{ 2 1 0 key_track_t key_track_t 1 }
{ 2 1 0 key_centre_offset_x key_centre_offset_x 1 }
{ 2 1 0 key_centre_offset_y key_centre_offset_y 1 }
}
{
$tracks
}
}

reference_frame $reference_frame
center {$center}
filter Lanczos4
selected_tracks 0
name $node_name
label $label
selected true
}
"""
)
