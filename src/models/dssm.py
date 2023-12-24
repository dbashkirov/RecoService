import pandas as pd

class DSSMModel:

    def __init__(self, path="files/dssm_recos.csv"):
        self.recos = pd.read_csv(path)

    def recommend(self, user_id):
        return self.recos.loc[self.recos["user_id"] == user_id, "item_id"]
