class DataProcessor:

    def get_conn(self):
        raise NotImplementedError

    def save_to_db(self, data, init):
        raise NotImplementedError

    def create_table(self):
        raise NotImplementedError

    def check_table(self):
        raise NotImplementedError

    def drop_table(self):
        raise NotImplementedError

    def insert_to_db(self, data):
        raise NotImplementedError
