import customtkinter as ctk
from .config import (
    BG_CARD, BG_CARD_ALT, BORDER, BG_HOVER, ACCENT, ACCENT_SOFT,
    TEXT_PRIMARY, TEXT_SECONDARY, TEXT_MUTED, FONT_FAMILY,
)

class StatCard(ctk.CTkFrame):

    def __init__(self, parent, icon, title, accent=ACCENT, image=None, **kwargs):
        super().__init__(parent, fg_color=BG_CARD, corner_radius=16,
                          border_width=1, border_color=BORDER, **kwargs)
        self.grid_columnconfigure(0, weight=1)
        top = ctk.CTkFrame(self, fg_color="transparent")
        top.grid(row=0, column=0, sticky="ew", padx=18, pady=(16, 0))
        top.grid_columnconfigure(1, weight=1)

        if image is not None:
            badge = ctk.CTkLabel(top, image=image, text="",
                                 fg_color=BG_CARD_ALT, width=34, height=34, corner_radius=10)
        else:
            badge = ctk.CTkLabel(top, text=icon, font=(FONT_FAMILY, 16),
                                 fg_color=BG_CARD_ALT,
                                 text_color=accent, width=34, height=34, corner_radius=10)
        badge.grid(row=0, column=0, sticky="w")
        ctk.CTkLabel(top, text=title.upper(), font=(FONT_FAMILY, 11, "bold"),
                     text_color=TEXT_MUTED).grid(row=0, column=1, sticky="e")
        self.value_label = ctk.CTkLabel(self, text="—", font=(FONT_FAMILY, 26, "bold"),
                                         text_color=TEXT_PRIMARY, anchor="w")
        self.value_label.grid(row=1, column=0, sticky="ew", padx=18, pady=(6, 18))

    def set_value(self, text):
        self.value_label.configure(text=text)

class SectionHeader(ctk.CTkFrame):

    def __init__(self, parent, title, subtitle):
        super().__init__(parent, fg_color="transparent")
        ctk.CTkLabel(self, text=title, font=(FONT_FAMILY, 24, "bold"),
                     text_color=TEXT_PRIMARY).pack(anchor="w")
        ctk.CTkLabel(self, text=subtitle, font=(FONT_FAMILY, 12),
                     text_color=TEXT_SECONDARY).pack(anchor="w", pady=(2, 0))

class Pill(ctk.CTkLabel):

    def __init__(self, parent, text, color=ACCENT):
        super().__init__(parent, text=text, font=(FONT_FAMILY, 11, "bold"),
                          text_color=color, fg_color=BG_CARD_ALT,
                          corner_radius=999, width=10, height=24, padx=12)

class NavButton(ctk.CTkButton):

    def __init__(self, parent, icon_image, label, command):
        super().__init__(
            parent,
            image=icon_image,
            text=label,
            command=command,
            anchor="w",
            font=(FONT_FAMILY, 13),
            height=42,
            corner_radius=10,
            fg_color="transparent",
            hover_color=BG_HOVER,
            text_color=TEXT_SECONDARY,
            compound="left"
        )

    def set_active(self, active):

        if active:
            self.configure(fg_color=ACCENT_SOFT, text_color=TEXT_PRIMARY)
        else:
            self.configure(fg_color="transparent", text_color=TEXT_SECONDARY)
