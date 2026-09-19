import re

import pandas as pd

def unpivot_expenses(df: pd.DataFrame) -> pd.DataFrame:

    # ---------------------------------------------------------
    # Identifica as posições das colunas que representam meses
    # ---------------------------------------------------------

    month_columns = [
        index
        for index in range(len(df.columns))
        if re.fullmatch(
            r"\d{4}-\d{2}",
            str(df.iloc[0, index]).strip()
        )
    ]

    if not month_columns:
        raise ValueError(
            "Nenhuma coluna mensal foi encontrada."
        )

    # ---------------------------------------------------------
    # Colunas da estrutura original
    # ---------------------------------------------------------

    GROUP_COLUMN = 1
    LEVEL_COLUMN = 2
    ITEM_COLUMN = 3
    STATUS_COLUMN = 4

    records = []

    current_group = None

    # ---------------------------------------------------------
    # Percorre as linhas
    # ---------------------------------------------------------

    for index, row in df.iterrows():

        group = row.iloc[GROUP_COLUMN]
        level = row.iloc[LEVEL_COLUMN]
        item = row.iloc[ITEM_COLUMN]
        status = row.iloc[STATUS_COLUMN]

        # -----------------------------------------------------
        # Atualiza grupo
        # -----------------------------------------------------

        if pd.notna(group):

            if isinstance(group, str) and group.strip():
                current_group = group.strip()

        # -----------------------------------------------------
        # Ignora linhas sem item
        # -----------------------------------------------------

        if pd.isna(item) or not str(item).strip():
            continue

        item = str(item).strip()

        # -----------------------------------------------------
        # UNPIVOT
        # -----------------------------------------------------

        for column in month_columns:

            month = str(
                df.iloc[0, column]
            ).strip()

            value = row.iloc[column]

            if pd.isna(value):
                continue

            records.append(
                {
                    "grupo": current_group,
                    "nivel": level,
                    "item": item,
                    "status": (
                        str(status).strip()
                        if pd.notna(status) else None
                    ),
                    "mes": month,
                    "valor": float(value),
                    "linha_origem": index + 1,
                }
            )

    return pd.DataFrame(records)
