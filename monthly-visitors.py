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
    # - Use the "activeUsers" metric (for total unique visitors).
    request = RunReportRequest(
        property=f"properties/{PROPERTY_ID}",
        date_ranges=[DateRange(start_date="2025-01-01", end_date="2025-06-30")],
        dimensions=[Dimension(name="month")],
        metrics=[Metric(name="activeUsers")],
    )

    # Run the report
    response = client.run_report(request)
    return response


def process_response(response):
    # Create a dictionary to hold aggregated users for each month ("01" through "12")
    monthly_users = {f"{i:02d}": 0 for i in range(1, 13)}

    # Iterate through the rows returned by the API
    for row in response.rows:
        # The first dimension value is the month (as a string, e.g. "1", "2", etc.)
        month = row.dimension_values[0].value.zfill(2)  # Ensure two-digit month ("01", "02", ...)
        users = int(row.metric_values[0].value)
        monthly_users[month] += users

    # Convert the dictionary into a sorted list of dictionaries for DataFrame creation.
    data = []
    for month in sorted(monthly_users.keys()):
        # Construct a date for formatting purposes
        month_date = datetime.strptime(f"2025-{month}-01", "%Y-%m-%d")
        data.append({
            "Month": month_date.strftime("%Y-%m"),
            "Visitors": monthly_users[month]
        })
    return data


def export_to_excel(data):
    # Create a DataFrame from the data and export it to an Excel file.
    df = pd.DataFrame(data)
    output_file = "monthly_visitors_2025.xlsx"
    df.to_excel(output_file, index=False)
    print("Excel file created successfully!")
    os.startfile(output_file)  # This opens the file automatically on Windows


def main():
    response = run_report()
    data = process_response(response)
    export_to_excel(data)


if __name__ == "__main__":
    main()
