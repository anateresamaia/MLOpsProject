

"""Project pipelines."""
from typing import Dict
from kedro.pipeline import Pipeline, pipeline

from jobchange_full_project.pipelines import (
    ingestion as data_ingestion,
    data_unit_tests as data_tests,
    preprocessing_initial as preprocess_initial,
    data_unit_tests2,
    split_train_pipeline as split_train,
    preprocessing_train_val,
    feature_selection as feature_selection_pipeline,
    model_train as model_train_pipeline,
    model_selection as model_selection_pipeline,
    preprocessing_batch,
    model_predict,
    data_drift

)

def register_pipelines() -> Dict[str, Pipeline]:
    """Register the project's pipelines.

    Returns:
        A mapping from a pipeline name to a ``Pipeline`` object.
    """
    ingestion_pipeline = data_ingestion.create_pipeline()
    data_unit_tests_pipeline = data_tests.create_pipeline()
    preprocess_initial_pipeline = preprocess_initial.create_pipeline()
    data_unit_tests2_pipeline = data_unit_tests2.create_pipeline()
    split_train_pipeline = split_train.create_pipeline()
    preprocess_train_val_pipeline = preprocessing_train_val.create_pipeline()
    feature_selection = feature_selection_pipeline.create_pipeline()
    model_train = model_train_pipeline.create_pipeline()
    model_selection = model_selection_pipeline.create_pipeline()
    preprocess_batch_pipeline = preprocessing_batch.create_pipeline()
    model_predict_pipeline = model_predict.create_pipeline()
    data_drift_pipeline = data_drift.create_pipeline()

    return {
        "ingestion": ingestion_pipeline,
        "data_unit_tests": data_unit_tests_pipeline,
        "preprocess_initial": preprocess_initial_pipeline,
        "data_unit_tests2": data_unit_tests2_pipeline,
        "split_train": split_train_pipeline,
        "preprocess_train_val": preprocess_train_val_pipeline,
        "feature_selection": feature_selection,
        "model_train": model_train,
        "model_selection": model_selection,
        "preprocess_batch": preprocess_batch_pipeline,
        "inference": model_predict_pipeline,
        "data_drift_pipeline": data_drift_pipeline
    }