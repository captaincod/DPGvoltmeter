import random

import dearpygui.dearpygui as dpg
import numpy as np

dpg.create_context()
dpg.create_viewport(title='Funny Friendly Voltmeter With Kittens', min_width=700, max_width=700, min_height=400, max_height=400)
dpg.setup_dearpygui()
dpg.show_viewport()

with dpg.texture_registry():
    for i in range(1, 8):
        width, height, channels, data = dpg.load_image(f"src/kitten{i}.png")
        kitten_tag = f"kitten{i}"
        dpg.add_static_texture(width=width, height=height, default_value=data, tag=kitten_tag)

with dpg.font_registry():
    with dpg.font(r"src/minecraft.ttf", 20, default_font=True) as default_font:
        dpg.add_font_range_hint(dpg.mvFontRangeHint_Cyrillic)
    with dpg.font(r"src/minecraft.ttf", 36, default_font=True) as header_font:
        dpg.add_font_range_hint(dpg.mvFontRangeHint_Cyrillic)
    with dpg.font(r"src/minecraft.ttf", 12, default_font=True) as secondary_font:
        dpg.add_font_range_hint(dpg.mvFontRangeHint_Cyrillic)

gauss_distr = []
last_values = []

def show_avg():
    value = int(dpg.get_value("slider"))
    avg = 0
    if value > len(last_values):
        value = len(last_values)
    for i in range(value):
        avg += last_values[i]
    if value == 0:
        dpg.set_value("average", "Секунду :)")
    else:
        str_avg = "%.2f" % (avg / value)
        dpg.set_value("average", f"Среднее за {value} сек: {str_avg}V")
    current_kitten = int(dpg.get_item_configuration("btn_image")["texture_tag"][-1])
    new_kitten = current_kitten
    while new_kitten == current_kitten:
        new_kitten = random.randint(1, 7)
    dpg.configure_item("btn_image", texture_tag=f"kitten{new_kitten}")


with dpg.window(width=700, height=500, tag="Primary Window"):
    dpg.bind_font(default_font)
    dpg.add_text("Текущее напряжение")
    dpg.add_text(tag="voltage", default_value="??.??V")
    dpg.bind_item_font("voltage", header_font)
    dpg.add_text("")
    with dpg.group(horizontal=True):
        dpg.add_text("Период в секундах: ")
        dpg.add_slider_int(tag="slider", default_value=10, width=300, min_value=3, max_value=30)
    dpg.add_image_button(tag="btn_image", texture_tag="kitten1", width=200, height=120, background_color=(255, 230, 204),
                         callback=show_avg)
    with dpg.tooltip("btn_image"):
        dpg.add_text(tag="btn_label", default_value="Показать среднее за период")
        dpg.bind_item_font("btn_label", secondary_font)
    dpg.add_text(tag="average")
dpg.set_primary_window("Primary Window", True)

with dpg.theme() as global_theme:
    with dpg.theme_component(dpg.mvAll):
        dpg.add_theme_style(dpg.mvStyleVar_WindowPadding, 20, 20)
        dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 7)
        dpg.add_theme_style(dpg.mvStyleVar_ItemSpacing, 12, 7)
        dpg.add_theme_style(dpg.mvStyleVar_GrabRounding, 10)
        dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (147, 85, 255))
        dpg.add_theme_color(dpg.mvThemeCol_FrameBg, (255, 156, 0))
        dpg.add_theme_color(dpg.mvThemeCol_FrameBgHovered, (255, 120, 0))
        dpg.add_theme_color(dpg.mvThemeCol_FrameBgActive, (255, 120, 0))
        dpg.add_theme_color(dpg.mvThemeCol_SliderGrab, (255, 255, 255, 100))
        dpg.add_theme_color(dpg.mvThemeCol_SliderGrabActive, (255, 255, 255, 150))
        dpg.add_theme_color(dpg.mvThemeCol_Button, (255, 156, 0))
        dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (255, 120, 0))
        dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (255, 120, 0, 150))
dpg.bind_theme(global_theme)

while dpg.is_dearpygui_running():
    a = 25 + np.random.randn()
    a += 10 * np.random.randn()
    gauss_distr.append(a)
    if len(gauss_distr) % 60 == 0:
        last_values.insert(0, a)
        str_voltage = "%.2f" % a
        dpg.set_value("voltage", str_voltage+"V")
    if len(gauss_distr) > 1800:
        gauss_distr = []
        last_values = [last_values[i] for i in range(30)]
    dpg.render_dearpygui_frame()

dpg.start_dearpygui()
dpg.destroy_context()
