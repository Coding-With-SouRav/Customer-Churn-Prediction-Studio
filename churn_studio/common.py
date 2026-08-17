from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from .config import (
    BG_MAIN, BG_SIDEBAR, BG_CARD, BG_CARD_ALT,
    BORDER, ACCENT_SOFT, TEXT_PRIMARY, TEXT_SECONDARY, FONT_FAMILY,
)

def fmt_pct(value):
    return f"{value * 100:.1f}%"

def make_mpl_canvas(parent, figsize=(5, 3.4), dpi=100):
    fig = Figure(figsize=figsize, dpi=dpi, facecolor=BG_CARD)
    canvas = FigureCanvasTkAgg(fig, master=parent)
    canvas.get_tk_widget().configure(bg=BG_CARD, highlightthickness=0)
    return fig, canvas

def style_dark_treeview():
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Premium.Treeview",
                     background=BG_CARD_ALT, fieldbackground=BG_CARD_ALT,
                     foreground=TEXT_PRIMARY, bordercolor=BORDER,
                     borderwidth=0, rowheight=26,
                     font=(FONT_FAMILY, 10))
    style.configure("Premium.Treeview.Heading",
                     background=BG_SIDEBAR, foreground=TEXT_SECONDARY,
                     font=(FONT_FAMILY, 10, "bold"), relief="flat", borderwidth=0)
    style.map("Premium.Treeview.Heading", background=[("active", BG_SIDEBAR)])
    style.map("Premium.Treeview",
              background=[("selected", ACCENT_SOFT)],
              foreground=[("selected", TEXT_PRIMARY)])
    style.configure("Premium.Vertical.TScrollbar", background=BG_SIDEBAR,
                     troughcolor=BG_MAIN, bordercolor=BG_MAIN, arrowcolor=TEXT_SECONDARY)
