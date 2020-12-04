class ChuckData():
    def get_jokes(self):
        with open('data_layer/data_files/chuck_jokes.txt', 'r', encoding='utf-8', newline='') as file_stream:
            jokes_list = []
            for row in file_stream:
                jokes_list.append(row)
            return jokes_list