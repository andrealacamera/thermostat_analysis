import sys
import pandas as pd
import matplotlib.pyplot as plt


def analyze_thermostat(file_path):
    print(f"Reading file: {file_path}...")

    try:
        # Read CSV with ';' separator and ignore trailing semicolons via usecols
        df = pd.read_csv(file_path, sep=";", decimal=",", dtype={0: str}, usecols=[0, 1, 2], header=0)
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)

    # Explicitly name the columns based on your header
    df.columns = ["timestamp", "room_temp", "setpoint_temp"]

    # Convert timestamp column to datetime objects safely
    df["timestamp"] = pd.to_datetime(df["timestamp"].astype(str), format="%d/%m/%Y %H:%M:%S")

    # --- EXCLUDE NEGATIVE SETPOINT ERRORS (e.g., -1000) ---
    initial_row_count = len(df)
    df = df[df["setpoint_temp"] >= 0].copy()
    excluded_count = initial_row_count - len(df)
    print(f"Filtered out {excluded_count} error rows (negative setpoints like -1000).")

    # Sort data chronologically just in case
    df = df.sort_values("timestamp").reset_index(drop=True)

    # --- 1. Calculate Time "On" & Daily Statistics ---
    df["interval_min"] = df["timestamp"].diff(-1).abs().dt.total_seconds() / 60.0

    median_interval = df["timestamp"].diff().dt.total_seconds().median() / 60.0
    if pd.isna(median_interval) or median_interval == 0:
        median_interval = 1.0
    df["interval_min"] = df["interval_min"].fillna(median_interval)

    # Add a date column for grouping by day
    df["date"] = df["timestamp"].dt.date

    # Filter where setpoint temperature is greater than 18 for on-time calculation
    on_df = df[df["setpoint_temp"] > 18.0]
    daily_on_time = on_df.groupby("date")["interval_min"].sum()

    # Calculate daily statistics (Min, Max, Mean) for Room Temperature
    daily_room_stats = df.groupby("date")["room_temp"].agg(room_min="min", room_max="max", room_mean="mean")

    # Combine on-time and room temperature stats into a single summary table
    daily_summary = (
        pd.DataFrame({"on_minutes": daily_on_time}).join(daily_room_stats, how="outer").fillna({"on_minutes": 0})
    )

    print("\n--- Daily Summary (On Time & Room Temperature Statistics) ---")
    if daily_summary.empty:
        print("No data available to summarize.")
    else:
        for date, row in daily_summary.iterrows():
            minutes = row["on_minutes"]
            hours = int(minutes // 60)
            mins = int(minutes % 60)

            # Safe check in case a day had no readings for room temp
            r_min = f"{row['room_min']:.1f}°C" if pd.notna(row["room_min"]) else "N/A"
            r_max = f"{row['room_max']:.1f}°C" if pd.notna(row["room_max"]) else "N/A"
            r_mean = f"{row['room_mean']:.1f}°C" if pd.notna(row["room_mean"]) else "N/A"

            print(f"Date: {date} | On Time: {hours}h {mins}m | Room Temp -> Min: {r_min}, Max: {r_max}, Mean: {r_mean}")

    # --- 2. Plotting the Data Series ---
    plt.figure(figsize=(12, 6))

    plt.plot(df["timestamp"], df["room_temp"], label="Room Temperature (°C)", color="orange", linewidth=1.5)
    plt.plot(
        df["timestamp"],
        df["setpoint_temp"],
        label="Setpoint Temperature (°C)",
        color="blue",
        linestyle="--",
        linewidth=1.5,
    )

    plt.xlabel("Time")
    plt.ylabel("Temperature (°C)")
    plt.title("Thermostat Logs: Room vs. Setpoint Temperature")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    print("\nDisplaying plot...")
    plt.show()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python thermostat_analysis.py <path_to_csv>")
        sys.exit(1)

    analyze_thermostat(sys.argv[1])
