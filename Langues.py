class Language:
    def __init__(self):
        self.language = 1
        # 1 for French, 2 for English, 3 for German
        self.vocab = ["Magasin", "Projets", "Recherches", "Doctrines", "Armée","Infrastructures", "Ressources"]

    def change_language(self, l, bg, shop):
        self.language = l
        if self.language == 1:
            self.vocab = ["Magasin", "Projets", "Recherches", "Doctrines", "Armée","Infrastructures", "Ressources"]
        if self.language == 2:
            self.vocab = ["Shop", "Projects", "Research", "Doctrins", "Army", "Infrastructures", "Resources"]
        if self.language == 3:
            self.vocab = ["Laden", "Projekten", "Forschung", "Doktrinen", "Militär","Infrastrukturen","Ressourcen"]
        shop.tabs_name = bg.l.vocab[0], bg.l.vocab[1], bg.l.vocab[2], bg.l.vocab[3]