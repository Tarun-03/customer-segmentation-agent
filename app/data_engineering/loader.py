from pathlib import Path
import pandas as pd


class DataLoader:
    """
    Responsible only for loading datasets.
    """

    def __init__(self):

        self.dataset_path = (
            Path(__file__)
            .resolve()
            .parents[2]
            / "data"
            / "raw"
            / "bank-additional-full.csv"
        )

    def load_dataset(self):

        df = pd.read_csv(
            self.dataset_path,
            sep=";"
        )

        return df