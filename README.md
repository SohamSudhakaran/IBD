# All of Us Data Retrieval for IBD Comorbidity Analysis

## Study Design and Data Source

This case-control study utilized data from the All of Us Research Program, a nationwide precision medicine initiative led by the National Institutes of Health (NIH) established in 2016 and launched for national enrollment in May 2018. Data extraction for this study was performed in November 2024.

The All of Us Research Database contains comprehensive health information from over 600,000 participants across the United States, with approximately 80% coming from groups historically underrepresented in biomedical research. The database includes:

* Electronic health records (EHR)
* Participant-provided survey data
* Physical measurements
* Genomic data
* Digital health information

All data is structured within the Observational Medical Outcomes Partnership (OMOP) Common Data Model version 5.3. The OMOP Common Data Model standardizes clinical data across multiple sources using controlled vocabularies, with conditions mapped to SNOMED CT terminology. This standardization enables consistent identification of inflammatory bowel disease (IBD) cases using specific concept codes.

All analyses were conducted within the secure All of Us Researcher Workbench environment in compliance with the program's data use policies. The primary dataset for analysis was stored in the file "a1\_fixed\_corrected.csv."

## Cohort Definition

### Case Selection

We identified IBD cases using OMOP standard concept codes in the condition\_occurrence table. Specifically, participants with at least one occurrence of any of the following diagnostic codes were classified as IBD cases:

* 4074815 (Inflammatory bowel disease)
* 64766004 (Crohn's disease)
* 34000006 (Ulcerative colitis)

No additional temporal criteria or requirements for multiple occurrences were applied. We did not conduct separate subgroup analyses for Crohn's disease and ulcerative colitis patients; all IBD patients were analyzed as a single cohort.

### Control Selection

The control cohort comprised participants without any recorded instances of the aforementioned IBD-related concept codes (4074815, 64766004, 34000006) in their condition\_occurrence records. Additional exclusion criteria included:

* Participants with missing demographic information required for matching
* Participants with incomplete data for the analyzed comorbid conditions

### Matching Methodology

Cases were matched to controls in a 1:4 ratio, providing sufficient statistical power while maintaining computational efficiency. The Cohort Matcher tool, an integrated component of the All of Us Researcher Workbench platform, was employed to implement the matching algorithm.

Controls were matched to cases based on three demographic variables:

* Age (within ±1 year)
* Gender (exact match)
* Race (exact match)

This approach was designed to minimize confounding by these fundamental demographic factors. The matching process was performed without replacement, meaning each control participant could be matched to only one case. When multiple potential controls met the matching criteria for a case, selections were made randomly from the pool of eligible controls. For cases where fewer than four matching controls were available, all available matching controls were included, and the reduced matching ratio was accounted for in the statistical analysis.

## Comorbidity Selection

Comorbid conditions for analysis were selected based on a predefined list compiled in an Excel file prior to data extraction. This list was developed through literature review and clinical expertise to include conditions with potential mechanistic relationships or epidemiological associations with IBD. Each comorbid condition was identified using corresponding OMOP standard concept codes in the condition\_occurrence table, with temporal relationships to IBD diagnosis noted where available.

## Data Extraction and Processing

The data extraction process involved several key steps:

1. **Query Construction**:

   * OMOP concept codes were used to identify cases, controls, and comorbidities
   * SQL queries were developed within the All of Us Researcher Workbench
   * Demographic and clinical variables were extracted for all participants

2. **Data Integration**:

   * Case and control data were merged into a single analytical dataset
   * Comorbidity information was structured for statistical analysis
   * Quality control procedures were implemented to ensure data integrity

3. **Dataset Preparation**:

   * The final dataset included 25,470 participants (5,094 IBD cases and 20,376 matched controls)
   * Variables included demographic characteristics, comorbidity indicators, and group identifiers (case/control)
   * The dataset was exported as "a1\_fixed\_corrected.csv" for subsequent analysis

## Privacy and Access Restrictions

Due to privacy regulations and the sensitive nature of healthcare data:

1. The raw data cannot be directly shared in this repository
2. Researchers interested in accessing the raw data must:

   * Complete the All of Us Researcher Workbench registration process
   * Obtain appropriate institutional approval
   * Complete required training on responsible data use
   * Submit a data access request through the official All of Us platform

For more information on accessing All of Us data, visit: [https://allofus.nih.gov/](https://allofus.nih.gov/)

## Citation

When using data or methods from this project, please cite:
IBD Comorbidity Analysis Scripts

This repository contains the R and Python scripts required for the analysis of comorbidities in Inflammatory Bowel Disease (IBD) patients. The workflow involves two main steps:

Unadjusted OR Calculation (R Script)

Adjusted OR Calculation and Forest Plot Generation (Python Script)

📁 R Script: Unadjusted OR and Significance Filtering

Script Name: IBD_unadjusted_OR_calculation.R

Purpose:

This R script is used to calculate the unadjusted odds ratios (ORs) for each comorbidity present in the patient dataset. It also performs multiple hypothesis correction using the Benjamini-Hochberg (FDR) method to identify significantly associated comorbidities.

Key Steps:

Data Loading:

Reads the "a1_fixed_corrected.csv" file containing patient demographic and comorbidity data.

Unadjusted OR Calculation:

Constructs 2x2 contingency tables for each comorbidity.

Uses Fisher's exact test to compute the unadjusted OR and p-values.

Multiple Hypothesis Correction:

Applies the Benjamini-Hochberg (FDR) method to adjust the raw p-values.

Filters comorbidities with:

FDR-corrected p-value < 0.05

Log2(OR) > 1.5 or Log2(OR) < -0.5

Output Generation:

Produces "volcano_raw_data.csv" as the primary output, containing the unadjusted ORs, p-values, and corrected significance levels.

The significant comorbidities are saved separately in "Significant cormorbidities of volcano_raw_data.xlsx".

📁 Python Script: Adjusted OR Calculation and Forest Plot Generation

Script Name: IBD_Comorbidity_Analysis_Script_Revised.py

Purpose:

This Python script calculates the adjusted odds ratios (ORs) for the comorbidities identified as significant in the R script. It corrects for potential confounding factors like age and gender using the Mantel-Haenszel method and generates forest plots for final visualization.

Key Steps:

Data Loading:

Reads the pre-filtered list of significant comorbidities from "Significant cormorbidities of volcano_raw_data.xlsx".

Loads patient demographic data from "a1_fixed_corrected.csv".

Data Expansion:

Expands the long-format patient data to associate multiple comorbidities with each patient.

Adjusted OR Calculation:

Calculates stratified adjusted ORs using the Mantel-Haenszel method, including continuity correction for sparse data.

Excludes extremely sparse comorbidities (e.g., "Calcium oxalate calculus of kidney") from the main analysis to avoid skewing the results.

Output Generation:

Saves the final adjusted OR results to "final_adjusted_or_results_revised.csv".

Excludes extremely sparse data from the main plot and generates a separate summary for these comorbidities in "sparse_comorbidity_summary.csv".

Visualization:

Generates publication-quality forest plots, distinguishing between unadjusted and adjusted ORs.

📑 Citation

If you use these scripts in your research, please consider citing this repository.

📝 License

This repository is licensed under the MIT License. See the LICENSE file for more details.

