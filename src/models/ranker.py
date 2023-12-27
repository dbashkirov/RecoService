import pandas as pd

class Ranker:

    def __init__(self, path="files/pop_recos.csv"):
        self.recos = pd.read_csv(path)

    def recommend(self, user_id):
        return list(self.recos.item_id.values)