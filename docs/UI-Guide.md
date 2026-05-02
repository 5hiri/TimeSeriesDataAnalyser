# UI Guide

## Menu Bar

- File -> Open: Import a CSV file.
- File -> Save file: Write current DataFrame back to its original file path.
- File -> Exit: Close the app.
- Windows -> Filter Window: Opens numeric filter entries if filters are set.

## Sidebar

- Import File: Opens file picker and loads a CSV.
- Plotting: Shows table/plot buttons and plot settings.
- Transformations: Shows log transform option.
- Imported Data list: Double-click a dataset to make it active.
- Remove Data: Removes the selected dataset from the list.

## Toolbar

- Table: Display the current dataset in a table widget.
- Plot Graph: Render a line chart using selected X and Y columns.
- Set Filters: Choose visible columns and X/Y columns.
- Log Transform: Apply natural log to numeric columns.

## Plot Settings Window

- Column filters: Checkboxes to select which columns remain visible.
- X-axis and Y-axis selectors: Choose columns for plotting.
- Submit: Saves the selections and refreshes the view.

## Filter Window

- Appears after filters are set and Filter Window is opened.
- One entry per numeric column selected.
- Supports simple expressions with spaces, for example:
  - "> 100"
  - "< 0"
  - "= 5"

Multiple expressions can be combined by separating tokens with spaces.
