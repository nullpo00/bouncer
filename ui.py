# SPDX-License-Identifier: GPL-3.0-or-later

# type: ignore

import bpy

class BouncerUiPanel(bpy.types.Panel):
    bl_idname = "ANIMATION_PT_bouncer_ui"
    bl_label = "Bouncer"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Bouncer"

    # override
    def draw(self, context):

        layout = self.layout
        scene = context.scene
        props = scene.bounce_props

        # Transform Offset
        header, body = layout.panel("transform_settings", default_closed=False)
        header.label(text="Transform Offset")
        if body:

            # Location
            row = body .row()
            row.prop(props, "location_enabled")
            col = body.column()
            col.prop(props, "location_ofs")
            col.active = props.location_enabled

            # Rotation
            row = body.row()
            row.prop(props, "rotation_enabled")
            col = body.column()
            col.prop(props, "rotation_ofs")
            col.active = props.rotation_enabled

            # Scale
            row = body.row()
            row.prop(props, "scale_enabled")
            col = body.column()
            col.prop(props, "scale_ofs")
            col.active = props.scale_enabled

        # Animation Settings
        header, body = layout.panel(idname="animation_settings", default_closed=False)
        header.label(text="Animation Settings")

        if body:
            box = body.row().box()
            box.prop(props, "use_current_frame")
            if not props.use_current_frame:
                box.prop(props, "start_frame")
            
            col = body.row().box().column()
            col.prop(props, "bounce_amp", text=bpy.app.translations.pgettext_iface(msgid="Amplitude", msgctxt="BouncerPanel"))
            col.prop(props, "bounce_period", text=bpy.app.translations.pgettext_iface(msgid="Period", msgctxt="BouncerPanel"))
            col.prop(props, "anim_duration")
            col.prop(props, "frame_ofs")

            # Sort Option
            header, body = body.panel(idname="sort_option", default_closed=True)
            header.label(text="Sort Option")
            if body:
                body.use_property_decorate = False
                body.use_property_split = True
                # body.active = props.sort_option_enabled
                box = body.box()
                box.row().prop(props, "sort_type")
                if props.sort_type != "DISTANCE":
                    box.row().prop(props, "sort_axis", text="Axis")
                box.row().prop(props, "sort_reverse_enabled")
                box.use_property_split = False
                box.row().prop(props, "use_sort_obj", icon="TRIA_DOWN" if props.use_sort_obj else "TRIA_RIGHT")
                if props.use_sort_obj:
                    box = box.box()
                    box.use_property_split = True
                    box.row().prop(props, "sort_origin")

        # layout.separator(type="LINE")

        # Apply
        layout.operator(
            "bouncer.apply_animation_operator", 
            icon="PREVIEW_RANGE", 
            text=bpy.app.translations.pgettext_iface("Apply Animation")
        )

        # Reset
        layout.operator(
            "bouncer.reset_properties_operator", 
            icon="FILE_REFRESH", 
            text=bpy.app.translations.pgettext_iface("Reset Properties")
        )
        
register_classes = [
    BouncerUiPanel
]
