import configparser
import ctypes
import os
import sys
import customtkinter as ctk
import tkinter as tk
from PIL import Image
from .config import (
    BG_SIDEBAR, BG_CARD, BG_CARD_ALT, ACCENT, FONT_FAMILY,
    TEXT_PRIMARY, TEXT_MUTED, TEXT_SECONDARY,
)
from .widgets import NavButton

class Window:

    def load_window_geometry(self):

        if os.path.exists(self.config_file):
            config = configparser.ConfigParser()
            config.read(self.config_file)

            if "Geometry" in config:
                geometry = config["Geometry"].get("size", "")
                state = config["Geometry"].get("state", "normal")

                if geometry:
                    self.geometry(geometry)
                    self.update_idletasks()
                    self.update()

                if state == "zoomed":
                    self.state("zoomed")
                elif state == "iconic":
                    self.iconify()

    def save_window_geometry(self):
        config = configparser.ConfigParser()
        config["Geometry"] = {
            "size": self.geometry(),
            "state": self.state()
        }

        with open(self.config_file, "w") as f:
            config.write(f)

    def on_closing(self):
        self.save_window_geometry()
        self.destroy()

    def set_titlebar_color(self, hwnd, color):
        r = color[0]
        g = color[1]
        b = color[2]
        rgb = b << 16 | g << 8 | r
        ctypes.windll.dwmapi.DwmSetWindowAttribute(
            hwnd,
            self.DWMWA_CAPTION_COLOR,
            ctypes.byref(ctypes.c_int(rgb)),
            ctypes.sizeof(ctypes.c_int)
        )

    def set_text_color(self, hwnd, color):
        r, g, b = color
        rgb = b << 16 | g << 8 | r
        ctypes.windll.dwmapi.DwmSetWindowAttribute(
            hwnd,
            self.DWMWA_TEXT_COLOR,
            ctypes.byref(ctypes.c_int(rgb)),
            ctypes.sizeof(ctypes.c_int)
        )

    def resource_path(self, relative_path):

        try:
            base_path = sys._MEIPASS

        except Exception:
            base_path = os.path.abspath(".")

        if 'icons' in relative_path:
            full_path = os.path.join(base_path, relative_path.replace('\\', os.sep))
        else:
            full_path = os.path.join(base_path, relative_path)

        if not os.path.exists(full_path):
            raise FileNotFoundError(f"Resource not found: {full_path}")
        return full_path

    def load_images(self):
        dashboard_img = Image.open(self.resource_path(r"assets\dashboard.png"))
        dataset_img   = Image.open(self.resource_path(r"assets\dataset.png"))
        training_img  = Image.open(self.resource_path(r"assets\training.png"))
        evaluation_img= Image.open(self.resource_path(r"assets\evaluation.png"))
        prediction_img= Image.open(self.resource_path(r"assets\prediction.png"))
        about_img     = Image.open(self.resource_path(r"assets\about.png"))
        customers_img = Image.open(self.resource_path(r"assets\customers.png"))
        features_img = Image.open(self.resource_path(r"assets\features.png"))
        rate_img = Image.open(self.resource_path(r"assets\rate.png"))
        model_img = Image.open(self.resource_path(r"assets\model.png"))
        load_img = Image.open(self.resource_path(r"assets\load.png"))
        train_model_img = Image.open(self.resource_path(r"assets\train_model.png"))
        refresh_img = Image.open(self.resource_path(r"assets\refresh.png"))
        best_img = Image.open(self.resource_path(r"assets\best.png"))
        random_img = Image.open(self.resource_path(r"assets\random.png"))
        save_img = Image.open(self.resource_path(r"assets\save.png"))
        studio_img = Image.open(self.resource_path(r"assets\studio.png"))
        
        self.dashboard_icon  = ctk.CTkImage(light_image=dashboard_img, dark_image=dashboard_img, size=(20, 20))
        self.dataset_icon    = ctk.CTkImage(light_image=dataset_img,   dark_image=dataset_img,   size=(20, 20))
        self.training_icon   = ctk.CTkImage(light_image=training_img,  dark_image=training_img,  size=(20, 20))
        self.evaluation_icon = ctk.CTkImage(light_image=evaluation_img,dark_image=evaluation_img, size=(25, 25))
        self.prediction_icon = ctk.CTkImage(light_image=prediction_img,dark_image=prediction_img, size=(25, 25))
        self.about_icon      = ctk.CTkImage(light_image=about_img,     dark_image=about_img,      size=(20, 20))
        self.customers_icon  = ctk.CTkImage(light_image=customers_img, dark_image=customers_img,  size=(30, 30))
        self.features_icon   = ctk.CTkImage(light_image=features_img,  dark_image=features_img,   size=(30, 30))
        self.rate_icon       = ctk.CTkImage(light_image=rate_img,  dark_image=rate_img,   size=(30, 30))
        self.model_icon      = ctk.CTkImage(light_image=model_img,  dark_image=model_img,   size=(30, 30))
        self.load_icon       = ctk.CTkImage(light_image=load_img,  dark_image=load_img,   size=(20, 20))
        self.train_model_icon = ctk.CTkImage(light_image=train_model_img,  dark_image=train_model_img,   size=(20, 20))
        self.refresh_icon     = ctk.CTkImage(light_image=refresh_img,  dark_image=refresh_img,   size=(20, 20))
        self.best_icon        = ctk.CTkImage(light_image=best_img,  dark_image=best_img,   size=(30, 30))
        self.random_icon      = ctk.CTkImage(light_image=random_img,  dark_image=random_img,   size=(25, 25))
        self.save_icon        = ctk.CTkImage(light_image=save_img,  dark_image=save_img,   size=(25, 25))
        self.studio_icon        = ctk.CTkImage(light_image=studio_img,  dark_image=studio_img,   size=(40, 40))

    def _build_sidebar(self):
        sidebar = ctk.CTkFrame(self, width=250, fg_color=BG_SIDEBAR, corner_radius=0)
        sidebar.grid(row=0, column=0, sticky="nsw")
        sidebar.grid_propagate(False)
        sidebar.grid_rowconfigure(6, weight=1)
        brand = ctk.CTkFrame(sidebar, fg_color="transparent")
        brand.grid(row=0, column=0, sticky="ew", padx=20, pady=(26, 22))
        title_box = ctk.CTkFrame(brand, fg_color="transparent")
        title_box.pack(side="left", padx=(10, 0))
        ctk.CTkLabel(title_box,image=self.studio_icon, compound="left", text="  CHURN STUDIO", font=(FONT_FAMILY, 15, "bold"),
                     text_color=TEXT_PRIMARY).pack(anchor="w")
        ctk.CTkLabel(title_box, text="Predictive Retention Suite", font=(FONT_FAMILY, 10),
                     text_color=TEXT_MUTED).pack(anchor="w")
        nav_items = [
            ("dashboard", self.dashboard_icon, "Dashboard"),
            ("training", self.training_icon, "Model Training"),
            ("dataset", self.dataset_icon, "Dataset & EDA"),
            ("evaluation", self.evaluation_icon, "Evaluation"),
            ("prediction", self.prediction_icon, "Prediction"),
            ("about", self.about_icon, "About"),
        ]
        for i, (key, icon, label) in enumerate(nav_items, start=1):
            btn = NavButton(sidebar, icon, label, command=lambda k=key: self.show_page(k))
            btn.grid(row=i, column=0, sticky="ew", padx=14, pady=3)
            self.nav_buttons[key] = btn
        footer = ctk.CTkFrame(sidebar, fg_color=BG_CARD, corner_radius=14)
        footer.grid(row=7, column=0, sticky="ew", padx=14, pady=16)
        ctk.CTkLabel(footer, text="STATUS", font=(FONT_FAMILY, 10, "bold"),
                     text_color=TEXT_MUTED).pack(anchor="w", padx=14, pady=(12, 0))
        self.status_var = tk.StringVar(value="Ready")
        ctk.CTkLabel(footer, textvariable=self.status_var, font=(FONT_FAMILY, 11),
                     text_color=TEXT_SECONDARY, wraplength=190, justify="left"
                     ).pack(anchor="w", padx=14, pady=(2, 12))
        self.sidebar_progress = ctk.CTkProgressBar(footer, height=6, progress_color=ACCENT,
                                                     fg_color=BG_CARD_ALT)
        self.sidebar_progress.set(0)
        self.sidebar_progress.pack(fill="x", padx=14, pady=(0, 14))

    def show_page(self, key):
        for name, btn in self.nav_buttons.items():
            btn.set_active(name == key)
        for name, page in self.pages.items():

            if name == key:
                page.grid(row=0, column=0, sticky="nsew")
            else:
                page.grid_remove()

    def set_status(self, text):
        self.status_var.set(text)
