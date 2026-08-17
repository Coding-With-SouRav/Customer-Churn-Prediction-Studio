import customtkinter as ctk
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import seaborn as sns
BG_MAIN        = "#0A0D14"
BG_SIDEBAR     = "#0E1119"
BG_CARD        = "#151926"
BG_CARD_ALT    = "#1B2030"
BG_HOVER       = "#20263A"
BORDER         = "#242B3D"
ACCENT         = "#7C5CFC"
ACCENT_HOVER   = "#9078FF"
ACCENT_SOFT    = "#241E42"
GOLD           = "#F0B94D"
SUCCESS        = "#33D69F"
DANGER         = "#FF6B6B"
TEXT_PRIMARY   = "#F3F4F8"
TEXT_SECONDARY = "#8A93AB"
TEXT_MUTED     = "#5B6377"
FONT_FAMILY    = "Segoe UI"
PALETTE = [ACCENT, GOLD]

def apply_global_theme():
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")
    ctk.CTk._windows_set_titlebar_icon = lambda self: None
    plt.rcParams.update({
        "figure.facecolor": BG_CARD,
        "axes.facecolor": BG_CARD,
        "axes.edgecolor": BORDER,
        "axes.labelcolor": TEXT_PRIMARY,
        "xtick.color": TEXT_SECONDARY,
        "ytick.color": TEXT_SECONDARY,
        "text.color": TEXT_PRIMARY,
        "grid.color": BORDER,
        "savefig.facecolor": BG_CARD,
        "font.family": "sans-serif",
    })
    sns.set_style("darkgrid", {
        "axes.facecolor": BG_CARD,
        "figure.facecolor": BG_CARD,
        "grid.color": BORDER,
    })
apply_global_theme()
