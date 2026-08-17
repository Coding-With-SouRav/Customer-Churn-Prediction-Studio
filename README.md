# Churn Prediction Studio

A dark-themed, `customtkinter`-based desktop app for exploring customer
churn data, training Logistic Regression & Random Forest models,
comparing their performance, and predicting churn for individual
customers.

This app was refactored from a single 1,500+ line `app.py` script into a
proper package so each concern (theming, widgets, and every page) lives
in its own module.

## Project structure

```
ChurnPredictionStudio/
│
├── main.py                # entry point — run this
├── requirements.txt       # Python dependencies
├── README.md
│
└── churn_studio/
    ├── __init__.py        # package init, exposes ChurnStudio & main()
    ├── app.py              # ChurnStudio window class (combines all page mixins)
    ├── config.py           # colors, fonts & global theme setup (ctk/matplotlib/seaborn)
    ├── common.py           # small shared helpers (fmt_pct, mpl canvas, treeview style)
    ├── widgets.py          # reusable widgets: StatCard, SectionHeader, Pill, NavButton
    ├── icon.py             # programmatic window icon (PIL gradient + chart glyph)
    ├── window.py           # app shell: sidebar/nav, window geometry, asset loading
    ├── dashboard.py        # Dashboard page (stat cards, quick actions, workflow)
    ├── dataset.py          # Dataset & EDA page (CSV load/validate, preview, charts)
    ├── training.py         # Model Training page + background training worker
    ├── evaluation.py       # Evaluation page (comparison chart, confusion matrices)
    ├── prediction.py       # Prediction page (sample / manual customer prediction)
    └── about.py            # About page (app info, model export)
```

## How the pieces fit together

`ChurnStudio` (in `app.py`) is a `customtkinter.CTk` window that inherits
from a set of small **mixin classes** — one per page/feature area
(`Window`, `Dashboard`, `Dataset`, `Training`,
`Evaluation`, `Prediction`, `About`). Each mixin owns the
methods that build and drive its page, but they all share the same
`self` (and therefore the same state — dataframe, trained models,
widgets, etc.), exactly like the methods did in the original single
class. This keeps the split purely organizational: behavior is
unchanged from the original `app.py`.

## Assets

The app expects an `assets/` folder (next to wherever it's run from, or
bundled via PyInstaller) containing the PNG icons referenced in
`window.py`'s `load_images()` (`dashboard.png`, `dataset.png`,
`training.png`, `evaluation.png`, `prediction.png`, `about.png`,
`customers.png`, `features.png`, `rate.png`, `model.png`, `load.png`,
`train_model.png`, `refresh.png`, `best.png`, `random.png`, `save.png`,
`studio.png`). Add this folder yourself — it was not part of the
original script's contents.

## Running

```bash
pip install -r requirements.txt
python main.py
```

## Notes

- Windows-only APIs (`ctypes.windll...` for the titlebar color and
  taskbar app-id) are used as-is, unchanged from the original script —
  the app is intended to run on Windows.
- Load a CSV with a `Churn` column (e.g. a Telco-style customer churn
  dataset) from the **Dataset & EDA** page, then train models from the
  **Model Training** page.
