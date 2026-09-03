# Version 1.5.0

Version 1.5.0 improves dashboard date control, administrator client context,
and cross-domain correlation analysis.

## Month range

Each dashboard opens with the latest available month selected. The filter is a
compact popover. Opening it displays a checkbox beside every available month.
Additional months can be checked for longer trend analysis.

## Administrator intake details

On the main Dashboard, administrators can expand **View full client intake
information** for the selected client. The panel displays every client-profile
field currently stored in the database.

Client logins do not see this panel.

## Correlation analysis

Cross-Domain Analytics now lets the administrator choose the X metric and Y
metric. The page displays a scatter plot, regression trend line, Pearson
correlation coefficient, relationship strength/direction, and number of matched
days.

Downloads include CSV for the selected metric pair and an Excel workbook with
the selected pair, filtered daily data, and complete correlation matrix.
