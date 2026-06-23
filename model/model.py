from database.dao import Dao
import networkx as nx

class Model:
    def __init__(self):
        self._graph = nx.Graph()
        self._users_list = []
        self.load_all_users()

    def load_all_users(self):
        self._users_list = Dao.read_all_users()
        print(f"Users: {self._users_list}") 7
