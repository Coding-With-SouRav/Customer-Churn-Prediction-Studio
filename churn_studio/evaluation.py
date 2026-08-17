import customtkinter as ctk
from tkinter import ttk
import seaborn as sns
from sklearn.metrics import confusion_matrix
from .config import (
    BG_MAIN, BG_CARD, BORDER, ACCENT, ACCENT_SOFT,
    TEXT_PRIMARY, TEXT_SECONDARY, FONT_FAMILY, PALETTE,
)
from .widgets import SectionHeader
from .common import make_mpl_canvas

class Evaluation:

    def _build_evaluation_page(self):
        page = ctk.CTkScrollableFrame(self.container, fg_color=BG_MAIN)
        page.grid_columnconfigure((0, 1), weight=1)
        self.pages["evaluation"] = page
        SectionHeader(page, "Evaluation",
                      "Compare model performance and inspect confusion matrices."
                      ).grid(row=0, column=0, columnspan=2, sticky="ew", padx=24, pady=(24, 12))
        self.eval_placeholder = ctk.CTkLabel(
            page, text="Train the models to see evaluation results here.",
            font=(FONT_FAMILY, 13), text_color=TEXT_SECONDARY)
        self.eval_placeholder.grid(row=1, column=0, columnspan=2, sticky="w", padx=24, pady=20)
        self.eval_content = ctk.CTkFrame(page, fg_color="transparent")
        self.eval_content.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=24, pady=(0, 24))
        self.eval_content.grid_columnconfigure((0, 1), weight=1)

    def render_evaluation(self):
        self.eval_placeholder.grid_remove()
        for w in self.eval_content.winfo_children():
            w.destroy()
        chart_card = ctk.CTkFrame(self.eval_content, fg_color=BG_CARD, corner_radius=16,
                                   border_width=1, border_color=BORDER)
        chart_card.grid(row=0, column=0, columnspan=2, sticky="ew", padx=4, pady=8)
        ctk.CTkLabel(chart_card, text="Model Comparison", font=(FONT_FAMILY, 13, "bold"),
                     text_color=TEXT_PRIMARY).pack(anchor="w", padx=20, pady=(16, 8))
        fig, canvas = make_mpl_canvas(chart_card, figsize=(9.5, 3.6))
        ax = fig.add_subplot(111)
        metrics_names = ["Accuracy", "Precision", "Recall", "F1 Score", "ROC-AUC"]
        comp = self.results_df.set_index("Model")[metrics_names]
        comp.T.plot(kind="bar", ax=ax, color=PALETTE, width=0.7)
        ax.set_ylim(0, 1)
        ax.set_ylabel("Score", color=TEXT_SECONDARY)
        ax.legend(facecolor=BG_CARD, edgecolor=BORDER, labelcolor=TEXT_PRIMARY)
        ax.tick_params(axis="x", rotation=0)
        fig.tight_layout()
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=16, pady=(0, 16))
        for i, (name, model) in enumerate([("Logistic Regression", self.logistic_model),
                                            ("Random Forest", self.rf_model)]):
            card = ctk.CTkFrame(self.eval_content, fg_color=BG_CARD, corner_radius=16,
                                 border_width=1, border_color=BORDER)
            card.grid(row=1, column=i, sticky="nsew", padx=4, pady=8)
            ctk.CTkLabel(card, text=f"{name} — Confusion Matrix", font=(FONT_FAMILY, 12, "bold"),
                         text_color=TEXT_PRIMARY).pack(anchor="w", padx=18, pady=(14, 6))
            fig, canvas = make_mpl_canvas(card, figsize=(4.6, 3.6))
            ax = fig.add_subplot(111)
            cm = confusion_matrix(self.y_test, model.predict(self.X_test))
            sns.heatmap(cm, annot=True, fmt="d", cmap="mako", ax=ax, cbar=False,
                        xticklabels=["No Churn", "Churn"], yticklabels=["No Churn", "Churn"])
            ax.set_xlabel("Predicted", color=TEXT_SECONDARY)
            ax.set_ylabel("Actual", color=TEXT_SECONDARY)
            fig.tight_layout()
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True, padx=14, pady=(0, 14))
        table_card = ctk.CTkFrame(self.eval_content, fg_color=BG_CARD, corner_radius=16,
                                   border_width=1, border_color=BORDER)
        table_card.grid(row=2, column=0, columnspan=2, sticky="ew", padx=4, pady=8)
        ctk.CTkLabel(table_card, text="Full Results", font=(FONT_FAMILY, 13, "bold"),
                     text_color=TEXT_PRIMARY).pack(anchor="w", padx=20, pady=(16, 8))
        cols = list(self.results_df.columns)
        tree = ttk.Treeview(table_card, columns=cols, show="headings", height=2,
                             style="Premium.Treeview")
        for c in cols:
            tree.heading(c, text=c)
            tree.column(c, width=130, anchor="center")
        for _, row in self.results_df.iterrows():
            vals = [row[c] if c == "Model" else f"{row[c]:.4f}" for c in cols]
            tree.insert("", "end", values=vals)
        tree.pack(fill="x", padx=20, pady=(0, 10))
        banner = ctk.CTkFrame(table_card, fg_color=ACCENT_SOFT, corner_radius=12)
        banner.pack(fill="x", padx=20, pady=(6, 18))
        ctk.CTkLabel(banner,image=self.best_icon, text=f"  Best Model: {self.best_model_name}",
                     font=(FONT_FAMILY, 13, "bold"), text_color=ACCENT, compound="left",
                     ).pack(anchor="w", padx=16, pady=10)
