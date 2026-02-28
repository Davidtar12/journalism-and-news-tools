import os
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import DateRange, Dimension, Metric, RunReportRequest, Filter, FilterExpression
import pandas as pd
import os

# Replace with your values
PROPERTY_ID = os.getenv("GA4_PROPERTY_ID", "YOUR_GA4_PROPERTY_ID")  # set in .envCREDENTIALS_PATH = r"C:\Users\david\OneDrive\Documents\DS - Coding - Python\CP\YOUR_SERVICE_ACCOUNT.json"

# Authenticate
client = BetaAnalyticsDataClient.from_service_account_file(CREDENTIALS_PATH)

# Define the request with gender filter
request = RunReportRequest(
    property=f"properties/{PROPERTY_ID}",
    dimensions=[Dimension(name="month")],  # Group by month
    metrics=[Metric(name="totalUsers")],   # Unique users metric
    date_ranges=[DateRange(start_date="2025-01-01", end_date="2025-06-30")],
    dimension_filter=FilterExpression(
        filter=Filter(
            field_name="userGender",
            string_filter=Filter.StringFilter(value="female")  # Only include female users
        )
    )
)

# Fetch data
response = client.run_report(request)

# Convert to dataframe
data = []
for row in response.rows:
    month = row.dimension_values[0].value.zfill(2)  # Ensure two-digit month (01, 02, ..., 12)
    users = row.metric_values[0].value
    data.append({"Year-Month": f"2025-{month}", "Total Female Users": int(users)})

df = pd.DataFrame(data)

# Order by month (chronological order)
df = df.sort_values(by="Year-Month").reset_index(drop=True)

print(df)
output_file = "../female_users_2025.xlsx"
df.to_excel(output_file, index=False)

# Abrir el archivo Excel automáticamente
os.startfile(output_file)