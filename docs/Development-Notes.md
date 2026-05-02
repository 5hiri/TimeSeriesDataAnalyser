# Development Notes

## Dependencies

- Python 3.x
- pandas
- numpy
- matplotlib
- tkinter (built-in with most Python distributions)

## Internal Behavior Notes

- The app stores both a current DataFrame and a backup copy for each dataset.
- Log transform modifies numeric columns in place on the current DataFrame.
- Filters update the current DataFrame and then re-plot the view.

## Known Issues and Limitations

- File name display uses a split on '/', which is not correct for Windows paths. Using os.path.basename would be more robust.
- The filter logic checks only the first numeric column name when applying filters; it should check all numeric columns.
- Plot setup validation repeats the X column check twice instead of checking X and Y separately.
- The table view renders every row, which can be slow for large datasets.

## Improvement Ideas

- Replace list-based dataset storage with a small data class for clarity.
- Add a reset-to-original button that restores the backup DataFrame.
- Add explicit error messages for invalid filter input formats.
- Add a simple About dialog in the Help menu.
