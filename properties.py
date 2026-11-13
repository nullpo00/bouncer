# SPDX-License-Identifier: GPL-3.0-or-later

# type: ignore

import bpy

class BounceProperties(bpy.types.PropertyGroup):

    location_enabled: bpy.props.BoolProperty(
        name="Location",
        description="Enable the location offset",
        default=True
    )

    rotation_enabled: bpy.props.BoolProperty(
        name="Rotation",
        description="Enable the rotation offset",
        default=True,
    )

    scale_enabled: bpy.props.BoolProperty(
        name="Scale",
        description="Enable the scale offset",
        default=True
    )

    use_current_frame: bpy.props.BoolProperty(
        name="Use Current Frame",
        description="Use current frame for start frame of animation",
        default=True
    )

    sort_option_enabled: bpy.props.BoolProperty(
        name="Sort Option",
        description="Enable sort option",
        default=False
    )

    sort_reverse_enabled: bpy.props.BoolProperty(
        name="Reverse",
        description="Enable reverse sort",
        default=False
    )

    use_sort_obj: bpy.props.BoolProperty(
        name="Use Sort Object",
        description="Use any object for sort of Frame Offset",
        default=False
    )

    fast_mode_enabled: bpy.props.BoolProperty(
        name="Fast Mode",
        description="Use fast mode. (Unstable)",
        default=False
    )

    location_ofs: bpy.props.FloatVectorProperty(
        name="",
        subtype="TRANSLATION",
        default=(0.0, 0.0, 0.0),
        step=1,
        precision=3
    )

    rotation_ofs: bpy.props.FloatVectorProperty(
        name="",
        subtype="EULER",
        default=(0.0, 0.0, 0.0),
        step=100
    )

    scale_ofs: bpy.props.FloatVectorProperty(
        name="",
        subtype="XYZ",
        default=(1.0, 1.0, 1.0),
        step=1,
        precision=3
    )

    bounce_amp: bpy.props.FloatProperty(
        name="Amplitude",
        default=1.0,
        min=0.0,
        step=1
    )

    bounce_period: bpy.props.FloatProperty(
        name="Period",
        default=30.0,
        step=10
    )

    start_frame: bpy.props.IntProperty(
        name="Start Frame",
        default=1,
        min=0,
        step=1
    )

    anim_duration: bpy.props.IntProperty(
        name="Duration",
        default=60,
        min=0,
        step=1
    )

    frame_ofs: bpy.props.IntProperty(
        name="Frame Offset",
        default=3,
        min=0,
        step=1
    )

    sort_origin: bpy.props.PointerProperty(
        name="Sort Origin",
        description="Sort by distance from this object",
        type=bpy.types.Object
    )

    sort_type: bpy.props.EnumProperty(
        name="Sort Type",
        description="Sort Type",
        items=[
            ("DISTANCE", "Distance", "Distance", "", 0),
            ("LOCATION", "Location", "Location", "", 1),
            ("ROTATION", "Rotation", "Rotation", "", 2),
            ("SCALE", "Scale", "Scale", "", 3)
        ],
        default="DISTANCE"
    )

    sort_axis: bpy.props.EnumProperty(
        name="Sort Axis",
        description="Sort Axis",
        items=[
            ("AXIS_X", "X", "Axis X", "", 0),
            ("AXIS_Y", "Y", "Axis Y", "", 1),
            ("AXIS_Z", "Z", "Axis Z", "", 2)
        ],
        default="AXIS_X"
    )

register_classes = [
    BounceProperties
]
    
def init():
    bpy.types.Scene.bounce_props = bpy.props.PointerProperty(type=BounceProperties)

def finalize():
    del bpy.types.Scene.bounce_props
