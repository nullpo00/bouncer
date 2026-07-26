# SPDX-License-Identifier: GPL-3.0-or-later

# ruff: noqa: E402

bl_info = {
    "name" : "Bouncer",
    "author" : "NullPo",
    "version" : (1, 0, 0),
    "blender" : (5, 0, 0),
    "location" : "N-Panel",
    "description" : "Easily make a bounce animation",
    "warning" : "Work in progress",
    "category" : "Animation"
}

import importlib
import sys

MODULES = [
    ".operators",
    ".properties",
    ".ui"
]

if "bpy" in locals():
    for module in MODULES:
        if __package__ + module in sys.modules:
            importlib.reload(sys.modules[__package__ + module])
else:
    import bpy
    for module in MODULES:
        importlib.import_module(name=module, package=__package__)


# 日本語翻訳用
translation_dict = {
    "ja_JP": {
        ("*", "Animation Settings"): "アニメーション設定",
        ("*", "Use Current Frame"): "現在のフレームを使用",
        ("BouncerPanel", "Amplitude"): "振幅",
        ("BouncerPanel", "Period"): "周期",
        ("BouncerPanel", "Frequency"): "周波数",
        ("*", "Apply Animation"): "アニメーションを適用",
        ("*", "Reset Properties"): "プロパティをリセット"
    }
}

def register():
    bpy.app.translations.register(__name__, translation_dict)

    for module in MODULES:
        mod = sys.modules[__package__ + module]
        if hasattr(mod, "register_classes"):
            for cls in mod.register_classes:
                bpy.utils.register_class(cls)
                
            if hasattr(mod, "construct_pointer_property"):
                mod.construct_pointer_property()

def unregister():
    bpy.app.translations.unregister(__name__)

    for module in MODULES:
        mod = sys.modules[__package__ + module]
        if hasattr(mod, "register_classes"):
            for cls in mod.register_classes:
                bpy.utils.unregister_class(cls)

            if hasattr(mod, "delete_pointer_property"):
                mod.delete_pointer_property()


if __name__ == "__main__":
    register()
