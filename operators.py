# SPDX-License-Identifier: GPL-3.0-or-later

# type: ignore

import bpy
from . import properties
from bpy_extras import anim_utils

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
    def insert_keyframe(self, obj: bpy.types.Object, data_path: str, frame: int, values: list[tuple[float, str]]) -> None:

        # X
        exec(f"obj.{data_path}.x = {values[0][0]}")
        print(values[0][0])
        obj.keyframe_insert(data_path=data_path, index=0, frame=frame)
        ad = obj.animation_data
        channelbag = anim_utils.action_get_channelbag_for_slot(ad.action, ad.action_slot)
        fc_x = channelbag.fcurves.find(data_path, index=0)
        kf = [kf for kf in fc_x.keyframe_points if kf.co[0] == frame][0]
        kf.interpolation = values[0][1]
        if values[0][1] == "ELASTIC":
            kf.amplitude = self.amp
            kf.period = self.period

        # Y
        exec(f"obj.{data_path}.y = {values[1][0]}")
        obj.keyframe_insert(data_path=data_path, index=1, frame=frame)
        ad = obj.animation_data
        channelbag = anim_utils.action_get_channelbag_for_slot(ad.action, ad.action_slot)
        fc_y = channelbag.fcurves.find(data_path, index=1)
        kf = [kf for kf in fc_y.keyframe_points if kf.co[0] == frame][0]
        kf.interpolation = values[1][1]
        if values[1][1] == "ELASTIC":
            kf.amplitude = self.amp
            kf.period = self.period
        # Z
        exec(f"obj.{data_path}.z = {values[2][0]}")
        obj.keyframe_insert(data_path=data_path, index=2, frame=frame)
        ad = obj.animation_data
        channelbag = anim_utils.action_get_channelbag_for_slot(ad.action, ad.action_slot)
        fc_z = channelbag.fcurves.find(data_path, index=2)
        kf = [kf for kf in fc_z.keyframe_points if kf.co[0] == frame][0]
        kf.interpolation = values[2][1]
        if values[2][1] == "ELASTIC":
            kf.amplitude = self.amp
            kf.period = self.period

        # Update
        fc_x.update()
        fc_y.update()
        fc_z.update()

        ad.action.update_tag()

    # Insert keyframe for XYZ (Fast Mode)
    def insert_keyframe_fast(self, obj: bpy.types.Object, data_path: str, frame: int, values: list[tuple[float, str]]) -> None:
        
        if obj.animation_data is None:
            obj.animation_data_create()

        ad = obj.animation_data
        if ad.action is None:
            ad.action = bpy.data.actions.new(name=obj.name + "Action")

        # Get F-Curve info
        channelbag = anim_utils.action_ensure_channelbag_for_slot(ad.action, ad.action_slot)
        fc_x = channelbag.fcurves.ensure(data_path, index=0)
        fc_y = channelbag.fcurves.ensure(data_path, index=1)
        fc_z = channelbag.fcurves.ensure(data_path, index=2)

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

        ad.action.update_tag()

    # Override
    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False

        layout.prop(self, "amp")
        layout.prop(self, "period")
        layout.prop(self, "frame_ofs")
        layout.prop(self, "duration")
   
    # Override
    def execute(self, context):

        props = context.scene.bounce_props
        active_object = context.active_object
        selected_objects = context.selected_objects

        if not active_object or not selected_objects:
            self.report({"INFO"}, "Object is not selected or active object is None")
            return{"CANCELLED"}

        if props.use_sort_obj and not props.sort_origin:
            self.report({"INFO"}, "Sort Origin is not selected")
            return{"CANCELLED"}

        sort_obj = props.sort_origin if props.use_sort_obj else active_object
        reverse = props.sort_reverse_enabled
        sort_key = None
        
        # Sort
        if props.sort_type == "DISTANCE":
            # Sort by distance
            pt_x = sort_obj.matrix_world.translation.x
            pt_y = sort_obj.matrix_world.translation.y
            pt_z = sort_obj.matrix_world.translation.z

            sort_key = lambda obj: ((obj.matrix_world.translation.x - pt_x) ** 2 
                + (obj.matrix_world.translation.y - pt_y) ** 2 
                + (obj.matrix_world.translation.z - pt_z) ** 2)
        else:
            idx = context.scene.bounce_props.bl_rna.properties["sort_axis"].enum_items[props.sort_axis].value
            match props.sort_type:
                case "LOCATION":
                    sort_key = lambda obj: (obj.location[idx] - sort_obj.location[idx])
                case "ROTATION":
                    sort_key = lambda obj: (obj.rotation_euler[idx] - sort_obj.rotation_euler[idx])
                case "SCALE":
                    sort_key = lambda obj: (obj.scale[idx] - sort_obj.scale[idx])

        if sort_key:
            selected_objects.sort(key=sort_key, reverse=reverse)

        default_interpolation = context.preferences.edit.keyframe_new_interpolation_type
        st_frame = context.scene.frame_current if props.use_current_frame else props.start_frame
        
        for cnt, obj in enumerate(selected_objects):
            
            if  isinstance(obj, bpy.types.Object) and hasattr(obj, "keyframe_insert"):
                frame = st_frame + self.frame_ofs * cnt
                loc = obj.location.copy()
                rot = obj.rotation_euler.copy()
                scl = obj.scale.copy()

                exec_func = self.insert_keyframe_fast if props.fast_mode_enabled else self.insert_keyframe

                # Location keyframe
                if props.location_enabled:
                    default_val = props.bl_rna.properties["location_ofs"].default_array
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
                    exec_func(obj=obj, data_path="location", frame=frame, values=values)
                    values = [(item, default_interpolation) for item in list(loc)]
                    exec_func(obj=obj, data_path="location", frame=frame + self.duration, values=values)

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
                    exec_func(obj=obj, data_path="rotation_euler", frame=frame, values=values)
                    values = [(item, default_interpolation) for item in list(rot)]
                    exec_func(obj=obj, data_path="rotation_euler", frame=frame + self.duration, values=values)

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
                    exec_func(obj=obj, data_path="scale", frame=frame, values=values)
                    values = [(item, default_interpolation) for item in list(scl)]
                    exec_func(obj=obj, data_path="scale", frame=frame + self.duration, values=values)

                obj.update_tag()

        return {"FINISHED"}
    
    # Override
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

    # Override
    def execute(self, context):

        props = context.scene.bounce_props

        # Get properties name
        prop_names = list(properties.BounceProperties.__annotations__.keys())

        # Reset
        for name in prop_names:
            props.property_unset(name)

        return {"FINISHED"}

register_classes = [
    ApplyAnimationOperator,
    ResetPropertiesOperator
]
