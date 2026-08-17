import configparser
import ctypes
import os
import sys
import queue
import customtkinter as ctk
from .config import BG_MAIN
from .common import style_dark_treeview
from .icon import draw_icon
from .window import Window
from .dashboard import Dashboard
from .dataset import Dataset
from .training import Training
from .evaluation import Evaluation
from .prediction import Prediction
from .about import About

class ChurnStudio(
    Window,
    Dashboard,
    Dataset,
    Training,
    Evaluation,
    Prediction,
    About,
    ctk.CTk,
):

    def __init__(self):
        super().__init__()
        self.title("Churn Prediction Studio")
        self.geometry("1180x720")
        self.minsize(1180, 720)
        self.configure(fg_color=BG_MAIN)

        if sys.platform == "win32":
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("com.example.CHURNPrediction")
        self.data_dir = os.path.join(os.path.expanduser("~"), ".CustomerCharn")
        os.makedirs(self.data_dir, exist_ok=True)
        self.config_file = os.path.join(self.data_dir, 'config.ini')
        style_dark_treeview()
        self.df = None
        self.csv_path = None
        self.X_train = self.X_test = self.y_train = self.y_test = None
        self.numeric_features = []
        self.categorical_features = []
        self.category_options = {}
        self.logistic_model = None
        self.rf_model = None
        self.best_model = None
        self.best_model_name = None
        self.metrics_lr = {}
        self.metrics_rf = {}
        self.results_df = None
        self.current_sample = None
        self.manual_inputs = {}
        self.DWMWA_BORDER_COLOR = 34
        self.DWMWA_CAPTION_COLOR = 35
        self.DWMWA_TEXT_COLOR = 36
        self.DWMWA_USE_IMMERSIVE_DARK_MODE = 20
        hwnd = ctypes.windll.user32.GetParent(self.winfo_id())
        self.log_queue = queue.Queue()
        self.load_images()
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.pages = {}
        self.nav_buttons = {}
        self._build_sidebar()
        self.container = ctk.CTkFrame(self, fg_color=BG_MAIN)
        self.container.grid(row=0, column=1, sticky="nsew")
        self.container.grid_columnconfigure(0, weight=1)
        self.container.grid_rowconfigure(0, weight=1)
        self.set_titlebar_color(hwnd, (0, 0, 0))
        self.set_text_color(hwnd, (255, 255, 255))
        self._build_dashboard_page()
        self._build_dataset_page()
        self._build_training_page()
        self._build_evaluation_page()
        self._build_prediction_page()
        self._build_about_page()
        self.show_page("dashboard")
        self.after(150, self._poll_log_queue)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.load_window_geometry()

def main():
    app = ChurnStudio()
    draw_icon(app)
    app.mainloop()

if __name__ == "__main__":
    main()
