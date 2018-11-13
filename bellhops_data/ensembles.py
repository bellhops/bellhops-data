import numpy as np
import pandas as pd
from xgboost import XGBRegressor
from sklearn.ensemble import AdaBoostRegressor

class AdaBoostQuantile(AdaBoostRegressor):
    def _get_quantile_predict(self, X, limit):
        # Evaluate predictions of all estimators
        predictions = np.array([
            est.predict(X) for est in self.estimators_[:limit]]).T

        # Sort the predictions
        sorted_idx = np.argsort(predictions, axis=1)

        # Find index of median prediction for each sample
        weight_cdf = self.estimator_weights_[sorted_idx].cumsum(axis=1)
        median_or_above = weight_cdf >= 0.5 * weight_cdf[:, -1][:, np.newaxis]
        median_idx = median_or_above.argmax(axis=1)

        median_estimators = sorted_idx[np.arange(X.shape[0]), median_idx]

        # Return median predictions
        return predictions[np.arange(X.shape[0]), median_estimators]

    def predict(self, X):
            check_is_fitted(self, "estimator_weights_")
            X = self._validate_X_predict(X)

            return self._get_quantile_predict(X, len(self.estimators_))

class XGBQuantile(XGBRegressor):
    def __init__(self, max_depth=3, learning_rate=0.1, n_estimators=100, silent=True, objective="reg:linear", booster='gbtree', n_jobs=1, nthread=None, gamma=0, min_child_weight=1, max_delta_step=0, subsample=1, colsample_bytree=1, colsample_bylevel=1, reg_alpha=0, reg_lamda=1, scale_pos_weight=1, base_score=0.5, random_state=0, seed=None, missing=None, **kwargs):
        self.max_depth = max_depth
        self.learning_rate = learning_rate
        self.n_estimators = n_estimators
        self.silent = silent
        self.objective = objective
        self.booster = booster
        self.gamma = gamma
        self.min_child_weight = min_child_weight
        self.max_delta_step = max_delta_step
        self.subsample = subsample
        self.colsample_bytree = colsample_bytree
        self.colsample_bylevel = colsample_bylevel
        self.reg_alpha = reg_alpha
        self.reg_lambda = reg_lamda
        self.scale_pos_weight = scale_pos_weight
        self.base_score = base_score
        self.missing = missing if missing is not None else np.nan
        self.kwargs = kwargs
        self._Booster = None
        self.seed = seed
        self.random_state = random_state
        self.nthread = nthread
        self.n_jobs = n_jobs
