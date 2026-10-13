# Dataset sources and attribution

## Dataset A
- Title: Food Delivery Time Prediction
- Provider: Den_Kuznetz (`denkuznetz`)
- URL: https://www.kaggle.com/datasets/denkuznetz/food-delivery-time-prediction
- Version: 1; originally downloaded 11 October 2026.
- Original file: `dataset_a/Food_Delivery_Times.csv` (1,000 rows, 9 columns).
- Kaggle license metadata: Apache 2.0. See `dataset_a/DATA_LICENSE.txt` and saved `source_metadata.json`.
- The collection protocol, geography and exact target endpoint definitions are not verified.

## Dataset B
- Title: Food Delivery Time
- Provider: Rajat Kumar (`rajatkumar30`)
- URL: https://www.kaggle.com/datasets/rajatkumar30/food-delivery-time
- Version: 1; downloaded 13 October 2026 from Kaggle's public dataset download endpoint.
- Original file: `dataset_b/deliverytime.csv` (45,593 rows, 11 columns).
- Metadata snapshot: `dataset_b/second_food_metadata.json`.
- Kaggle license name: **Database: Open Database, Contents: Database Contents**.
- Database license: https://opendatacommons.org/licenses/odbl/1-0/
- Contents license: https://opendatacommons.org/licenses/dbcl/1-0/

Contains information from **Food Delivery Time by Rajat Kumar**, made available under the Open Database License (ODbL). The contents are under the Database Contents License (DbCL), as specified in the saved Kaggle metadata. Raw data are redistributed unchanged with this attribution. Any derived data tables from B in this project are available under ODbL 1.0, with original content attribution retained. This notice does not change the separate license of Dataset A or apply a dataset license to the source code.

## Processing and lineage
The raw files are unchanged; SHA-256 checksums are in `results/audits.json`. The notebook performs feature engineering and cleaning in memory. It excludes every B row whose order ID repeats (259 rows), retaining 45,334. It records exclusions and split membership. A uses six predictors. B uses straight-line distance, age, order type and vehicle. Courier IDs define groups but are not predictors. A and B are separate experiments, not a merged database or matched set of orders. No missing targets are imputed.

Source collection dates, event timing and sampling details remain limited. Do not relabel these as verified operational data from a particular company.


## Dataset C
- Title: NYC Restaurants Data - Food Ordering and Delivery (FoodHub orders).
- Provider: Ahsan Raza (`ahsan81`).
- Link: https://www.kaggle.com/datasets/ahsan81/food-ordering-and-delivery-app-dataset
- Version 1, downloaded 13 October 2026.
- Original file: `dataset_c/food_order.csv`: 1,898 orders, 9 columns, 178 restaurants.
- Metadata license: **CC0: Public Domain**. https://creativecommons.org/publicdomain/zero/1.0/
- Catalogue metadata and detailed description are saved alongside the raw file.
- The target is `delivery_time`: delivery stage only. `food_preparation_time` is separate and excluded; it is not added to the target.
- Three inputs: order cost, cuisine and weekday/weekend. Exclude post-order rating and IDs. Restaurant name is used only for split grouping, not as a predictor.
- 1,600 development orders from 142 restaurants; 298 test orders from 36 separate restaurants. Customers may cross restaurant groups, so this is not an unseen-customer test.
- No rows are removed from C. Raw data stay unchanged. Dataset C is a third independent experiment, with no concatenation or joins to A/B.
