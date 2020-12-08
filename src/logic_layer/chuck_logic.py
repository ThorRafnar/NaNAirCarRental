import random

class ChuckLogic():
    def __init__(self, data_api):
        self.data_api = data_api

    def get_random_joke(self):
        chuck_jokes = self.data_api.get_jokes()
        random_number = random.randint(0,len(chuck_jokes)-1)
        return chuck_jokes[random_number]