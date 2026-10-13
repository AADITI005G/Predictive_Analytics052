# Food Delivery Time Prediction Using Three Kaggle Datasets

**Aaditi Gaikwad | PRN 23070521052**  
**Predictive Analytics | Submitted to Dr. Deepak Asudani**

## Problem statement
Predict recorded food delivery duration in minutes and evaluate whether available order information improves on a fixed typical-time estimate. This supervised regression project follows the full KDD process on **three distinct Kaggle datasets**.

## All three dataset links
1. **A: Den_Kuznetz — Food Delivery Time Prediction**  
   https://www.kaggle.com/datasets/denkuznetz/food-delivery-time-prediction
2. **B: Rajat Kumar — Food Delivery Time**  
   https://www.kaggle.com/datasets/rajatkumar30/food-delivery-time
3. **C: Ahsan Raza — NYC Restaurants Data - Food Ordering and Delivery**  
   https://www.kaggle.com/datasets/ahsan81/food-ordering-and-delivery-app-dataset

| Dataset | Raw / usable rows | Main predictors | Evaluation |
|---|---:|---|---|
| A | 1,000 / 1,000 | Distance, experience, weather, traffic, time, vehicle | Random orders |
| B | 45,593 / 45,334 | Derived distance, age, order type, vehicle | Unseen couriers |
| C | 1,898 / 1,898 | Order cost, cuisine, weekday/weekend | Unseen restaurants |

Each dataset enters training, validation, final testing and model export. The files have different schemas and no verified shared key, so **three separate models** are fitted. C's `delivery_time` excludes preparation. We do not combine target definitions or claim that a lower score across sources proves a better algorithm. Raw CSVs are included; source metadata and license notices are in `data/DATA_SOURCES.md`.

## Methodology / approach
This study applies the Knowledge Discovery in Databases framework to three public Kaggle datasets. After defining the prediction task, the workflow audits missing values, identifiers and feature availability. Dataset A uses contextual inputs; B derives straight-line distance from coordinates; C uses order-level FoodHub information. Actual preparation duration, ratings whose availability is unsuitable or unclear, and identifying columns are excluded from the relevant predictor sets. Pipelines fit missing-value imputation, category encoding and scaling only on training folds. Five-fold validation compares a median baseline, Ridge, random forest and histogram gradient boosting. A uses random-order validation, B separates couriers and C separates restaurants. Each selected model is refitted on development data and evaluated once on its reserved test set using MAE, RMSE and R-squared. Importance and example predictions provide interpretation, and three complete pipelines are saved for reuse.

## Data cleaning and splits
- A: 120 missing predictor cells. Exclude ID and actual preparation time. 800 development / 200 test orders.
- B: exclude all 259 rows whose order ID repeats. Derive Haversine straight-line distance, not road distance. Zero/out-of-range coordinates and distances over 100 km become missing; age outside 18–80 becomes missing. No guessed coordinate sign corrections. Retain these rows for fold-local imputation.
- B: after exclusions, 4,043 derived distances and 37 ages are missing. Use 36,397 development orders from 1,056 couriers and 8,937 test orders from 264 separate couriers.
- C: all 1,898 orders retained, no missing selected inputs or targets. Exclude rating and actual preparation time. Restaurant name defines groups only. Use 1,600 development orders from 142 restaurants and 298 test orders from 36 unseen restaurants.
- B/C hold out 20% of entities rather than exactly 20% of rows. Five GroupKFold validation folds maintain entity separation. C customers may appear across restaurant groups, so no unseen-customer claim is made.
- All random seeds are 42. No final-test-based tuning is performed.

## Models
Four fixed candidates: median baseline; Ridge alpha 10; random forest with 100 trees and minimum leaf size 5; histogram gradient boosting with 200 iterations, learning rate 0.05, maximum 15 leaves and early stopping disabled. Numeric inputs use median imputation, missing indicators and scaling. Categories use Unknown and one-hot encoding. Non-negative clipping is consistent during scoring and inference.

## Executed test results
MAE and RMSE use minutes; lower is better. Improvements are against each source's own median baseline.

