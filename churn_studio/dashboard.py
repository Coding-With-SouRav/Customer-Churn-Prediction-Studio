"""Dashboard page: overview stat cards, quick actions and workflow steps."""

import customtkinter as ctk

from .config import (
    BG_MAIN, BG_CARD, BG_CARD_ALT, BG_HOVER, BORDER,
    ACCENT, ACCENT_HOVER, ACCENT_SOFT, GOLD, DANGER, SUCCESS,
    TEXT_PRIMARY, TEXT_SECONDARY, FONT_FAMILY,
)
from .widgets import StatCard, SectionHeader


class Dashboard:
    """Builds and manages the Dashboard page."""

    # ------------------------------------------------------------------
    #  DASHBOARD PAGE
    # ------------------------------------------------------------------
    def _build_dashboard_page(self):
        page = ctk.CTkScrollableFrame(self.container, fg_color=BG_MAIN)
        page.grid_columnconfigure((0, 1, 2, 3), weight=1)
        self.pages["dashboard"] = page

        SectionHeader(page, "Dashboard",
                      "Load a dataset, train models, and monitor churn risk at a glance."
                      ).grid(row=0, column=0, columnspan=4, sticky="ew", padx=24, pady=(24, 18))

        self.card_customers = StatCard(page, "", "Customers", ACCENT, image=self.customers_icon)
        self.card_features  = StatCard(page, "", "Features", GOLD,   image=self.features_icon)
        self.card_churn     = StatCard(page, "", "Churn Rate", DANGER, image=self.rate_icon)
        self.card_best      = StatCard(page, "", "Best Model", SUCCESS, image=self.model_icon)
        for i, card in enumerate([self.card_customers, self.card_features,
                                    self.card_churn, self.card_best]):
            card.grid(row=1, column=i, sticky="nsew", padx=(24 if i == 0 else 8,
                                                              24 if i == 3 else 8), pady=8)

        quick = ctk.CTkFrame(page, fg_color=BG_CARD, corner_radius=16,
                              border_width=1, border_color=BORDER)
        quick.grid(row=2, column=0, columnspan=4, sticky="ew", padx=24, pady=(18, 8))
        ctk.CTkLabel(quick, text="Quick Actions", font=(FONT_FAMILY, 14, "bold"),
                     text_color=TEXT_PRIMARY).pack(anchor="w", padx=20, pady=(18, 10))
        qrow = ctk.CTkFrame(quick, fg_color="transparent")
        qrow.pack(fill="x", padx=20, pady=(0, 20))
        ctk.CTkButton(qrow,image=self.load_icon, text="Load Dataset", command=self.select_dataset,
                      fg_color=ACCENT, hover_color=ACCENT_HOVER, height=40,
                      corner_radius=10, font=(FONT_FAMILY, 12, "bold")
                      ).pack(side="left", padx=(0, 10))
        ctk.CTkButton(qrow, image=self.train_model_icon, text="Train Models", command=self.start_training,
                      fg_color=BG_CARD_ALT, hover_color=BG_HOVER, height=40,
                      corner_radius=10, font=(FONT_FAMILY, 12, "bold"),
                      text_color=TEXT_PRIMARY
                      ).pack(side="left", padx=10)
        ctk.CTkButton(qrow, image = self.prediction_icon, text="Predict", command=lambda: self.show_page("prediction"),
                      fg_color=BG_CARD_ALT, hover_color=BG_HOVER, height=40,
                      corner_radius=10, font=(FONT_FAMILY, 12, "bold"),
                      text_color=TEXT_PRIMARY
                      ).pack(side="left", padx=10)

        workflow = ctk.CTkFrame(page, fg_color=BG_CARD, corner_radius=16,
                                 border_width=1, border_color=BORDER)
        workflow.grid(row=3, column=0, columnspan=4, sticky="ew", padx=24, pady=(8, 24))
        ctk.CTkLabel(workflow, text="Workflow", font=(FONT_FAMILY, 14, "bold"),
                     text_color=TEXT_PRIMARY).pack(anchor="w", padx=20, pady=(18, 10))
        steps = [
            "Load the Telco-style customer churn CSV",
            "Inspect data quality and explore churn patterns visually",
            "Preprocess numeric & categorical features automatically",
            "Train Logistic Regression and Random Forest in parallel",
            "Compare Accuracy, Precision, Recall, F1 and ROC-AUC",
            "Automatically select the best-performing model",
            "Predict churn risk for a sample or a manually entered customer",
        ]
        for i, s in enumerate(steps, start=1):
            row = ctk.CTkFrame(workflow, fg_color="transparent")
            row.pack(fill="x", padx=20, pady=4)
            ctk.CTkLabel(row, text=str(i), width=22, height=22, corner_radius=11,
                         fg_color=ACCENT_SOFT, text_color=ACCENT,
                         font=(FONT_FAMILY, 10, "bold")).pack(side="left")
            ctk.CTkLabel(row, text=s, font=(FONT_FAMILY, 12),
                         text_color=TEXT_SECONDARY).pack(side="left", padx=10)
        ctk.CTkFrame(workflow, fg_color="transparent", height=10).pack()
