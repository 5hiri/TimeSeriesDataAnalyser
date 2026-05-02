# Project Overview

## Goal

Provide a simple desktop tool to load CSV data, inspect it in a table, and plot a basic line chart. The focus is on quick inspection of tabular time series or numeric data without complex setup.

## Core Workflow

1. Import one or more CSV files.
2. Pick an active dataset from the sidebar list.
3. Choose plotting settings (columns, filters) when prompted.
4. View the data table or plot a line graph.
5. Optionally apply a log transform or column filters.

## Key Capabilities

- Multi-dataset list with quick switching.
- Table view of the current dataset.
- Line plot from selected X and Y columns.
- Column visibility filters for table and plot.
- Numeric filtering via the Filter Window.
- Log transform for numeric columns.

## Intended Usage

This app is best for small-to-medium CSV files where quick visual inspection is more important than advanced analysis. For large datasets, the UI may be slower because it renders every row in a table widget.