| Dataset | Selected model | Test orders | Baseline MAE | Selected MAE | RMSE | R-squared | MAE reduction |
|---|---|---:|---:|---:|---:|---:|---:|
| A | Ridge | 200 | 17.47 | 8.57 | 11.14 | 0.723 | 50.9% |
| B | Gradient boosting | 8,937 | 7.61 | 6.48 | 8.04 | 0.271 | 14.9% |
| C | Gradient boosting | 298 | 4.28 | 3.64 | 4.36 | 0.242 | 14.8% |

C boosting and Ridge are almost tied in validation (3.6146 vs 3.6160 minutes). Selection follows the minimum-MAE rule, not evidence of statistically meaningful superiority. C's ten-minute tolerance rate is 100% for both its selected model and baseline, so this is not perfect accuracy and is not a useful differentiator there. A and B tolerance rates are 66.5% and 78.6%.

## Project files
- `Food_Delivery_Three_Datasets_KDD.ipynb`: fully executed notebook for A, B and C.
- `data/dataset_a/`, `dataset_b/`, `dataset_c/`: three unchanged raw datasets and source notices.
- `features.py`: feature preparation shared by notebook and inference.
- `predict.py`: inference for A, B or C.
- `run_notebook.py`: execute all notebook cells and save outputs.
- `models/model_A.joblib`, `model_B.joblib`, `model_C.joblib`: complete fitted pipelines.
- `results/`: input audits, excluded rows, splits, CV scores, test predictions, metrics, importance and figures.
- `report/Aaditi_Food_Delivery_Three_Datasets_Report.pdf`: nine-page report containing the six required chapters.
- `presentation/Aaditi_Food_Delivery_Detailed_Animated.pptx`: ten-slide editable presentation with all three dataset links, simple explanations, speaker notes, fade transitions and click-to-reveal animations.

## Run
Use Python 3.12. Open a terminal in this project folder.

```bash
python -m venv .venv
```

Activate on Windows: `.venv\Scripts\activate`  
On macOS/Linux: `source .venv/bin/activate`

```bash
python -m pip install -r requirements.txt
python run_notebook.py
python predict.py --dataset A --input data/example_A.csv --output results/demo_A.csv
python predict.py --dataset B --input data/example_B.csv --output results/demo_B.csv
python predict.py --dataset C --input data/example_C.csv --output results/demo_C.csv
```

Alternatively open the notebook in Jupyter or VS Code with this environment and run all cells from the project root. All data are bundled, so training needs no Kaggle login or internet. The notebook depends on the included `features.py`; keep the project folder together. Pinned dependency versions appear in requirements.txt. Hardware-dependent runtime is a few minutes.

A inputs: Distance_km, Courier_Experience_yrs, Weather, Traffic_Level, Time_of_Day, Vehicle_Type. B inputs: the four location coordinates, Delivery_person_Age, Type_of_order, Type_of_vehicle. C inputs: cost_of_the_order, cuisine_type, day_of_the_week. The target is never required for inference. The examples omit targets. Predictions are estimates, not promised arrival times.

## Presentation
Start desktop PowerPoint **Slide Show** and click to reveal content. Static previews and PDF exports do not play animations. Speaker notes provide elaboration and source context.

## Limitations and future work
These are three separate benchmarks, not a pooled or cross-source transfer model. Sources lack reliable order dates and complete collection provenance. A cannot test unseen entities. B tests unseen couriers; C tests unseen restaurants but can share customers across groups. C measures delivery excluding preparation and has no route/traffic information. B's coordinate cleaning threshold is a declared assumption; age associations are not causal and should not support employment decisions. No calibrated uncertainty intervals are provided. Future work needs timestamped data, verified prediction-time inputs, road-route distances, group-level error checks and arrival-time ranges.

## References and licenses
- Garg et al. (2025): https://arxiv.org/abs/2503.15177
- Wen et al. (2023): https://arxiv.org/abs/2309.01194
- Pipelines: https://scikit-learn.org/stable/modules/compose.html
- Cross-validation and groups: https://scikit-learn.org/stable/modules/cross_validation.html
- Permutation importance: https://scikit-learn.org/stable/modules/permutation_importance.html

Literature summaries use public abstracts, not copied performance scores. Kaggle metadata lists Apache 2.0 for A, ODbL/DbCL for B and CC0 for C. Retain the included source and license notices when uploading. These notices apply to the respective data, not automatically to the project code.
