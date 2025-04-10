from string import Template

fusion_tpl_start = """{
    Tools = ordered() {
        Blend_Tracker1 = Tracker {
            Trackers = {
"""
fusion_tpl_pattern = Template(
    """                {
                    PatternTime = $reference_frame,
                    PatternX = $first_frame_x,
                    PatternY = $first_frame_y,
                },
"""
)
fusion_tpl_mid_01 = """         },
            CtrlWZoom = false,
            Inputs = {
                TrackerList = Input { Value = 1, },
"""
fusion_tlp_tracker = """                Name{counter} = Input {{ Value = "{track_name}", }},
                PatternCenter{counter} = Input {{ Value = {{ 0, 0, }}, }},
                SearchWidth{counter} = Input {{ Value = 0, }},
                SearchHeight{counter} = Input {{ Value = 0, }},
                TrackedCenter{counter} = Input {{
                    SourceOp = "{path_name}",
                    Source = "Position",
                }},
"""
fusion_tpl_mid_02 = """         },
            ViewInfo = OperatorInfo { Pos = { 0, 0, }, },
        },
"""
fusion_tpl_polypath_start = """     {path_name} = PolyPath {{
            ShowKeyPoints = false,
            ShowHandles = false,
            DrawMode = "ModifyOnly",
            Inputs = {{
                Displacement = Input {{
                    SourceOp = "{path_name}Displacement",
                    Source = "Value",
                }},
                PolyLine = Input {{
                    Value = Polyline {{
                        Points = {{
"""
fusion_tpl_polypath_position = """                          {{ Linear = true, LockY = true, X = {pos_x}, Y = {pos_y}, }},
"""
fusion_tpl_polypath_end = """                       },
                    },
                },
            },
        },
"""
fusion_tpl_pathdisplace_start = """     {path_name}Displacement = BezierSpline {{
            SplineColor = {{ Red = 255, Green = 0, Blue = 255, }},
            NameSet = true,
            KeyFrames = {{
"""
fusion_tpl_pathdisplace_frame = """             [{frame}] = {{ {displace}, Flags = {{ Linear = true, LockedY = true, }}, }},
"""
fusion_tpl_pathdisplace_end = """            },
        },
"""
fusion_tpl_end = """    },
    ActiveTool = "Blend_Tracker1",
}
"""
