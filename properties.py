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

register_classes = [
    BounceProperties
]
    
def construct_pointer_property():
    bpy.types.Scene.bounce_props = bpy.props.PointerProperty(type=BounceProperties)

def delete_pointer_property():
    del bpy.types.Scene.bounce_props
