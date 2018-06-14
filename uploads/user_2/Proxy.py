class Implementacja:
    atrybucik = 'K5g9'

    def princik(self):
        print("Twój atrybucik to: {}".format(self.atrybucik))

    def pobieranko_atrybuciku(self):
        self.atrybucik = input("Podaj nową wartość atrybuciku: ")


class Proxy:

    def __init__(self):
        self.__implementacja = Implementacja()

    def princik(self): self.__implementacja.princik()
    def pobieranko_atrybuciku(self): self.__implementacja.pobieranko_atrybuciku()


class BardziejPythonoweProxy:

    def __init__(self):
        self.__implementacja = Implementacja()

    def __getattr__(self, name):
        return getattr(self.__implementacja, name)


p = BardziejPythonoweProxy()
p.princik()
p.pobieranko_atrybuciku()
p.princik()
