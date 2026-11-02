"""ESTATIQ: reproducible, chronological one-month-ahead Zillow ZHVI evaluation."""
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.dummy import DummyRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import lightgbm as lgb
import xgboost as xgb
ROOT = Path(__file__).resolve().parent
DATA = ROOT / 'data'
INPUT = DATA / 'zillow_cleaned.csv'


def monthly_columns(frame):
    return sorted(c for c in frame.columns if len(str(c)) == 10 and pd.notna(pd.to_datetime(c, format='%Y-%m-%d', errors='coerce')))


def build_examples(frame, dates):
    values = frame[dates].apply(pd.to_numeric, errors='coerce')
    ids = frame['RegionID'] if 'RegionID' in frame else pd.Series(np.arange(len(frame)))
    names = frame['RegionName'] if 'RegionName' in frame else pd.Series(['Unknown'] * len(frame))
    states = frame['State'] if 'State' in frame else pd.Series([''] * len(frame))
    parts = []
    for i in range(3, len(dates)):
        if dates[i] < '2018-01-01':
            continue
        block = values.iloc[:, i-3:i+1].copy()
        block.columns = ['Month1', 'Month2', 'Month3', 'Target']
        block['Date'] = dates[i]
        block['RegionID'] = ids.to_numpy()
        block['RegionName'] = names.to_numpy()
        block['State'] = states.to_numpy()
        parts.append(block.dropna(subset=['Month1','Month2','Month3','Target']))
    if not parts:
        raise ValueError('No valid monthly training examples were found.')
    return pd.concat(parts, ignore_index=True)


def evaluate(data, test_start):
    train = data[data['Date'] < test_start]
    test = data[data['Date'] >= test_start].copy()
    if train.empty or test.empty:
        raise ValueError('Chronological training or test set is empty.')
    features = ['Month1','Month2','Month3']
    x_train, y_train = train[features], train['Target']
    x_test, y_test = test[features], test['Target']
    models = {
        'Naive baseline (previous month)': None,
        'Linear Regression': LinearRegression(),
        'Random Forest': RandomForestRegressor(n_estimators=50, max_depth=12, random_state=42, n_jobs=-1),
    }

    # These are intentionally conservative settings. The Zillow data here is a very smooth,
    # near-linear monthly trend, so deep/tree-heavy boosters tend to overfit the short lag features.
    if xgb is not None:
        models['XGBoost'] = xgb.XGBRegressor(
            objective='reg:squarederror',
            n_estimators=500,
            learning_rate=0.03,
            max_depth=4,
            subsample=0.8,
            colsample_bytree=0.8,
            reg_lambda=3.0,
            min_child_weight=3,
            random_state=42,
            n_jobs=-1,
        )
    if lgb is not None:
        models['LightGBM'] = lgb.LGBMRegressor(
            objective='regression',
            n_estimators=500,
            learning_rate=0.03,
            max_depth=6,
            num_leaves=16,
            subsample=0.9,
            colsample_bytree=0.9,
            reg_alpha=0.1,
            reg_lambda=1.0,
            min_child_samples=20,
            random_state=42,
            n_jobs=-1,
            verbosity=-1,
        )
    metrics, predictions = [], []
    for name, model in models.items():
        if model is None:
            pred = x_test['Month3'].to_numpy()
        else:
            model.fit(x_train, y_train)
            pred = model.predict(x_test)
        metrics.append({
            'Model': name,
            'MAE': round(mean_absolute_error(y_test, pred), 2),
            'RMSE': round(float(np.sqrt(mean_squared_error(y_test, pred))), 2),
            'R2': round(float(r2_score(y_test, pred)), 6),
            'Train Samples': len(train),
            'Test Samples': len(test),
            'Test Start': test_start,
            'Test End': test['Date'].max(),
        })
        output = test[['RegionID','RegionName','State','Date','Target']].copy()
        output = output.rename(columns={'Target':'Actual'})
        output['Predicted'] = pred
        output['Absolute Error'] = np.abs(output['Actual'] - output['Predicted'])
        output['Model'] = name
        predictions.append(output)
    return pd.DataFrame(metrics), pd.concat(predictions, ignore_index=True)


def main():
    if not INPUT.exists():
        raise FileNotFoundError(f'Missing {INPUT}. Run explore_data.py first.')
    df = pd.read_csv(INPUT, low_memory=False)
    dates = monthly_columns(df)
    if len(dates) < 16:
        raise ValueError('At least 16 monthly periods are required.')
    test_start = dates[-12]
    data = build_examples(df, dates)
    results, predictions = evaluate(data, test_start)
    DATA.mkdir(exist_ok=True)
    results.to_csv(DATA / 'model_results.csv', index=False)
    predictions.to_csv(DATA / 'model_predictions.csv', index=False)
    print('=== ESTATIQ MACHINE LEARNING V2 ===')
    print(f'Chronological holdout: {test_start} through {dates[-1]}')
    print(results.to_string(index=False))
    print(f'\nSaved: {DATA / "model_results.csv"}')
    print(f'Saved: {DATA / "model_predictions.csv"}')
    print('\nNote: This is one-month-ahead historical backtesting, not a multi-month future forecast.')


if __name__ == '__main__':
    main()
