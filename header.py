# Imports
from palette import *
from flet import (
    Container,
    Row,
    Text,
    IconButton,
    icons,
    TextField,
    TextStyle,
    AppBar,
    MainAxisAlignment,
    ButtonStyle,
    VerticalDivider,
    Icon,
    Page,
)
from datetime import datetime
from time import sleep
from threading import Thread

hdr_btn_style = {
    "icon_color": scndry_clr,
    "icon_size": 42,
    "scale": 0.6,
    "style": ButtonStyle(elevation=1, shadow_color="#9CA1BE"),
    "highlight_color": "#F6B17A",
}

class Header:
    def __init__(self, system_name, module_name, user_name,on_logout=callable,on_changeUsr=callable,on_changePWD=callable,on_notif=callable, page= Page):
        self.system_name = system_name
        self.module_name = module_name
        self.user_name = user_name
        self.time_text = Text("", color="white", text_align="center")
        self.page = page  # This will be set when creating the header

    def get_app_bar(self):
        return AppBar(
            bgcolor=prim_clr,
            center_title=True,
            toolbar_height=60,
            title=Row(
                controls=[
                    Text(f"{self.system_name} - {self.module_name}", size=20, text_align=MainAxisAlignment.START, color="white")
                ],
                alignment=MainAxisAlignment.START,
            ),
            actions=[
                Row(
                    controls=[
                        Container(
                            content=Row(
                                controls=[
                                    Icon(icons.SEARCH, color=scndry_clr),
                                    TextField(
                                        label="البحث",
                                        label_style=TextStyle(size=14, color=scndry_clr),
                                        border_color="white",
                                        border_radius=30,
                                        height=35,
                                        cursor_color=scndry_clr,
                                        cursor_height=13,
                                        text_size=14,
                                        text_style=TextStyle(size=14, color=scndry_clr),
                                    ),
                                ],
                                vertical_alignment=MainAxisAlignment.CENTER,
                            ),
                            width=400,
                        ),
                        VerticalDivider(10, 1, fade_clr),
                        self.time_text,
                        VerticalDivider(1, 1, fade_clr),
                        Text(self.user_name, color="white"),
                        IconButton(icon=icons.ACCOUNT_CIRCLE, icon_color="white"),
                        VerticalDivider(1, 1, fade_clr),
                        IconButton(icon=icons.NOTIFICATIONS, icon_color="white"),
                        IconButton(icon=icons.VPN_KEY, icon_color="white"),
                        IconButton(icon=icons.REFRESH_OUTLINED, icon_color="white"),
                        IconButton(icon=icons.LOGOUT, icon_color="white"),
                    ],
                    alignment=MainAxisAlignment.START,
                )
            ],
        )

    def update_time(self):
        self.time_text.value = datetime.now().strftime("%H:%M:%S")
        self.page.update()

    def update_clock(self):
        while True:
            self.update_time()
            sleep(1)

    def start_clock_thread(self):
        clock_thread = Thread(target=self.update_clock, daemon=True)
        clock_thread.start()


# Test
# def main(page: Page):
#     page.window_maximized = True
#     page.title = "قالب"
#     page.theme_mode = "Light"
#     page.rtl = True
#     page.theme = Theme(font_family="Lalezar")
    
#     header = Header("إدارة المدخلات", "بيانات الموظفين", "مدير النظام",page)
#     page.appbar = header.get_container()
#     page.update()

#     # def update_clock():
#     #     while True:
#     #         header.update_time()
#     #         sleep(1)

#     # clock_thread = Thread(target=update_clock, daemon=True)
#     # clock_thread.start()



# app(target=main)
