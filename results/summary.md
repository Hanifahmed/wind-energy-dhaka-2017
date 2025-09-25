# Dhaka Wind Assessment — Summary

Single turbine AEP (MWh): 1536.58
Single turbine Capacity Factor: 0.08770433789954338
Number of turbines used for farm scaling (if set): 50

## Model performance
- Random Forest: MAE=0.0007192174913693901, RMSE=0.029983693305057294, R2=0.9999999828685675
- LSTM:         MAE=101.8479207318589, RMSE=198.78464347336399, R2=0.24701021084587282

## Notes
- RF gave very strong fit on test split; TimeSeriesSplit reduced over-optimism.
- LSTM behaved less accurately on this dataset — consider more features or longer records.
- This site (Dhaka) showed low resource (CF ~ 8.77%). Consider coastal sites for utility-scale projects.