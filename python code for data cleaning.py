import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import numpy as np

# Load the dataset
file_path = "/mnt/data/IEA CCUS Projects Database 2024.xlsx"
xls = pd.ExcelFile(file_path)
ccus_df = pd.read_excel(xls, sheet_name="CCUS Projects Database")

# Select relevant columns
ccus_cleaned = ccus_df[["Project name", "Country", "Project type", "Announcement", "FID", "Operation", "Project Status"]]

# Rename columns
ccus_cleaned.columns = ["Project_Name", "Country", "Project_Type", "Announcement_Year", "FID_Year", "Operation_Year", "Project_Status"]

# Convert year columns to numeric
ccus_cleaned[["Announcement_Year", "FID_Year", "Operation_Year"]] = ccus_cleaned[["Announcement_Year", "FID_Year", "Operation_Year"]].apply(pd.to_numeric, errors="coerce")

# Count projects by country
country_counts = ccus_cleaned["Country"].value_counts().head(10)
plt.figure(figsize=(12, 6))
plt.barh(country_counts.index, country_counts.values, color="royalblue")
plt.xlabel("Number of CCUS Projects")
plt.ylabel("Country")
plt.title("Top 10 Countries with CCUS Projects")
plt.gca().invert_yaxis()
plt.grid(axis="x", linestyle="--", alpha=0.7)
plt.show()

# Count projects by status
status_counts = ccus_cleaned["Project_Status"].value_counts()
plt.figure(figsize=(8, 8))
plt.pie(status_counts, labels=status_counts.index, autopct="%1.1f%%", colors=["lightblue", "orange", "green", "red"])
plt.title("CCUS Project Status Distribution")
plt.show()

# Trend of CCUS project announcements
announcement_trend = ccus_cleaned.groupby("Announcement_Year").size()
plt.figure(figsize=(12, 6))
plt.plot(announcement_trend.index, announcement_trend.values, marker="o", linestyle="-", color="blue")
plt.xlabel("Year")
plt.ylabel("Number of CCUS Projects Announced")
plt.title("Trend of CCUS Project Announcements Over Time")
plt.grid(True)
plt.show()

# Count projects by type
project_type_counts = ccus_cleaned["Project_Type"].value_counts()
plt.figure(figsize=(10, 6))
plt.bar(project_type_counts.index, project_type_counts.values, color="teal")
plt.xlabel("Project Type")
plt.ylabel("Number of Projects")
plt.title("Distribution of CCUS Project Types")
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.show()

# Estimating GHG reduction potential
capture_rates = {"Capture": 2.5, "CCU": 1.8, "Full chain": 3.0}
ccus_cleaned["Estimated_GHG_Reduction"] = ccus_cleaned["Project_Type"].map(capture_rates)
total_ghg_reduction = ccus_cleaned["Estimated_GHG_Reduction"].sum()
print(f"Total Estimated GHG Reduction: {total_ghg_reduction} million metric tons")

# Save cleaned dataset for Power BI
power_bi_df = ccus_cleaned[["Project_Name", "Country", "Project_Type", "Announcement_Year", "FID_Year", "Operation_Year", "Project_Status", "Estimated_GHG_Reduction"]]
power_bi_path = "/mnt/data/ccus_clean_impact_assessment.csv"
power_bi_df.to_csv(power_bi_path, index=False)
