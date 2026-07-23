# SPDX-License-Identifier: GPL-3.0-or-later

# type: ignore

import bpy
from typing_extensions import override
from . import properties

class ApplyAnimationOperator(bpy.types.Operator):
    bl_idname = "bouncer.apply_animation_operator"
    bl_label = "Apply Animation"
    bl_options = {"REGISTER", "UNDO"}

    amp: bpy.props.FloatProperty(
        name="Amplitude",
        min=0.0,
        step=1
    )

    period: bpy.props.FloatProperty(
        name="Period",
        step=10
    )

    frame_ofs: bpy.props.IntProperty(
        name="Frame Offset",
        min=0,
        step=1
    )

    duration: bpy.props.IntProperty(
        name="Duration",
        min=0,
        step=1
    )

    # Insert keyframe for XYZ
    # XYZへキーフレーム追加
    def insert_keyframe(self, object: bpy.types.Object, data_path: str, frame: int, values: list[tuple[float, str]]) -> None:

        if object.animation_data is None:
            object.animation_data_create()

        action = object.animation_data.action
        if action is None:
            action = bpy.data.actions.new(name=object.name + "Action")
            object.animation_data.action = action

        # Get F-Curve info
        # Fカーブ情報取得
        fc_x = action.fcurve_ensure_for_datablock(datablock=object, data_path=data_path, index=0)
        fc_y = action.fcurve_ensure_for_datablock(datablock=object, data_path=data_path, index=1)
        fc_z = action.fcurve_ensure_for_datablock(datablock=object, data_path=data_path, index=2)

        # X
        kf = fc_x.keyframe_points.insert(frame=frame, value=values[0][0])
        kf.interpolation = values[0][1]
        if values[0][1] == "ELASTIC":
            kf.amplitude = self.amp
            kf.period = self.period

        # Y
        kf = fc_y.keyframe_points.insert(frame=frame, value=values[1][0])
        kf.interpolation = values[1][1]
        if values[1][1] == "ELASTIC":
            kf.amplitude = self.amp
            kf.period = self.period
        # Z
        kf = fc_z.keyframe_points.insert(frame=frame, value=values[2][0])
        kf.interpolation = values[2][1]
        if values[2][1] == "ELASTIC":
            kf.amplitude = self.amp
            kf.period = self.period

        # Update
        fc_x.update()
        fc_y.update()
        fc_z.update()

        action.update_tag()

    @override
    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False

        layout.prop(self, "amp")
        layout.prop(self, "period")
        layout.prop(self, "frame_ofs")
        layout.prop(self, "duration")
   
    @override
    def execute(self, context):

        active_object = context.active_object
        selected_objects = context.selected_objects

        if not active_object or not selected_objects:
            self.report({"INFO"}, "Object is not selected or active object is None")
            return{"CANCELLED"}

        # Sort by distance from active object
        # アクティブオブジェクトからの距離でソート
        pt_x = active_object.matrix_world.translation.x
        pt_y = active_object.matrix_world.translation.y
        pt_z = active_object.matrix_world.translation.z

        selected_objects.sort(
            key=lambda obj: (obj.matrix_world.translation.x - pt_x) ** 2 
            + (obj.matrix_world.translation.y - pt_y) ** 2 
            + (obj.matrix_world.translation.z - pt_z) ** 2
        )

        props = context.scene.bounce_props
        default_interpolation = context.preferences.edit.keyframe_new_interpolation_type
        st_frame = context.scene.frame_current if props.use_current_frame else props.start_frame
        
        for cnt, obj in enumerate(selected_objects):
            
            if  isinstance(obj, bpy.types.Object) and hasattr(obj, "keyframe_insert"):
                frame = st_frame + self.frame_ofs * cnt

                # Location keyframe
                if props.location_enabled:
                    default_val = props.bl_rna.properties["location_ofs"].default_array
                    # キーフレーム情報格納
                    # values = [(X keyframe value, X interpolation), Y..., Z...]
                    values = [
                        (
                            obj.location.x + props.location_ofs[0], 
                            default_interpolation if props.location_ofs[0] == default_val[0] else "ELASTIC"
                        ), 
                        (
                            obj.location.y + props.location_ofs[1], 
                            default_interpolation if props.location_ofs[1] == default_val[1] else "ELASTIC"
                        ),
                        (
                            obj.location.z + props.location_ofs[2], 
                            default_interpolation if props.location_ofs[2] == default_val[2] else "ELASTIC"
                        )
                    ]
                    self.insert_keyframe(object=obj, data_path="location", frame=frame, values=values)
                    values = [(item, default_interpolation) for item in list(obj.location)]
                    self.insert_keyframe(object=obj, data_path="location", frame=frame + self.duration, values=values)

                # Rotation keyframe
                if props.rotation_enabled:
                    default_val = props.bl_rna.properties["rotation_ofs"].default_array
                    values = [
                        (
                            obj.rotation_euler.x + props.rotation_ofs[0], 
                            default_interpolation if props.rotation_ofs[0] == default_val[0] else "ELASTIC"
                        ),
                        (
                            obj.rotation_euler.y + props.rotation_ofs[1], 
                            default_interpolation if props.rotation_ofs[1] == default_val[1] else "ELASTIC"
                        ),
                        (
                            obj.rotation_euler.z + props.rotation_ofs[2], 
                            default_interpolation if props.rotation_ofs[2] == default_val[2] else "ELASTIC"
                        )
                    ]
                    self.insert_keyframe(object=obj, data_path="rotation_euler", frame=frame, values=values)
                    values = [(item, default_interpolation) for item in list(obj.rotation_euler)]
                    self.insert_keyframe(object=obj, data_path="rotation_euler", frame=frame + self.duration, values=values)

                # Scale keyframe
                if props.scale_enabled:
                    default_val = props.bl_rna.properties["scale_ofs"].default_array
                    values = [
                        (
                            obj.scale[0] * props.scale_ofs[0], 
                            default_interpolation if props.scale_ofs[0] == default_val[0] else "ELASTIC"
                        ),
                        (
                            obj.scale[1] * props.scale_ofs[1], 
                            default_interpolation if props.scale_ofs[1] == default_val[1] else "ELASTIC"
                        ),
                        (
                            obj.scale[2] * props.scale_ofs[2], 
                            default_interpolation if props.scale_ofs[2] == default_val[2] else "ELASTIC"
                        )
                    ]
                    self.insert_keyframe(object=obj, data_path="scale", frame=frame, values=values)
                    values = [(item, default_interpolation) for item in list(obj.scale)]
                    self.insert_keyframe(object=obj, data_path="scale", frame=frame + self.duration, values=values)

                obj.update_tag()

        return {"FINISHED"}
    
    @override
    def invoke(self, context, event):
        props = context.scene.bounce_props

        self.amp = props.bounce_amp
        self.period = props.bounce_period
        self.frame_ofs = props.frame_ofs
        self.duration = props.anim_duration

        return self.execute(context)
    

class ResetPropertiesOperator(bpy.types.Operator):
    bl_idname = "bouncer.reset_properties_operator"
    bl_label = "Reset Properties"
    bl_options = {"REGISTER", "UNDO"}

    @override
    def execute(self, context):

        props = context.scene.bounce_props

        # アノテーションからプロパティ名を取得
        prop_names = list(properties.BounceProperties.__annotations__.keys())

        # Reset
        for name in prop_names:
            props.property_unset(name)

        return {"FINISHED"}

register_classes = [
    ApplyAnimationOperator,
    ResetPropertiesOperator
]
