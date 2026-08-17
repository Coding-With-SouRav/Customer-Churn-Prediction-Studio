from pathlib import Path
import customtkinter as ctk
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
import seaborn as sns
from .config import (
    BG_MAIN, BG_CARD, BG_CARD_ALT, BG_HOVER, BORDER,
    ACCENT, ACCENT_HOVER, TEXT_PRIMARY, TEXT_SECONDARY, TEXT_MUTED, FONT_FAMILY, PALETTE,
)
from .widgets import SectionHeader
from .common import make_mpl_canvas

class Dataset:

    def _build_dataset_page(self):
        page = ctk.CTkFrame(self.container, fg_color=BG_MAIN)
        page.grid_columnconfigure(0, weight=1)
        page.grid_rowconfigure(2, weight=1)
        self.pages["dataset"] = page
        header_row = ctk.CTkFrame(page, fg_color="transparent")
        header_row.grid(row=0, column=0, sticky="ew", padx=24, pady=(24, 12))
        header_row.grid_columnconfigure(0, weight=1)
        SectionHeader(header_row, "Dataset & EDA",
                      "Load your CSV, preview the rows, and explore churn patterns."
                      ).grid(row=0, column=0, sticky="w")
        btns = ctk.CTkFrame(header_row, fg_color="transparent")
        btns.grid(row=0, column=1, sticky="e")
        ctk.CTkButton(btns, image = self.load_icon, text=" Select CSV", command=self.select_dataset,
                      fg_color=ACCENT, hover_color=ACCENT_HOVER, height=38,
                      corner_radius=10, font=(FONT_FAMILY, 12, "bold")).pack(side="left", padx=4)
        ctk.CTkButton(btns, image = self.refresh_icon, text="Refresh Charts", command=self.render_eda,
                      fg_color=BG_CARD_ALT, hover_color=BG_HOVER, height=38,
                      corner_radius=10, font=(FONT_FAMILY, 12, "bold"),
                      text_color=TEXT_PRIMARY).pack(side="left", padx=4)
        self.dataset_info_var = tk.StringVar(value="No dataset loaded yet.")
        ctk.CTkLabel(page, textvariable=self.dataset_info_var, font=(FONT_FAMILY, 12),
                     text_color=TEXT_SECONDARY).grid(row=1, column=0, sticky="w", padx=24)
        tabs = ctk.CTkTabview(page, fg_color=BG_CARD, corner_radius=16,
                               segmented_button_fg_color=BG_CARD_ALT,
                               segmented_button_selected_color=ACCENT,
                               segmented_button_selected_hover_color=ACCENT_HOVER,
                               segmented_button_unselected_color=BG_CARD_ALT,
                               text_color=TEXT_PRIMARY, border_width=1, border_color=BORDER)
        tabs.grid(row=2, column=0, sticky="nsew", padx=24, pady=(12, 24))
        tabs.add("Preview")
        tabs.add("Exploratory Charts")
        preview_tab = tabs.tab("Preview")
        preview_tab.grid_columnconfigure(0, weight=1)
        preview_tab.grid_rowconfigure(0, weight=1)
        tree_wrap = ctk.CTkFrame(preview_tab, fg_color=BG_CARD_ALT, corner_radius=12)
        tree_wrap.grid(row=0, column=0, sticky="nsew", padx=12, pady=12)
        tree_wrap.grid_columnconfigure(0, weight=1)
        tree_wrap.grid_rowconfigure(0, weight=1)
        self.tree = ttk.Treeview(tree_wrap, show="headings", style="Premium.Treeview")
        yscroll = ctk.CTkScrollbar(tree_wrap, orientation="vertical", command=self.tree.yview)
        xscroll = ctk.CTkScrollbar(tree_wrap, orientation="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=yscroll.set, xscrollcommand=xscroll.set)
        self.tree.grid(row=0, column=0, sticky="nsew", padx=(2, 0), pady=(2, 0))
        yscroll.grid(row=0, column=1, sticky="ns")
        xscroll.grid(row=1, column=0, sticky="ew")
        eda_tab = tabs.tab("Exploratory Charts")
        eda_tab.grid_columnconfigure((0, 1), weight=1)
        eda_tab.grid_rowconfigure((0, 1), weight=1)
        self.eda_frame = eda_tab

    def render_eda(self):

        if self.df is None or "Churn" not in self.df.columns:
            messagebox.showwarning("Dataset Required", "Load a dataset with a 'Churn' column first.")
            return
        for w in self.eda_frame.winfo_children():
            w.destroy()
        df = self.df.copy()
        specs = [
            ("Churn Distribution", lambda ax: sns.countplot(
                data=df, x="Churn", ax=ax, hue="Churn", palette=PALETTE, legend=False)),
        ]

        if "Contract" in df.columns:
            specs.append(("Churn by Contract", lambda ax: sns.countplot(
                data=df, x="Contract", hue="Churn", ax=ax, palette=PALETTE)))

        if "MonthlyCharges" in df.columns:
            specs.append(("Monthly Charges vs Churn", lambda ax: sns.boxplot(
                data=df, x="Churn", y="MonthlyCharges", ax=ax, hue="Churn",
                palette=PALETTE, legend=False)))

        if "tenure" in df.columns:
            specs.append(("Tenure Distribution", lambda ax: sns.histplot(
                data=df, x="tenure", hue="Churn", kde=True, bins=30, ax=ax, palette=PALETTE)))
        for i, (title, plot_fn) in enumerate(specs[:4]):
            card = ctk.CTkFrame(self.eda_frame, fg_color=BG_CARD_ALT, corner_radius=14)
            card.grid(row=i // 2, column=i % 2, sticky="nsew", padx=10, pady=10)
            fig, canvas = make_mpl_canvas(card, figsize=(5, 3.2))
            ax = fig.add_subplot(111)

            try:
                plot_fn(ax)
                ax.set_title(title, color=TEXT_PRIMARY, fontsize=11, fontweight="bold")

            except Exception as e:
                ax.text(0.5, 0.5, f"Chart unavailable\n{e}", ha="center", va="center",
                        color=TEXT_MUTED, fontsize=9)
            fig.tight_layout()
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True, padx=8, pady=8)

    def select_dataset(self):
        path = filedialog.askopenfilename(
            title="Select Customer Churn CSV",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")])

        if not path:
            return
        p = Path(path)

        try:

            if not p.exists():
                messagebox.showerror("Dataset Error", f"File not found:\n{path}")
                self.set_status("Failed to load dataset.")
                return

            if p.stat().st_size == 0:
                messagebox.showerror("Dataset Error", "The selected file is empty (0 bytes).")
                self.set_status("Failed to load dataset.")
                return

        except OSError as e:
            messagebox.showerror("Dataset Error", f"Could not access the file:\n{e}")
            self.set_status("Failed to load dataset.")
            return

        try:
            df = pd.read_csv(path)

        except pd.errors.EmptyDataError:
            messagebox.showerror("Dataset Error", "The CSV file has no columns / data to parse.")
            self.set_status("Failed to load dataset.")
            return

        except pd.errors.ParserError as e:
            messagebox.showerror("Dataset Error", f"Could not parse this CSV (malformed file):\n{e}")
            self.set_status("Failed to load dataset.")
            return

        except UnicodeDecodeError:
            df = None
            for enc in ("latin1", "cp1252", "utf-16"):

                try:
                    df = pd.read_csv(path, encoding=enc)
                    self._log(f"$ Note: file was not UTF-8, loaded using '{enc}' encoding.")
                    break

                except Exception:
                    continue

            if df is None:
                messagebox.showerror(
                    "Dataset Error",
                    "Could not decode this file. Try re-saving it as UTF-8 CSV.")
                self.set_status("Failed to load dataset.")
                return

        except PermissionError:
            messagebox.showerror("Dataset Error", "Permission denied while reading the file.")
            self.set_status("Failed to load dataset.")
            return

        except MemoryError:
            messagebox.showerror("Dataset Error", "The file is too large to load into memory.")
            self.set_status("Failed to load dataset.")
            return

        except Exception as e:
            messagebox.showerror("Dataset Error", f"Unexpected error while reading CSV:\n{e}")
            self.set_status("Failed to load dataset.")
            return

        try:

            if df.shape[1] == 0:
                messagebox.showerror("Dataset Error", "No columns found in this file.")
                self.set_status("Failed to load dataset.")
                return

            if df.shape[0] == 0:
                messagebox.showerror("Dataset Error", "The CSV has headers but no data rows.")
                self.set_status("Failed to load dataset.")
                return

            if df.columns.duplicated().any():
                dupes = df.columns[df.columns.duplicated()].unique().tolist()
                messagebox.showwarning(
                    "Duplicate Columns",
                    f"Duplicate column names found and will be auto-suffixed: {dupes}")

            if "customerID" in df.columns:
                df = df.drop(columns=["customerID"])

            if "TotalCharges" in df.columns:
                before_na = df["TotalCharges"].isna().sum()
                df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")
                new_na = df["TotalCharges"].isna().sum() - before_na

                if new_na > 0:
                    self._log(f"$ Note: {new_na} non-numeric 'TotalCharges' values "
                               f"converted to NaN.")
            self.df = df
            self.csv_path = path
            self.card_customers.set_value(f"{len(df):,}")
            self.card_features.set_value(str(df.shape[1] - (1 if "Churn" in df.columns else 0)))

            if "Churn" in df.columns:
                churn_series = df["Churn"].dropna()

                if churn_series.empty:
                    self.card_churn.set_value("N/A")
                elif pd.api.types.is_numeric_dtype(churn_series):
                    rate = churn_series.astype(float).mean() * 100
                    self.card_churn.set_value(f"{rate:.1f}%")
                else:
                    normalized = churn_series.astype(str).str.strip().str.lower()
                    known = {"yes", "no", "true", "false", "1", "0"}

                    if not set(normalized.unique()).issubset(known):
                        self._log(f"$ Note: unexpected values in 'Churn' column: "
                                   f"{sorted(set(normalized.unique()) - known)}")
                    rate = normalized.isin({"yes", "true", "1"}).mean() * 100
                    self.card_churn.set_value(f"{rate:.1f}%")
            else:
                self.card_churn.set_value("N/A")
            self.dataset_info_var.set(
                f"{Path(path).name}  •  {df.shape[0]:,} rows × {df.shape[1]} columns")
            self._populate_tree(df.head(150))
            self.render_eda()
            self.set_status("Dataset loaded successfully.")

        except KeyError as e:
            messagebox.showerror("Dataset Error", f"Missing expected column: {e}")
            self.set_status("Failed to load dataset.")

        except Exception as e:
            messagebox.showerror("Dataset Error", f"Unexpected error while processing data:\n{e}")
            self.set_status("Failed to load dataset.")

    def _populate_tree(self, df):
        self.tree.delete(*self.tree.get_children())
        self.tree["columns"] = list(df.columns)
        for col in df.columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120, minwidth=70, anchor="center")
        for _, row in df.iterrows():
            values = ["" if pd.isna(v) else str(v) for v in row]
            self.tree.insert("", "end", values=values)
