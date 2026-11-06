# Thermostat Data Analyzer

A lightweight Python script to read, process, and visualize CSV data exported from a thermostat. It automatically handles European decimal formatting (`comma` to `dot`), converts timestamps, filters out negative sensor error codes, plots room vs. setpoint temperatures over time, and calculates daily heating statistics.

## Features

* **Automatic Parsing**: Handles `;` delimiters and European decimal values (e.g., `21,5` $\rightarrow$ `21.5`).
* **Error Filtering**: Automatically excludes faulty thermostat readings with negative setpoint error values (e.g., `-1000`).
* **Daily Heat Usage Analysis**: Calculates total minutes/hours per day when the setpoint temperature exceeds $18^\circ\text{C}$.
* **Daily Temperature Statistics**: Calculates the Minimum, Maximum, and Mean room temperature for each calendar day.
* **Data Visualization**: Generates clean time-series plots for Room Temperature and Setpoint Temperature using `matplotlib`.

## Installation

### Prerequisites

Ensure you have Python 3.13+ installed.

### Dependencies

Install the required Python packages using `pip`:

```bash
pip install pandas matplotlib
```

## Usage

Run the script from your terminal by passing the path to your thermostat CSV file as an argument:

```bash
python thermostat_analysis.py path/to/your/thermostat_data.csv
```

### Input CSV Requirements

The CSV file must follow this structure:

```csv
DateTime;Room Temperature;Setpoint Temperature
30/10/2026 22:35:16;22,8;-1000;
30/10/2026 22:48:31;22,8;18;
30/10/2026 23:01:46;22,7;18;
```

* **Delimiter**: Semicolon (`;`)
* **Column 1**: Timestamp in `dd/mm/yyyy hh:mm:ss` format
* **Column 2**: Room Temperature (decimal separator can be `,`)
* **Column 3**: Setpoint Temperature (decimal separator can be `,`)

### Output Example

```text
Reading file: thermostat_data.csv...
Filtered out 1 error rows (negative setpoints like -1000).

--- Daily Summary (On Time & Room Temperature Statistics) ---
Date: 2026-10-30 | On Time: 0h 26m | Room Temp -> Min: 22.7°C, Max: 22.8°C, Mean: 22.8°C

Displaying plot...
```

## References & Documentation

* [Pandas `read_csv` Documentation](https://pandas.pydata.org/docs/reference/api/pandas.read_csv.html)
* [Matplotlib Pyplot Documentation](https://matplotlib.org/stable/api/pyplot_summary.html)

## Modification History 
- **written** by ALC 2026-11-06
- **updated**: 