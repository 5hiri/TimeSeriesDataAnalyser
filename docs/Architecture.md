# Architecture

## Modules

- main.py: Single-module app that defines the Tkinter GUI, data model, and plotting logic.

## Key Class

- DataVisApp: Tkinter root window. Owns all UI widgets and application state.

## State Model

- loaded_data: List of datasets, each stored as [display_name, file_path, df_current, df_original].
- data: The currently active dataset entry from loaded_data.
- x_col, y_col: Selected columns for plotting.
- filters: Column list for table and plot filtering.
- col_filters: GUI entries for numeric filter conditions.

## Data Flow

1. File import reads a CSV into a pandas DataFrame.
2. The dataset is stored in loaded_data with both current and original copies.
3. Selecting a dataset updates the active data reference.
4. Plot or table actions read from data[2] (current DataFrame).
5. Log transform and filters modify data[2] and preserve data[3] as a backup.

## Plotting Pipeline

- The app uses Matplotlib Figure + FigureCanvasTkAgg to render into a Tkinter frame.
- Each plot re-creates the figure and replaces the canvas widget.

## UI Composition

- PanedWindow layout: left sidebar (data list + buttons), right main panel.
- Toolbar above the main panel hosts table, plot, filter, and transform actions.
