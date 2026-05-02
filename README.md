# TimeSeriesDataAnalyser

A small Tkinter desktop app for loading CSV files, viewing them as tables, and plotting simple line charts. The app also supports column filtering and a log transform on numeric columns.

## Quickstart

1. Install dependencies:

```bash
pip install pandas numpy matplotlib
```

2. Run the app:

```bash
python main.py
```

Tkinter ships with most Python distributions. If it is missing, install it using your Python distribution's package manager.

## Features

- Import one or more CSV files and switch between them from the sidebar list.
- Display data as a table in the main panel.
- Plot a line chart from selected X and Y columns.
- Filter visible columns and apply numeric filters via the Filter Window.
- Apply a log transform to numeric columns.

## Project Layout

- main.py: Tkinter application and all GUI logic.
- test.py: Small script showing log transform on a CSV.
- Financial-Analytics-data1.csv, Financial-Analytics-data1 - Copy.csv: Sample financial dataset.
- plot.csv, plot copy.csv: Sample datasets with small numeric series.
- LICENSE: Non-commercial license terms.
- docs/: Project documentation for Obsidian import.

## Docs Index

Start here: docs/Index.md

## Notes and Limitations

- Log transform uses natural log and will produce -inf for zeros.
- Filter expressions expect tokens separated by spaces (for example: "> 100" or "< 0").
- Some internal checks are minimal and may surface UI errors for invalid column selections.

## License

Non-commercial license. See LICENSE for full terms.
