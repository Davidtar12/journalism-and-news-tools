import os
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import (
    DateRange,
    Dimension,
    Metric,
    RunReportRequest,
    Filter,
    FilterExpression
)
from google.oauth2 import service_account
import pandas as pd
from datetime import datetime
import os

# Configuration
PROPERTY_ID = os.getenv("GA4_PROPERTY_ID", "YOUR_GA4_PROPERTY_ID")  # set in .env
CREDENTIALS_PATH = r"C:\Users\david\OneDrive\Documents\DS - Coding - Python\CP\YOUR_SERVICE_ACCOUNT.json"


def run_report():
    # Authenticate with GA4 Data API using your service account key
    client = BetaAnalyticsDataClient.from_service_account_file(CREDENTIALS_PATH)

    # Build the report request:
    # - Group data by "month" and "userAgeBracket"
    # - Retrieve the "activeUsers" metric
    # - Apply a filter to include only the age brackets "18-24" and "25-34"
    request = RunReportRequest(
        property=f"properties/{PROPERTY_ID}",
        date_ranges=[DateRange(start_date="2025-01-01", end_date="2025-06-30")],
        dimensions=[
            Dimension(name="month"),
            Dimension(name="userAgeBracket")
        ],
        metrics=[Metric(name="activeUsers")],
        dimension_filter=FilterExpression(
            filter=Filter(
                field_name="userAgeBracket",
                in_list_filter=Filter.InListFilter(values=["18-24", "25-34"])
            )
        )
    )

    # Run the report
    response = client.run_report(request)
    return response


def process_response(response):
    # Initialize a dictionary for months "01" to "12" with 0 users each.
    monthly_users = {f"{i:02d}": 0 for i in range(1, 13)}

    # Iterate over each row returned in the report.
    # Each row corresponds to a unique combination of month and age bracket.
    for row in response.rows:
        # row.dimension_values[0] is the month value.
        # Ensure the month is two-digit (e.g. "1" becomes "01")
        month = row.dimension_values[0].value.zfill(2)
        users = int(row.metric_values[0].value)
        # Sum the users for this month (across both age brackets)
        monthly_users[month] += users

    # Create a list of dictionaries with formatted dates and user counts.
    data = []
    for month in sorted(monthly_users.keys()):
        # Build a datetime object for the first day of the month in 2024
        month_date = datetime.strptime(f"2025-{month}-01", "%Y-%m-%d")
        data.append({
            "Month": month_date.strftime("%Y-%m"),
            "Users under 35": monthly_users[month]
        })

    return data


def export_to_excel(data):
    df = pd.DataFrame(data)
    output_file = "users_under_35_2025.xlsx"
    df.to_excel(output_file, index=False)
    print("Excel file created successfully!")
    os.startfile(output_file)  # This will open the file automatically on Windows


def main():
    response = run_report()
    data = process_response(response)
    export_to_excel(data)


if __name__ == "__main__":
    main()
