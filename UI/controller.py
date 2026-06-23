from model.model import Model
from UI.view import View
import flet as ft

class Controller:
    def __init__(self, view : View, model : Model):
        self._view = view
        self._model = model

    def handler_crea_grafo(self, e):
        n_bus_str= self._view.get_n_bus()

        if n_bus_str is None or n_bus_str.strip() == "":
            self._view.show_alert("inserisci un numero minimo di business")
            return

        try:
            n_bus= int(n_bus_str)
        except ValueError:
            self.view.show_alert("il numero minimo di business dev'essere intero")
            return

        if n_bus <= 0:
            self._view.show_alert("il numero deve essere maggiore di zero")
            return
        try:
            self._model.crea_grafo(n_bus)
        except Exception as ex:
            self._view.show_alert(str(ex))
            return
        nodi, archi = self._model.get_num_nodi_archi()

        self._view.clear_result()
        self._view.add_result(f"Grafo creato")
        self._view.update.result()

        self._view.popola_dropdown_utenti(self._model.get_utenti_grafo())
        self._view.abilita_dopo_creazione_grafo()

        #pass

    def handler_utenti_connessi(self, e):
            try:
                risultato= self._model.get_utenti_piu_connessi()
            except Exception as ex:
                self._view.show_alert(str(ex))
                return

            self._view.clear_result()
            for utente, forza in risultato:
                self._view.add_result(f"{utente} - strength= {forza}")
                self._view.update_result()

    def handler_cerca_sequenza(self, e):
        user_id= self._view.get_utente_selezionato()

        if user_id is None:
            self._view.show_alert("seleziona utente iniziale")
            return

        l_str= self._view.get_lunghezza_sequenza()
        if l_str is None or l_str.strip() == "":
            self._view.show_alert("inserisci lunghezza di sequenza")
            return
        try:
            L=int(l_str)
        except ValueError:
            self._view.show_alert("la lunghezza dev'essere intero")
            return

        utente_iniziale= self._model.get_utente_by_id(user_id)
        if utente_iniziale is None:
            self._view.show_alert("non valido utente")
            return

        try:
            sequenza, peso= self._model.cerca_sequenza(utente_iniziale, L)
        except Exception as ex:
            self._view.show_alert(str(ex))
            return

        self._view.clear_result()
        self._view.add_result(f"punteggio totale = {peso}")
        self._view.add_result("sequenza trovata:")
        for utente in sequenza:
            self._view.add_result(str(utente))
        self._view.update_result()




        pass


