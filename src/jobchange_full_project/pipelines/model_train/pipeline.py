"""
This is a boilerplate pipeline
generated using Kedro 0.18.8
"""

from kedro.pipeline import Pipeline, node, pipeline

from .nodes import model_train


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                func=model_train,
                inputs=["X_train_final","X_val_final","y_train_final","y_val_final",
                        "parameters"],
                outputs=["production_model","production_cols", "production_model_metrics", "output_plot"],
                name="train",
            ),
        ]
    )