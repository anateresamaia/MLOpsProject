import pandas as pd
import logging
from typing import Dict, Any
import numpy as np
import yaml
import pickle
import warnings
import matplotlib

matplotlib.use('Agg')  # Use a non-interactive backend
warnings.filterwarnings("ignore", category=Warning)

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import RandomizedSearchCV
from sklearn.metrics import accuracy_score

import mlflow

logger = logging.getLogger(__name__)


def model_selection(X_train: pd.DataFrame,
                    X_val: pd.DataFrame,
                    y_train: pd.DataFrame,
                    y_val: pd.DataFrame,
                    champion_dict: Dict[str, Any],
                    champion_model: pickle.Pickler,
                    parameters: Dict[str, Any]) -> Any:
    """Trains a model on the given data and saves it to the given model path.

    Args:
    --
        X_train (pd.DataFrame): Training features.
        X_test (pd.DataFrame): Test features.
        y_train (pd.DataFrame): Training target.
        y_test (pd.DataFrame): Test target.
        parameters (dict): Parameters defined in parameters.yml.

    Returns:
    --
        model (pickle): Trained models.
        scores (json): Trained model metrics.
    """

    models_dict = {
        'LogisticRegression': LogisticRegression(),
        'GradientBoostingClassifier': GradientBoostingClassifier(),
    }

    initial_results = {}

    with open('conf/local/mlflow.yml') as f:
        experiment_name = yaml.load(f, Loader=yaml.loader.SafeLoader)['tracking']['experiment']['name']
        experiment_id = mlflow.get_experiment_by_name(experiment_name).experiment_id
        logger.info(experiment_id)

    logger.info('Starting first step of model selection: Comparing between model types')

    for model_name, model in models_dict.items():
        with mlflow.start_run(experiment_id=experiment_id, nested=True):
            mlflow.sklearn.autolog(log_model_signatures=True, log_input_examples=True)
            y_train = np.ravel(y_train)
            model.fit(X_train, y_train)
            initial_results[model_name] = model.score(X_val, y_val)
            run_id = mlflow.last_active_run().info.run_id
            logger.info(f"Logged model: {model_name} in run {run_id}")

    best_model_name = max(initial_results, key=initial_results.get)
    best_model = models_dict[best_model_name]

    logger.info(f"Best model is {best_model_name} with score {initial_results[best_model_name]}")
    logger.info('Starting second step of model selection: Hyperparameter tuning')

    # Perform hyperparameter tuning with RandomizedSearchCV
    param_distributions = parameters['hyperparameters'][best_model_name]
    with mlflow.start_run(experiment_id=experiment_id, nested=True):
        random_search = RandomizedSearchCV(best_model, param_distributions, n_iter=50, cv=2, scoring='f1',
                                           n_jobs=-1, random_state=42)
        random_search.fit(X_train, y_train)
        best_model = random_search.best_estimator_

    logger.info(f"Hypertuned model score: {random_search.best_score_}")
    pred_score = accuracy_score(y_val, best_model.predict(X_val))

    if champion_dict['val_score'] < pred_score:
        logger.info(
            f"New champion model is {best_model_name} with score: {pred_score} vs {champion_dict['val_score']}")
        return best_model
    else:
        logger.info(
            f"Champion model is still {champion_dict['regressor']} with score: {champion_dict['val_score']} vs {pred_score}")
        return champion_model

