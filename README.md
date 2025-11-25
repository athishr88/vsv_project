
# **VSV Monthly Dataset Builder**
*A complete pipeline to generate a unified spatiotemporal dataset of weather, county-level metadata, and Vesicular Stomatitis Virus (VSV) outbreak information for the US and Mexico.*

## **Overview**

This repository provides a **step-by-step workflow** to generate a monthly dataset for all counties in the United States and municipalities in Mexico.  
It integrates:

- Geographic shapefiles  
- County/municipality centroids  
- Monthly weather features extracted from `.nc` (NetCDF) files  
- VSV outbreak information  
- Serotype and species metadata  

The final output is a **single combined dataframe** containing every county × every month × all selected features.

This pipeline is useful for:
- Disease forecasting  
- Spatial–temporal modeling  
- Epidemiology studies  
- Machine learning on structured county-level data  

---

## **Input Files Required**

### 1. **Counties of Interest**
A simple text file containing a list of county codes. Example format:

```
MX01001
MX01002
MX01003
MX01004
MX01005
...
```

### 2. **Geospatial Codes**
- US State + County codes  
- Mexico municipality codes  

### 3. **Weather Data (.NC files)**
Each `.nc` file represents a weather variable (temperature, precipitation, humidity, etc.) across time.

### 4. **PII VSV Case File**
A CSV containing:
- County name  
- Outbreak date  
- Species  
- Serotype  
- Other VSV metadata  

Place this file in:  
`original_data/`

---

# **Pipeline Overview**

## **Step 1 — Create Geometry File**  
Run: **`10_create_geometry_file.ipynb`**

- Downloads & processes county/municipality shapefiles (US + Mexico)  
- Combines them into one GeoDataFrame  
- Saves:  
  - `generated_files/geometry_file.csv`  
  - `generated_files/us_mx_combined_shapefile.shp`

---

## **Step 2 — Compute County/Municipality Centroids**  
Run: **`20_calculate_centroid.ipynb`**

- Loads combined shapefile  
- Calculates latitude & longitude of each region  
- Saves:  
  - `generated_files/centroids_us_mx.csv`

---

## **Step 3 — Create Base Monthly Dataframe**  
Run: **`30_create_base_file.ipynb`**

- Creates a master monthly file for:  
  **3597 counties × 560 months (1979–2025)**  
- Acts as the backbone for all weather and VSV features  
- Saves:  
  - `main_data/base_file.pkl`

---

## **Step 4 — Populate Monthly Weather Features**  
Run: **`35_populate_monthly_new.py`**

- Reads each `.nc` file and adds its weather feature to the base dataframe  
- Must be run **once per weather variable**  
- Edit **line 8 & 9** to select your `.nc` file and feature name  
- Produces multiple partial feature files in `main_data/`

---

## **Step 5 — Combine All Weather Feature Files**  
Run: **`40_combine_all.ipynb`**

- Merges all partially populated dataframes from Step 4  
- Saves:  
  - `main_data/combined_v2.pkl`

This file now contains:  
**Every county × every month × all weather variables**

---

# **Integrating VSV Case Information**

## **Step 6 — Build County/Municipality Code Dictionary**  
Run: **`50_new_muni_conversion.ipynb`**

- Builds mapping between  
  **county/municipality names → unique COUNTY_MUNI_CODE**  
- Saves:  
  - `supporting_files/county2municodes_ultimate_dict.json`

---

## **Step 7 — Add COUNTY_MUNI_CODE to VSV Data**  
Run: **`55_add_ccode_to_pii_file.ipynb`**

- Reads the VSV case file  
- Adds the correct COUNTY_MUNI_CODE for each row  
- Outputs an updated PII VSV dataset

---

## **Step 8 — Process VSV Dates**  
Run: **`60_datetime_to_PII.ipynb`**

- Ensures all dates are standardized  
- Extracts year, month, and related fields for joining with monthly data

---

## **Step 9 — Integrate VSV Cases With Monthly Features**  
Run: **`70_integrate_cases_w_feats.ipynb`**

- Adds VSV outbreak counts to the monthly dataset  
- Output contains:  
  - Weather features  
  - VSV count per county per month

---

## **Step 10 — Add Serotype & Species Information**  
Run: **`80_integrate_sp_ser.ipynb`**

- Appends extra columns including:  
  - Serotype (e.g., IN, NJ)  
  - Host species  
- Produces the final polished dataset

---

# **Final Output**

A master dataframe containing:

| COUNTY_MUNI_CODE | Year | Month | Weather Features | VSV Case Count | Serotype | Species |
|------------------|-------|--------|------------------|----------------|----------|----------|

Saved as:

```
main_data/final_dataset.pkl
```

---

# **Folder Structure**

```
project_folder/
│
├── original_data/
│   └── vsv_cases.csv
│
├── generated_files/
│   ├── geometry_file.csv
│   ├── us_mx_combined_shapefile.shp
│   └── centroids_us_mx.csv
│
├── main_data/
│   ├── base_file.pkl
│   ├── combined_v2.pkl
│   ├── weather_feature_*.pkl
│   └── final_dataset.pkl
│
├── supporting_files/
│   └── county2municodes_ultimate_dict.json
```

---

# **Requirements**

Recommended environment:

```
Python 3.9+
geopandas
pandas
netCDF4
numpy
xarray
matplotlib
scipy
```

---

# **Contributing**

Feel free to open a pull request if you'd like to add more weather variables, integrate a new disease dataset, or improve the workflow.

---

# **Questions?**

Create an issue in this repository, and we’ll help you out.
