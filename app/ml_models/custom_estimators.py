
from sklearn.base import BaseEstimator, RegressorMixin, clone
from sklearn.model_selection import cross_val_predict


class ResidualEnhancedEnsemble(BaseEstimator, RegressorMixin):

    def __init__(self, primary_model, compensator_model):
        self.primary_model = primary_model
        self.compensator_model = compensator_model

    def fit(self, X, y):
        self.primary_model_ = clone(self.primary_model)
        self.compensator_model_ = clone(self.compensator_model)

        y1_hat_oof = cross_val_predict(
            self.primary_model_, X, y, cv=5
        )

        residuals = y - y1_hat_oof

        self.primary_model_.fit(X, y)
        self.compensator_model_.fit(X, residuals)

        return self

    def predict(self, X):
        y1_hat = self.primary_model_.predict(X)
        r_hat = self.compensator_model_.predict(X)

        return y1_hat + r_hat
