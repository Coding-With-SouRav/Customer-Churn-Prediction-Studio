import queue
import threading
import customtkinter as ctk
from tkinter import messagebox
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, classification_report,
)
from .config import (
    BG_MAIN, BG_CARD, BG_CARD_ALT, BORDER, ACCENT, ACCENT_HOVER, GOLD,
    TEXT_PRIMARY, TEXT_SECONDARY, SUCCESS, FONT_FAMILY,
)
from .widgets import SectionHeader
from .common import fmt_pct

class Training:

    def _build_training_page(self):
        page = ctk.CTkScrollableFrame(self.container, fg_color=BG_MAIN)
        page.grid_columnconfigure((0, 1), weight=1)
        self.pages["training"] = page
        header_row = ctk.CTkFrame(page, fg_color="transparent")
        header_row.grid(row=0, column=0, columnspan=2, sticky="ew", padx=24, pady=(24, 12))
        header_row.grid_columnconfigure(0, weight=1)
        SectionHeader(header_row, "Model Training",
                      "Train Logistic Regression & Random Forest and watch progress live."
                      ).grid(row=0, column=0, sticky="w")
        self.train_button = ctk.CTkButton(
            header_row,image = self.train_model_icon, text="Train Models", command=self.start_training,
            fg_color=ACCENT, hover_color=ACCENT_HOVER, height=42, width=170,
            corner_radius=10, font=(FONT_FAMILY, 13, "bold"))
        self.train_button.grid(row=0, column=1, sticky="e")
        progress_card = ctk.CTkFrame(page, fg_color=BG_CARD, corner_radius=16,
                                      border_width=1, border_color=BORDER)
        progress_card.grid(row=1, column=0, columnspan=2, sticky="ew", padx=24, pady=8)
        ctk.CTkLabel(progress_card, text="Training Progress", font=(FONT_FAMILY, 13, "bold"),
                     text_color=TEXT_PRIMARY).pack(anchor="w", padx=20, pady=(16, 8))
        self.progress_bar = ctk.CTkProgressBar(progress_card, height=10, progress_color=ACCENT,
                                                fg_color=BG_CARD_ALT, corner_radius=6)
        self.progress_bar.set(0)
        self.progress_bar.pack(fill="x", padx=20, pady=(0, 18))
        log_card = ctk.CTkFrame(page, fg_color=BG_CARD, corner_radius=16,
                                 border_width=1, border_color=BORDER)
        log_card.grid(row=2, column=0, columnspan=2, sticky="ew", padx=24, pady=8)
        ctk.CTkLabel(log_card, text="Training Log", font=(FONT_FAMILY, 13, "bold"),
                     text_color=TEXT_PRIMARY).pack(anchor="w", padx=20, pady=(16, 8))
        self.log_box = ctk.CTkTextbox(log_card, height=220, fg_color=BG_CARD_ALT,
                                       text_color=SUCCESS, font=("Consolas", 11),
                                       corner_radius=10)
        self.log_box.pack(fill="x", padx=20, pady=(0, 18))
        self.log_box.insert("end", "$ Ready. Load a dataset, then click Train Models.\n")
        self.log_box.configure(state="disabled")
        self.metric_group_lr = self._build_metric_group(page, "Logistic Regression", ACCENT)
        self.metric_group_lr["frame"].grid(row=3, column=0, sticky="nsew", padx=(24, 12), pady=(8, 24))
        self.metric_group_rf = self._build_metric_group(page, "Random Forest", GOLD)
        self.metric_group_rf["frame"].grid(row=3, column=1, sticky="nsew", padx=(12, 24), pady=(8, 24))

    def _build_metric_group(self, parent, title, accent):
        frame = ctk.CTkFrame(parent, fg_color=BG_CARD, corner_radius=16,
                              border_width=1, border_color=BORDER)
        top = ctk.CTkFrame(frame, fg_color="transparent")
        top.pack(fill="x", padx=20, pady=(16, 6))
        ctk.CTkLabel(top, text=title, font=(FONT_FAMILY, 13, "bold"),
                     text_color=TEXT_PRIMARY).pack(side="left")
        badge = ctk.CTkLabel(top, text="", font=(FONT_FAMILY, 10, "bold"),
                              text_color=SUCCESS, fg_color=BG_CARD_ALT,
                              corner_radius=999, width=10, height=22, padx=10)
        badge.pack(side="right")
        labels = {}
        grid = ctk.CTkFrame(frame, fg_color="transparent")
        grid.pack(fill="x", padx=20, pady=(4, 18))
        grid.grid_columnconfigure((0, 1), weight=1)
        metric_names = ["Accuracy", "Precision", "Recall", "F1 Score", "ROC-AUC"]
        for i, name in enumerate(metric_names):
            row = ctk.CTkFrame(grid, fg_color="transparent")
            row.grid(row=i // 2, column=i % 2, sticky="ew", pady=6, padx=6)
            ctk.CTkLabel(row, text=name, font=(FONT_FAMILY, 11),
                         text_color=TEXT_SECONDARY).pack(anchor="w")
            val = ctk.CTkLabel(row, text="—", font=(FONT_FAMILY, 18, "bold"),
                                text_color=accent)
            val.pack(anchor="w")
            labels[name] = val
        return {"frame": frame, "labels": labels, "badge": badge}

    def start_training(self):

        if self.df is None:
            messagebox.showwarning("Dataset Required", "Please load a CSV dataset first.")
            return

        if "Churn" not in self.df.columns:
            messagebox.showerror("Error", "The dataset must contain a 'Churn' column.")
            return
        self.train_button.configure(state="disabled", text="Training…")
        self.progress_bar.set(0)
        self.sidebar_progress.set(0)
        self._log_clear()
        self.set_status("Training models…")
        self.show_page("training")
        threading.Thread(target=self._train_worker, daemon=True).start()

    def _log(self, msg):
        self.log_queue.put(("log", msg))

    def _progress(self, value):
        self.log_queue.put(("progress", value))

    def _poll_log_queue(self):

        try:

            while True:
                kind, payload = self.log_queue.get_nowait()

                if kind == "log":
                    self.log_box.configure(state="normal")
                    self.log_box.insert("end", payload + "\n")
                    self.log_box.see("end")
                    self.log_box.configure(state="disabled")
                elif kind == "progress":
                    self.progress_bar.set(payload)
                    self.sidebar_progress.set(payload)

        except queue.Empty:
            pass
        self.after(150, self._poll_log_queue)

    def _log_clear(self):
        self.log_box.configure(state="normal")
        self.log_box.delete("1.0", "end")
        self.log_box.configure(state="disabled")

    def _train_worker(self):

        try:
            df = self.df.copy()
            churn_col = df["Churn"]

            if pd.api.types.is_numeric_dtype(churn_col):
                df["Churn"] = churn_col
            else:
                normalized = churn_col.astype(str).str.strip().str.lower()
                mapping = {"yes": 1, "no": 0, "true": 1, "false": 0, "1": 1, "0": 0}
                mapped = normalized.map(mapping)
                unmapped = normalized[mapped.isna() & churn_col.notna()].unique().tolist()

                if unmapped:
                    self.after(0, lambda: self._on_training_failed(
                        f"'Churn' column has values I don't know how to map to 0/1: "
                        f"{unmapped}. Expected Yes/No, True/False, or 1/0."))
                    return
                df["Churn"] = mapped

            if df["Churn"].isna().any():
                n_missing = int(df["Churn"].isna().sum())
                self._log(f"$ Note: dropping {n_missing} rows with missing 'Churn' values.")
                df = df.dropna(subset=["Churn"])

            if df.empty:
                self.after(0, lambda: self._on_training_failed(
                    "No rows remain after removing missing 'Churn' values."))
                return
            df["Churn"] = df["Churn"].astype(int)

            if df["Churn"].nunique() < 2:
                self.after(0, lambda: self._on_training_failed(
                    "The 'Churn' column only has one class after cleaning — "
                    "need both churned and non-churned examples to train a classifier."))
                return
            X = df.drop(columns=["Churn"])
            y = df["Churn"]

            if X.shape[1] == 0:
                self.after(0, lambda: self._on_training_failed(
                    "No feature columns remain after removing the 'Churn' column."))
                return
            self._log(f"$ Loaded {X.shape[0]} rows, {X.shape[1]} features.")
            self._progress(0.08)
            min_class_count = int(y.value_counts().min())
            can_stratify = min_class_count >= 2

            if not can_stratify:
                self._log("$ Note: a churn class has fewer than 2 rows — "
                           "splitting without stratification.")
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.20, random_state=42,
                stratify=y if can_stratify else None)
            self._log(f"$ Split → train={len(X_train)}  test={len(X_test)}")
            self._progress(0.18)
            numeric_features = X.select_dtypes(include=["number"]).columns.tolist()
            categorical_features = [c for c in X.columns if c not in numeric_features]
            self._log(f"$ Numeric features:     {numeric_features}")
            self._log(f"$ Categorical features: {categorical_features}")
            category_options = {
                col: sorted(X[col].dropna().unique().tolist()) for col in categorical_features
            }
            numeric_pipeline = Pipeline([
                ("imputer", SimpleImputer(strategy="median")),
                ("scaler", StandardScaler()),
            ])
            categorical_pipeline = Pipeline([
                ("imputer", SimpleImputer(strategy="most_frequent")),
                ("encoder", OneHotEncoder(handle_unknown="ignore")),
            ])
            preprocessor = ColumnTransformer([
                ("numeric", numeric_pipeline, numeric_features),
                ("categorical", categorical_pipeline, categorical_features),
            ])
            self._progress(0.30)
            self._log("\n$ Training Logistic Regression…")
            logistic_model = Pipeline([
                ("preprocessing", preprocessor),
                ("model", LogisticRegression(max_iter=2000)),
            ])
            logistic_model.fit(X_train, y_train)
            lr_pred = logistic_model.predict(X_test)
            lr_prob = logistic_model.predict_proba(X_test)[:, 1]
            metrics_lr = self._compute_metrics(y_test, lr_pred, lr_prob)
            self._log(f"$ Logistic Regression — Accuracy {metrics_lr['accuracy']:.4f}, "
                       f"ROC-AUC {metrics_lr['auc']:.4f}")
            self._progress(0.60)
            self._log("\n$ Training Random Forest (300 trees)…")
            rf_model = Pipeline([
                ("preprocessing", preprocessor),
                ("model", RandomForestClassifier(
                    n_estimators=300, random_state=42,

                    class_weight="balanced", n_jobs=-1)),
            ])
            rf_model.fit(X_train, y_train)
            rf_pred = rf_model.predict(X_test)
            rf_prob = rf_model.predict_proba(X_test)[:, 1]
            metrics_rf = self._compute_metrics(y_test, rf_pred, rf_prob)
            self._log(f"$ Random Forest — Accuracy {metrics_rf['accuracy']:.4f}, "
                       f"ROC-AUC {metrics_rf['auc']:.4f}")
            self._progress(0.88)

            if metrics_rf["auc"] >= metrics_lr["auc"]:
                best_model, best_name = rf_model, "Random Forest"
            else:
                best_model, best_name = logistic_model, "Logistic Regression"
            self._log(f"\n$ Best model selected: {best_name} "
                       f"(ROC-AUC {max(metrics_lr['auc'], metrics_rf['auc']):.4f})")
            results_df = pd.DataFrame({
                "Model": ["Logistic Regression", "Random Forest"],
                "Accuracy": [metrics_lr["accuracy"], metrics_rf["accuracy"]],
                "Precision": [metrics_lr["precision"], metrics_rf["precision"]],
                "Recall": [metrics_lr["recall"], metrics_rf["recall"]],
                "F1 Score": [metrics_lr["f1"], metrics_rf["f1"]],
                "ROC-AUC": [metrics_lr["auc"], metrics_rf["auc"]],
            })
            self._progress(1.0)
            self._log("$ Training complete.\n")

            def finish():
                self.X_train, self.X_test = X_train, X_test
                self.y_train, self.y_test = y_train, y_test
                self.numeric_features = numeric_features
                self.categorical_features = categorical_features
                self.category_options = category_options
                self.logistic_model = logistic_model
                self.rf_model = rf_model
                self.best_model = best_model
                self.best_model_name = best_name
                self.metrics_lr = metrics_lr
                self.metrics_rf = metrics_rf
                self.results_df = results_df
                self._on_training_complete()
            self.after(0, finish)

        except Exception as e:
            self.after(0, lambda: self._on_training_failed(str(e)))
    @staticmethod

    def _compute_metrics(y_true, y_pred, y_prob):
        return {
            "accuracy": accuracy_score(y_true, y_pred),
            "precision": precision_score(y_true, y_pred, zero_division=0),
            "recall": recall_score(y_true, y_pred, zero_division=0),
            "f1": f1_score(y_true, y_pred, zero_division=0),
            "auc": roc_auc_score(y_true, y_prob),
            "report": classification_report(y_true, y_pred, zero_division=0),
        }

    def _on_training_complete(self):
        self.train_button.configure(state="normal", text="Train Models")
        self.set_status(f"Training complete — best: {self.best_model_name}")
        self.card_best.set_value(self.best_model_name)
        for group, metrics in [(self.metric_group_lr, self.metrics_lr),
                                (self.metric_group_rf, self.metrics_rf)]:
            group["labels"]["Accuracy"].configure(text=fmt_pct(metrics["accuracy"]))
            group["labels"]["Precision"].configure(text=fmt_pct(metrics["precision"]))
            group["labels"]["Recall"].configure(text=fmt_pct(metrics["recall"]))
            group["labels"]["F1 Score"].configure(text=fmt_pct(metrics["f1"]))
            group["labels"]["ROC-AUC"].configure(text=f"{metrics['auc']:.3f}")
        self.metric_group_lr["badge"].configure(
            text="BEST" if self.best_model_name == "Logistic Regression" else "",
            text_color=SUCCESS)
        self.metric_group_rf["badge"].configure(
            text="BEST" if self.best_model_name == "Random Forest" else "",
            text_color=SUCCESS)
        self.render_evaluation()
        self._build_manual_form()
        self.sample_predict_btn.configure(state="normal")
        messagebox.showinfo("Training Complete",
                             f"Training finished successfully.\n\nBest model: {self.best_model_name}")

    def _on_training_failed(self, error):
        self.train_button.configure(state="normal", text="Train Models")
        self.progress_bar.set(0)
        self.sidebar_progress.set(0)
        self.set_status("Training failed.")
        self._log(f"$ ERROR: {error}")
        messagebox.showerror("Training Error", error)
