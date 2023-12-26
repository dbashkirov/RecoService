import pandas as pd
from ast import literal_eval


class DSSMModel:

    def __init__(self, path="files/pop_recos.csv"):
        self.recos = pd.read_csv(path)
        try:
            self.recos.item_id = self.recos.item_id.apply(literal_eval)
        except:
            self.recos = pd.DataFrame.from_dict({"0": list(self.recos.item_id)})


    def recommend(self, user_id):
        try:
            res = self.recos.loc[self.recos["user_id"] == user_id, "item_id"].values[0]
        except:
            res = []
        return res
