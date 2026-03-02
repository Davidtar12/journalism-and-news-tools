import os
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import DateRange, Dimension, Metric, RunReportRequest
from google.oauth2 import service_account
import pandas as pd
from datetime import datetime
import os

# Configuration
PROPERTY_ID = os.getenv("GA4_PROPERTY_ID", "YOUR_GA4_PROPERTY_ID")  # set in .env
CREDENTIALS_PATH = os.getenv("GA4_CREDENTIALS_PATH", "credentials.json")


def run_report():
    # Authenticate with the GA4 Data API
    client = BetaAnalyticsDataClient.from_service_account_file(CREDENTIALS_PATH)

    # Build the report request:
    # - Retrieve data for 2024.
    # - Group results by month.
    # - Use the "averageSessionDuration" metric (for average session duration in seconds).
    request = RunReportRequest(
        property=f"properties/{PROPERTY_ID}",
        date_ranges=[DateRange(start_date="2023-06-01", end_date="2023-12-31")],
        dimensions=[Dimension(name="month")],
        metrics=[Metric(name="averageSessionDuration")],
    )

    # Run the report
    response = client.run_report(request)
    return response


def process_response(response):
    # Create a dictionary to hold aggregated average session durations for each month ("01" through "12")
    monthly_duration = {f"{i:02d}": 0 for i in range(1, 13)}
    monthly_sessions = {f"{i:02d}": 0 for i in range(1, 13)}  # Track total sessions per month

    # Iterate through the rows returned by the API
    for row in response.rows:
        # The first dimension value is the month (as a string, e.g. "1", "2", etc.)
        month = row.dimension_values[0].value.zfill(2)  # Ensure two-digit month ("01", "02", ...)
        avg_duration = float(row.metric_values[0].value)

        monthly_duration[month] += avg_duration
        monthly_sessions[month] += 1  # Increment the session count for the month

    # Calculate the average session duration for each month by dividing by the number of sessions
    data = []
    for month in sorted(monthly_duration.keys()):
        if monthly_sessions[month] > 0:
            avg_monthly_duration = monthly_duration[month] / monthly_sessions[month]
        else:
            avg_monthly_duration = 0

        # Construct a date for formatting purposes
        month_date = datetime.strptime(f"2023-{month}-01", "%Y-%m-%d")
        data.append({
            "Month": month_date.strftime("%Y-%m"),
            "Avg Session Duration (s)": round(avg_monthly_duration, 2)
        })
    return data


def export_to_excel(data):
    # Create a DataFrame from the data and export it to an Excel file.
    df = pd.DataFrame(data)
    output_file = "average_session_duration_2023.xlsx"
    df.to_excel(output_file, index=False)
    print("Excel file created successfully!")
    os.startfile(output_file)  # This opens the file automatically on Windows


def main():
    response = run_report()
    data = process_response(response)
    export_to_excel(data)


if __name__ == "__main__":
    main()
