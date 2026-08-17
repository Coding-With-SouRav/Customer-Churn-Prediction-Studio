import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import numpy as np
import pandas as pd
from .config import (
    BG_MAIN, BG_CARD, BG_CARD_ALT, BG_HOVER, BORDER,
    ACCENT, ACCENT_HOVER, DANGER, SUCCESS,
    TEXT_PRIMARY, TEXT_SECONDARY, TEXT_MUTED, FONT_FAMILY,
)
from .widgets import SectionHeader

class Prediction:

    def _build_prediction_page(self):
        page = ctk.CTkScrollableFrame(self.container, fg_color=BG_MAIN)
        page.grid_columnconfigure(0, weight=1)
        self.pages["prediction"] = page
        SectionHeader(page, "Prediction",
                      "Predict churn risk from a random test customer or your own inputs."
                      ).grid(row=0, column=0, sticky="ew", padx=24, pady=(24, 12))
        self.pred_mode = ctk.CTkSegmentedButton(
            page, values=["Sample Customer", "Manual Entry"],
            command=self._on_pred_mode_change, fg_color=BG_CARD_ALT,
            selected_color=ACCENT, selected_hover_color=ACCENT_HOVER,
            unselected_color=BG_CARD_ALT, text_color=TEXT_PRIMARY)
        self.pred_mode.set("Sample Customer")
        self.pred_mode.grid(row=1, column=0, sticky="w", padx=24, pady=(0, 16))
        self.sample_panel = ctk.CTkFrame(page, fg_color=BG_CARD, corner_radius=16,
                                          border_width=1, border_color=BORDER)
        self.sample_panel.grid(row=2, column=0, sticky="ew", padx=24, pady=8)
        row = ctk.CTkFrame(self.sample_panel, fg_color="transparent")
        row.pack(fill="x", padx=20, pady=16)
        ctk.CTkButton(row, image = self.random_icon, text="Pick Random Test Customer", command=self.get_sample_customer,
                      fg_color=BG_CARD_ALT, hover_color=BG_HOVER, height=38,
                      corner_radius=10, font=(FONT_FAMILY, 12, "bold"),
                      text_color=TEXT_PRIMARY).pack(side="left")
        self.sample_predict_btn = ctk.CTkButton(
            row, image = self.prediction_icon, text="Predict", command=self.predict_sample_customer,
            fg_color=ACCENT, hover_color=ACCENT_HOVER, height=38, corner_radius=10,
            font=(FONT_FAMILY, 12, "bold"), state="disabled")
        self.sample_predict_btn.pack(side="left", padx=10)
        self.sample_text = ctk.CTkTextbox(self.sample_panel, height=140, fg_color=BG_CARD_ALT,
                                           text_color=TEXT_SECONDARY, font=("Consolas", 10),
                                           corner_radius=10)
        self.sample_text.pack(fill="x", padx=20, pady=(0, 18))
        self.sample_text.insert("end", "Click 'Pick Random Test Customer' after training models.")
        self.sample_text.configure(state="disabled")
        self.manual_panel = ctk.CTkFrame(page, fg_color=BG_CARD, corner_radius=16,
                                          border_width=1, border_color=BORDER)
        ctk.CTkLabel(self.manual_panel, text="Enter customer feature values",
                     font=(FONT_FAMILY, 12), text_color=TEXT_SECONDARY
                     ).pack(anchor="w", padx=20, pady=(16, 4))
        self.manual_form_scroll = ctk.CTkScrollableFrame(
            self.manual_panel, fg_color="transparent", height=320)
        self.manual_form_scroll.pack(fill="x", padx=20, pady=8)
        self.manual_form_scroll.grid_columnconfigure((0, 1), weight=1)
        self.manual_predict_btn = ctk.CTkButton(
            self.manual_panel, image = self.prediction_icon, text="Predict", command=self.predict_manual_entry,
            fg_color=ACCENT, hover_color=ACCENT_HOVER, height=38, corner_radius=10,
            font=(FONT_FAMILY, 12, "bold"), state="disabled")
        self.manual_predict_btn.pack(anchor="w", padx=20, pady=(0, 18))
        self.result_card = ctk.CTkFrame(page, fg_color=BG_CARD, corner_radius=16,
                                         border_width=1, border_color=BORDER)
        self.result_card.grid(row=3, column=0, sticky="ew", padx=24, pady=(8, 24))
        ctk.CTkLabel(self.result_card, text="Prediction Result", font=(FONT_FAMILY, 13, "bold"),
                     text_color=TEXT_PRIMARY).pack(anchor="w", padx=20, pady=(16, 8))
        self.result_title = ctk.CTkLabel(self.result_card, text="No prediction yet",
                                          font=(FONT_FAMILY, 22, "bold"), text_color=TEXT_SECONDARY)
        self.result_title.pack(anchor="w", padx=20)
        self.result_prob_bar = ctk.CTkProgressBar(self.result_card, height=14, corner_radius=7,
                                                    progress_color=ACCENT, fg_color=BG_CARD_ALT)
        self.result_prob_bar.set(0)
        self.result_prob_bar.pack(fill="x", padx=20, pady=(14, 4))
        self.result_prob_label = ctk.CTkLabel(self.result_card, text="Churn probability: —",
                                               font=(FONT_FAMILY, 12), text_color=TEXT_SECONDARY)
        self.result_prob_label.pack(anchor="w", padx=20, pady=(0, 18))

    def _on_pred_mode_change(self, value):

        if value == "Sample Customer":
            self.manual_panel.grid_remove()
            self.sample_panel.grid()
        else:
            self.sample_panel.grid_remove()
            self.manual_panel.grid(row=2, column=0, sticky="ew", padx=24, pady=8)

    def _build_manual_form(self):
        for w in self.manual_form_scroll.winfo_children():
            w.destroy()
        self.manual_inputs = {}
        columns = self.numeric_features + self.categorical_features
        for i, col in enumerate(columns):
            cell = ctk.CTkFrame(self.manual_form_scroll, fg_color="transparent")
            cell.grid(row=i // 2, column=i % 2, sticky="ew", padx=6, pady=6)
            ctk.CTkLabel(cell, text=col, font=(FONT_FAMILY, 10, "bold"),
                         text_color=TEXT_MUTED).pack(anchor="w")

            if col in self.categorical_features:
                options = self.category_options.get(col, [""])
                var = tk.StringVar(value=options[0] if options else "")
                widget = ctk.CTkOptionMenu(cell, values=options, variable=var,
                                            fg_color=BG_CARD_ALT, button_color=BG_CARD_ALT,
                                            button_hover_color=BG_HOVER,
                                            dropdown_fg_color=BG_CARD_ALT,
                                            text_color=TEXT_PRIMARY)
                widget.pack(fill="x", pady=(2, 0))
                self.manual_inputs[col] = ("categorical", var)
            else:

                default = self.df[col].median() if col in self.df.columns else 0
                entry = ctk.CTkEntry(cell, fg_color=BG_CARD_ALT, text_color=TEXT_PRIMARY,
                                      corner_radius=8, border_width=0)
                entry.insert(0, f"{default:.2f}" if pd.notna(default) else "0")
                entry.pack(fill="x", pady=(2, 0))
                self.manual_inputs[col] = ("numeric", entry)
        self.manual_predict_btn.configure(state="normal")

    def get_sample_customer(self):

        if self.X_test is None or len(self.X_test) == 0:
            messagebox.showinfo("Info", "Train the models first to get test customers.")
            return
        idx = np.random.randint(0, len(self.X_test))
        self.current_sample = self.X_test.iloc[[idx]]
        self.sample_text.configure(state="normal")
        self.sample_text.delete("1.0", "end")
        for col in self.current_sample.columns:
            self.sample_text.insert("end", f"{col:<22}: {self.current_sample.iloc[0][col]}\n")
        self.sample_text.configure(state="disabled")
        self.set_status("Sample customer loaded. Click Predict.")

    def predict_sample_customer(self):

        if self.best_model is None:
            messagebox.showinfo("Info", "Train the models first.")
            return

        if self.current_sample is None:
            messagebox.showinfo("Info", "Pick a random test customer first.")
            return
        pred = int(self.best_model.predict(self.current_sample)[0])
        prob = float(self.best_model.predict_proba(self.current_sample)[0][1])
        self._show_prediction_result(pred, prob)

    def predict_manual_entry(self):

        if self.best_model is None:
            messagebox.showinfo("Info", "Train the models first.")
            return

        try:
            row = {}
            for col, (kind, widget) in self.manual_inputs.items():

                if kind == "numeric":
                    row[col] = [float(widget.get())]
                else:
                    row[col] = [widget.get()]
            sample_df = pd.DataFrame(row)
            sample_df = sample_df[self.numeric_features + self.categorical_features]
            pred = int(self.best_model.predict(sample_df)[0])
            prob = float(self.best_model.predict_proba(sample_df)[0][1])
            self._show_prediction_result(pred, prob)

        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid numbers in numeric fields.")

        except Exception as e:
            messagebox.showerror("Prediction Error", str(e))

    def _show_prediction_result(self, pred, prob):

        if pred == 1:
            self.result_title.configure(text="⚠ CUSTOMER WILL CHURN", text_color=DANGER)
            self.result_prob_bar.configure(progress_color=DANGER)
        else:
            self.result_title.configure(text="✓ CUSTOMER WILL STAY", text_color=SUCCESS)
            self.result_prob_bar.configure(progress_color=SUCCESS)
        self.result_prob_bar.set(prob)
        self.result_prob_label.configure(
            text=f"Churn probability: {prob * 100:.2f}%   •   Model: {self.best_model_name}")
        self.set_status("Prediction completed.")
