from kedro.pipeline import Pipeline, node, pipeline

from .nodes import unpivot_expenses

def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
        node(
            func=unpivot_expenses,
            inputs="expenses_pivot",
            outputs="expenses_unpivot",
            name="unpivot_expenses_node",
            )
        ]
    )
