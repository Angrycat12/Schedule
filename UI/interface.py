import dearpygui.dearpygui as dpg
import settings
import Schedule
import math


def print_me(sender):
    print(f"Menu Item: {sender}")

dpg.create_context()
dpg.create_viewport(title='Syllabus', min_width=settings.window_width, min_height=settings.window_height, resizable=True)

with dpg.viewport_menu_bar():
    with dpg.menu(label="File"):
        dpg.add_menu_item(label="Save", callback=print_me)
        dpg.add_menu_item(label="Save As", callback=print_me)
        dpg.add_menu_item(label="Open", callback=print_me)

    with dpg.menu(label="Settings"):
        dpg.add_menu_item(label="Setting 1", callback=print_me, check=True)
        dpg.add_menu_item(label="Setting 2", callback=print_me)

#with dpg.window(width=settings.window_width, height=settings.window_height,
               # no_collapse=True, no_resize=True, no_close=True, menubar=True, tag='main') as main_window:
    #pass

with dpg.window(width=settings.window_width, height=settings.window_height,
                no_collapse=True, no_resize=True, no_close=True, menubar=True, tag='Schedule') as main_menu_window:

    schedule = Schedule.generate()

    with dpg.table(header_row=False, policy=dpg.mvTable_SizingFixedFit, resizable=True, no_host_extendX=True,
                   borders_innerV=True, borders_outerV=True, borders_outerH=True):

        colum_num = 6

        for colum in range(colum_num):
            dpg.add_table_column(label=f"{colum}")

        num_week_i = 0
        num_week_j = 0
        print(len(schedule) // colum_num)
        for num_colum in range((len(schedule) // colum_num) * 2):
            if num_colum % 2 != 0:
                with dpg.table_row():
                    for week in range(0, math.ceil(num_colum / 2) * ((len(schedule) // colum_num) * 2)):
                        with dpg.table():
                            for day in range(1, len(schedule[week])):
                                dpg.add_table_column(label=f"day{day}")

                            for lesson in range(len(schedule[week][day])):
                                with dpg.table_row():
                                    for les in range(day):
                                        dpg.add_text(schedule[week][day][lesson])
                    num_week_i = week
                    print(num_week_i,"d")
            else:
                with dpg.table_row():
                    for week in range(0, colum_num):
                        dpg.add_text(f"week{week}")

                    num_week_j = week
                    print(num_week_j,"f")


dpg.set_primary_window(window=main_menu_window, value=True)

dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()