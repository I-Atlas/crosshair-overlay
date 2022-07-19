import json
import os.path
import tkinter as tk
import multiprocessing
import dearpygui.dearpygui as dpg
from dearpygui_ext.themes import create_theme_imgui_light, create_theme_imgui_dark
import overlay
import darkdetect

p = multiprocessing.Process()


def _get_theme():
    light_theme = create_theme_imgui_light()
    dark_theme = create_theme_imgui_dark()
    if darkdetect.isDark():
        return dark_theme
    else:
        return light_theme


def ui_loop(ww=1920, wh=1080):
    dpg.create_context()

    with dpg.window(tag="Primary Window"):
        with dpg.menu_bar():
            with dpg.menu(label="Menu"):
                with dpg.file_dialog(label="File Open", width=400, height=300, show=False,
                                     callback=_open_settings, tag="__file_open"):
                    dpg.add_file_extension(".json", color=(255, 255, 255, 255))
                dpg.add_menu_item(label="Open", user_data=dpg.last_container(),
                                  callback=lambda s, a, u: dpg.configure_item(u, show=True))

                with dpg.file_dialog(label="File Save", width=400, height=300, show=False,
                                     callback=_save_settings, tag="__file_save"):
                    dpg.add_file_extension(".json", color=(255, 255, 255, 255))
                dpg.add_menu_item(label="Save", user_data=dpg.last_container(),
                                  callback=lambda s, a, u: dpg.configure_item(u, show=True))

        dpg.add_color_edit((255, 255, 255, 255), label="Color", no_alpha=True, callback=_set_values,
                           tag="color")

        dpg.add_checkbox(label="Crosshair", default_value=True, callback=_set_values, tag="is_crosshair")
        dpg.add_checkbox(label="Center Dot", callback=_set_values, tag="is_center_dot")
        dpg.add_checkbox(label="Outline", callback=_set_values, tag="is_outline")

        dpg.add_input_int(label="Size", default_value=4, callback=_set_values, tag="size")
        dpg.add_input_int(label="Width", default_value=1, callback=_set_values, tag="width")
        dpg.add_input_int(label="Center distance", default_value=2, callback=_set_values, tag="distance")
        dpg.add_input_int(label="Offset X", callback=_set_values, min_value=int(-ww / 2),
                          max_value=int(ww / 2),
                          min_clamped=True, max_clamped=True, tag="offset_x")
        dpg.add_input_int(label="Offset Y", callback=_set_values, min_value=int(-wh / 2),
                          max_value=int(wh / 2),
                          min_clamped=True, max_clamped=True,
                          tag="offset_y")

        with dpg.group(label="Buttons", tag="start_stop_buttons", horizontal=True):
            dpg.add_button(label="Reset settings", callback=_reset)
            dpg.add_button(label="Open overlay", callback=_start)
            dpg.add_button(label="Close overlay", callback=_stop)

    theme = _get_theme()
    dpg.bind_theme(theme)

    dpg.create_viewport(title='Crosshair Overlay', width=1280, height=720)
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.set_primary_window("Primary Window", True)
    dpg.start_dearpygui()
    dpg.destroy_context()


def _crosshair_overlay(size=4, width=1, distance=2, color_r=255, color_g=255, color_b=255, is_outline=False,
                       is_center_dot=False, is_crosshair=True, offset_x=0, offset_y=0):
    overlay.CrosshairOverlay(size=size, width=width, distance=distance, color_r=color_r, color_g=color_g,
                             color_b=color_b,
                             is_outline=is_outline,
                             is_center_dot=is_center_dot, is_crosshair=is_crosshair, offset_x=offset_x,
                             offset_y=offset_y).mainloop()


def _set_values():
    if p.is_alive():
        _start()


def _start():
    global p
    if p.is_alive():
        p.kill()
        p.join()
    p = multiprocessing.Process(target=_crosshair_overlay, kwargs=_get_values(), daemon=True)
    p.start()


def _stop():
    if p.is_alive():
        p.kill()
        p.join()


def _get_values():
    r, g, b = list(map(int, dpg.get_value("color")[:3]))
    return {"size": dpg.get_value("size"), "width": dpg.get_value("width"), "distance": dpg.get_value("distance"),
            "color_r": r,
            "color_g": g, "color_b": b, "is_outline": dpg.get_value("is_outline"),
            "is_center_dot": dpg.get_value("is_center_dot"), "is_crosshair": dpg.get_value("is_crosshair"),
            "offset_x": dpg.get_value("offset_x"),
            "offset_y": -dpg.get_value("offset_y")}


def _reset():
    dpg.set_value("color", (255, 255, 255, 255))
    dpg.set_value("is_outline", False)
    dpg.set_value("is_center_dot", False)
    dpg.set_value("is_crosshair", True)
    dpg.set_value("size", 4)
    dpg.set_value("width", 1)
    dpg.set_value("distance", 2)
    dpg.set_value("offset_x", 0)
    dpg.set_value("offset_y", 0)
    _set_values()


def _open_settings(sender, app_data):
    if os.path.isfile(app_data["file_path_name"]):
        with open(app_data["file_path_name"], "r") as fp:
            data = json.load(fp)
            dpg.set_value("color", (data["color_r"], data["color_g"], data["color_b"], 255))
            dpg.set_value("is_outline", data["is_outline"])
            dpg.set_value("is_center_dot", data["is_center_dot"])
            dpg.set_value("is_crosshair", data["is_crosshair"])
            dpg.set_value("size", data["size"])
            dpg.set_value("width", data["width"])
            dpg.set_value("distance", data["distance"])
            dpg.set_value("offset_x", data["offset_x"])
            dpg.set_value("offset_y", data["offset_y"])
            _set_values()


def _save_settings(sender, app_data):
    with open(app_data["file_path_name"], "w") as fp:
        json.dump(_get_values(), fp)


if __name__ == '__main__':
    multiprocessing.freeze_support()
    root = tk.Tk()
    ww = root.winfo_screenwidth()
    wh = root.winfo_screenheight()
    root.destroy()
    ui_loop(ww=ww, wh=wh)
