import customtkinter as ctk
from tkinter import filedialog, messagebox
import joblib
from .config import BG_MAIN, BG_CARD, BORDER, ACCENT, ACCENT_HOVER, TEXT_PRIMARY, TEXT_SECONDARY, FONT_FAMILY
from .widgets import SectionHeader

class About:

    def _build_about_page(self):
        page = ctk.CTkFrame(self.container, fg_color=BG_MAIN)
        self.pages["about"] = page
        SectionHeader(page, "About",
                      "Application information and model export."
                      ).pack(anchor="w", padx=24, pady=(24, 16))
        about_card = ctk.CTkFrame(page, fg_color=BG_CARD, corner_radius=16,
                                   border_width=1, border_color=BORDER)
        about_card.pack(fill="x", padx=24, pady=8)
        ctk.CTkLabel(about_card, text="About", font=(FONT_FAMILY, 13, "bold"),
                     text_color=TEXT_PRIMARY).pack(anchor="w", padx=20, pady=(18, 6))
        ctk.CTkLabel(about_card,
                     text="Churn Prediction Studio combines exploratory analysis,\n"
                          "dual-model training (Logistic Regression + Random Forest),\n"
                          "evaluation, and live prediction into a single desktop tool.",
                     font=(FONT_FAMILY, 12), text_color=TEXT_SECONDARY, justify="left"
                     ).pack(anchor="w", padx=20, pady=(0, 20))
        save_card = ctk.CTkFrame(page, fg_color=BG_CARD, corner_radius=16,
                                  border_width=1, border_color=BORDER)
        save_card.pack(fill="x", padx=24, pady=8)
        ctk.CTkLabel(save_card, text="Export", font=(FONT_FAMILY, 13, "bold"),
                     text_color=TEXT_PRIMARY).pack(anchor="w", padx=20, pady=(18, 6))
        ctk.CTkButton(save_card, image = self.save_icon, text="Save Best Model (.pkl)", command=self.save_model,
                      fg_color=ACCENT, hover_color=ACCENT_HOVER, height=38, corner_radius=10,
                      font=(FONT_FAMILY, 12, "bold")).pack(anchor="w", padx=20, pady=(0, 20))

    def save_model(self):

        if self.best_model is None:
            messagebox.showwarning("No Model", "Train the models first.")
            return
        path = filedialog.asksaveasfilename(
            title="Save Best Model", defaultextension=".pkl",
            filetypes=[("Pickle model", "*.pkl")])

        if not path:
            return

        try:
            joblib.dump(self.best_model, path)
            messagebox.showinfo("Model Saved", f"Model saved successfully:\n\n{path}")
            self.set_status("Model saved.")

        except Exception as e:
            messagebox.showerror("Save Error", str(e))
