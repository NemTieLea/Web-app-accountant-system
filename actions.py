class Actions:
    def __init__(self, manager):
        self.manager = manager

    def saldo(self):
        state = self.manager.state
        stan_konta = int(input("> Podaj kwote do dodania lub odjecia na swoje saldo: "))
        if stan_konta == 0:
            print("> Podaj kwote wieksza lub mniejsza od 0")
            return
        state['caly_stan'] += stan_konta
        state['historia'].append(['saldo', stan_konta, state['caly_stan']])
        if state['caly_stan'] < 0:
            state['caly_stan'] -= stan_konta
            print("> Twoj calkowity stan konta nie moze byc na minusie. Podaj kwote ponownie")

    def sprzedaz(self):
        state = self.manager.state
        nazwa = input("> Podaj nazwe produktu: ")
        liczba_sztuk = int(input("> Podaj liczbe produktow: "))
        if liczba_sztuk <= 0:
            print(">> Liczba sprzedanych produktow musi byc wieksza od 0.")
            return
        if nazwa in state['slownik_produktow'] and state['slownik_produktow'][nazwa] >= liczba_sztuk:
            cena = state['cena_produktow'][nazwa] * liczba_sztuk
            print(f">> Sprzedaje {liczba_sztuk} sztuk '{nazwa}' za '{cena} 'pieniedzy.")
            state['slownik_produktow'][nazwa] -= liczba_sztuk
            state['caly_stan'] += cena
        else:
            print(f">> Niewystarczajaca liczba sztuk produktu.")
            return
        state['historia'].append(['sprzedaz', nazwa, liczba_sztuk])

    def zakup(self):
        state = self.manager.state
        nazwa = input("Podaj nazwe produktu: ")
        if nazwa in state['slownik_produktow']:
            cena = state['cena_produktow'][nazwa]
            liczba_sztuk = int(input("Podaj liczbe produktow: "))
            if liczba_sztuk <= 0:
                print(">> Liczba zakupionych produktow musi byc wieksza od 0.")
                return
            if state['caly_stan'] >= cena * liczba_sztuk:
                koszt = cena * liczba_sztuk
                print(f">> Zakupiono '{nazwa}' w liczbie {liczba_sztuk} sztuk za '{koszt}' pieniedzy")
                state['slownik_produktow'][nazwa] += liczba_sztuk
                state['caly_stan'] -= koszt
                state['historia'].append(['zakup', nazwa, liczba_sztuk])
            else:
                print("Niewystarczajaca ilosc pieniedzy")
                return
        else:
            liczba_sztuk = int(input("Podaj liczbe produktow: "))
            if liczba_sztuk <= 0:
                print(">> Liczba zakupionych produktow musi byc wieksza od 0.")
                return
            cena = int(input("Podaj cene jednego produktu: "))
            if cena <= 0:
                print(">> Cena musi byc wyzsza od 0")
                return
            koszt = cena * liczba_sztuk
            if state['caly_stan'] < koszt:
                print("Niewystarczajaca ilosc pieniedzy")
                return
            if nazwa not in state['slownik_produktow']:
                state['slownik_produktow'][nazwa] = 0
                state['cena_produktow'][nazwa] = cena
            state['slownik_produktow'][nazwa] += liczba_sztuk
            state['caly_stan'] -= koszt
            print(f">> Zakupiono '{nazwa}' w liczbie {liczba_sztuk} sztuk za '{koszt}' pieniedzy")
            state['historia'].append(['zakup', nazwa, liczba_sztuk])

    def konto(self):
        state = self.manager.state
        print(f">>Twoj aktualny stan konta to: {state['caly_stan']}")

    def lista(self):
        state = self.manager.state
        print("Lista dostepnych produktow:")
        for nazwa, liczba_sztuk in state['slownik_produktow'].items():
            print(f"Produkty oraz ilosc {nazwa:<35.35s} | {liczba_sztuk:>3.0f}")
        for nazwa, cena in state['cena_produktow'].items():
            print(f"Produkty oraz ceny: {nazwa:<35.35s} | {cena:>3.0f}")

    def magazyn(self):
        state = self.manager.state
        nazwa_produktu = input('Podaj nazwe produktu do sprawdzenia: ')
        if nazwa_produktu in state['slownik_produktow'] and state['slownik_produktow'][nazwa_produktu] > 0:
            print(f"""> Produkt '{nazwa_produktu}' jest dostepny. 
            ilosc: {state['slownik_produktow'][nazwa_produktu]}
            Cena za sztuke: {state['cena_produktow'][nazwa_produktu]}""")
        else:
            print(f"> Niestety, produkt '{nazwa_produktu}' jest niedostepny.")

    def przeglad(self):
        state = self.manager.state
        print(f"> Calkowita ilosc wprowadzonych komend: {len(state['historia'])}")
        try:
            wartosc_od = input("Wprowadz wartosc od (wcisnij enter dla calej listy): ")
            wartosc_do = input("Wprowadz wartosc do (wcisnij enter dla calej listy): ")
            if not wartosc_od.strip():
                wartosc_od = 0
            else:
                wartosc_od = int(wartosc_od)
            if not wartosc_do.strip():
                wartosc_do = len(state['historia'])
            else:
                wartosc_do = int(wartosc_do)
            if wartosc_od < 0 or wartosc_od > len(state['historia']):
                print(f"Nieprawidlowa wartosc. Musi byc pomiedzy 0 a {len(state['historia'])}")
                wartosc_od = 0
            if wartosc_do > len(state['historia']) or wartosc_od > wartosc_do:
                print(f"Nieprawidlowa wartosc. Musi byc pomiedzy {wartosc_od} a {len(state['historia'])}")
                wartosc_do = len(state['historia'])
            for entry in state['historia'][wartosc_od:wartosc_do]:
                print(entry)
        except ValueError:
            print("Nieprawidlowa wartosc. Prosze wpisac prawidlowa wartosc.")
        except Exception as e:
            print(f"Blad: {str(e)}")
