from logging import exception

from database.dao import Dao
import networkx as nx

class Model:
    def __init__(self):
        self._graph = nx.Graph()
        self._users_list = []
        self.load_all_users()

    def load_all_users(self):
        self._users_list = Dao.read_all_users()
        print(f"Users: {self._users_list}")

    def crea_grafo(self, n_bus):
        self._graph.clear()
        utenti = Dao.get_users_min_business(n_bus)

        if utenti is None:
            raise Exception("Errore di connessione al database")

        if len(utenti)==0:
            raise Exception("Nessun utente trovato")

        self._id_map={u.user_id: u for u utenti}
        self._graph.add_nodes_from(utenti)

        archi= Dao.get_archi(self._id_map)
        if archi is None:
            raise Exception("Errore di connessione al database")

        for u1, u2, peso in archi:
            self._graph.add_edge(u1, u2, weight=peso)

    def get_num_nodi_archi(self):
        return self._graph.number_of_nodes(), self._graph.number_of_edges()

    def get_utenti_grafo(self):
        return list(self._graph.nodes())

    def get_utente_by_id(self, user_id):
        return self._id_map.get(user_id)

    def get_utenti_piu_connessi(self):
        risultato=[]
        for utente in self._graph.nodes():
            forza=0
            for _, _, dati in self._graph.edges(utente, data=True):
                forza += dati["weight"]
            risultato.append((utente, forza))
        risultato.sort(key=lambda x: x[1], reverse=True)
        return risultato

    def cerca_sequenza(self, utente_iniziale, L):
        if utente_iniziale not in self._graph:
            raise Exception("Utente iniziale non è presente nel grafo")
        if L < 2 or L > self._graph.number_of_nodes():
            raise Exception("Lunghezza sequenza non è valida")

        self._L= L
        self._migliore_sequenza= []
        self._migliore_peso= -1

        parziale= [utente_iniziale]
        self._ricorsione(parziale, 0)

        return self._migliore_sequenza, self._migliore_peso

    def _ricorsione(self, parziale, peso_corrente):
        if len(parziale) == self._L:
            if peso_corrente > self._migliore_peso:
                self._migliore_peso = peso_corrente
                self._migliore_sequenza= parziale.copy()
            return

        ultimo = parziale[-1]
        for vicino in self._graph.neighbors(ultimo):
            if vicino not in parziale:
                peso = self._graph[ultimo][vicino]["weight"]
                parziale.append(vicino)
                self._ricorsione(parziale, peso_corrente + peso)
                parziale.pop()





