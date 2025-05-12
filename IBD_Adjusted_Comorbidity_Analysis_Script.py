# IBD Comorbidity Analysis Script (Revised for GitHub)

import pandas as pd
import numpy as np
from scipy.stats import fisher_exact
from statsmodels.stats.contingency_tables import StratifiedTable
import matplotlib.pyplot as plt

# Load the unadjusted OR input files
unadjusted_df = pd.read_csv("volcano_raw_data.csv")
significant_comorbidities_df = pd.read_excel("Significant cormorbidities of volcano_raw_data.xlsx", sheet_name=0, usecols="A")

# Extract the significant comorbidities from the Excel file
significant_comorbidities = significant_comorbidities_df["Comorbidity"].str.strip().tolist()

# Filter the unadjusted data for only the significant comorbidities
filtered_unadjusted_df = unadjusted_df[unadjusted_df["Comorbidity"].str.strip().isin(significant_comorbidities)].copy()

# Prepare for adjusted OR calculation
patients_df = pd.read_csv("a1_fixed_corrected.csv")
patients_df["group"] = (patients_df["group"] == "case").astype(int)
patients_df["age_group"] = pd.cut(patients_df["age"], bins=[0, 30, 40, 50, 60, 70, 80, 90, 100], labels=["0-30", "31-40", "41-50", "51-60", "61-70", "71-80", "81-90", "91+"], right=False)
patients_df["female"] = (patients_df["gender"] == "Female").astype(int)

# Expand comorbidities into long format
patients_expanded = patients_df.dropna(subset=["comorbidity"]).copy()
patients_expanded["comorbidity"] = patients_expanded["comorbidity"].str.split(", ")
patients_expanded = patients_expanded.explode("comorbidity").reset_index(drop=True)
patients_expanded["comorbidity"] = patients_expanded["comorbidity"].str.strip()

# Filter for selected comorbidities
patients_expanded_filtered = patients_expanded[patients_expanded["comorbidity"].isin(significant_comorbidities)].copy()

# Calculate adjusted ORs
adjusted_results = []
for comorbidity in significant_comorbidities:
    sub_df = patients_expanded_filtered[patients_expanded_filtered["comorbidity"] == comorbidity]
    strata_groups = sub_df.groupby(["age_group", "female"])
    strata_tables = []
    for _, group in strata_groups:
        table = [[(group["group"] == 1).sum(), (group["group"] == 0).sum()],
                 [(patients_df[patients_df["group"] == 1].shape[0] - (group["group"] == 1).sum()),
                  (patients_df[patients_df["group"] == 0].shape[0] - (group["group"] == 0).sum())]]
        if np.min(table) == 0:
            table = [[cell + 0.5 for cell in row] for row in table]
        strata_tables.append(table)
    
    try:
        mh_table = StratifiedTable(strata_tables)
        adj_or = mh_table.oddsratio_pooled
        adj_ci_low, adj_ci_high = mh_table.oddsratio_pooled_confint()
        adj_p = mh_table.test_null_odds().pvalue
    except Exception as e:
        adj_or, adj_ci_low, adj_ci_high, adj_p = (None, None, None, str(e))
    
    adjusted_results.append({
        "Comorbidity": comorbidity,
        "Adjusted_OR": adj_or,
        "Adj_CI_Lower": adj_ci_low,
        "Adj_CI_Upper": adj_ci_high,
        "Adj_P_value": adj_p
    })

# Save the final adjusted results
adjusted_df = pd.DataFrame(adjusted_results)
adjusted_df.to_csv("final_adjusted_or_results_revised.csv", index=False)

print("Analysis completed. Results saved to 'final_adjusted_or_results_revised.csv'")
