import config


class Beer:
    """
    Just a class for my beer
    """

    def __init__(self, name, country="Russia", brewery="some brewery", ibu=5, abv=10,
                 untappd_link="https://untappd.com/b/poehali-nebelyj-medved/1572703", type="IPA", bottled=False):
        """
        :param name: string
        :param country: string
        :param brewery: string
        :param ibu: int
        :param abv: int
        :param untappd_link: string
        :param type: string
        :param bottled: boolean

        PLEASE PUT BOTTLED AND UNBOTTLED BEERS INTO DIFFERENT LISTS
        """
        self.name = name
        self.country = country
        self.brewery = brewery
        self.ibu = ibu
        self.abv = abv
        self.untappd_link = untappd_link
        self.type = type  # TYPE -  Ipa, Apa, Trippel and so on
        self.bottled = bottled

    def _init__(self, name):
        self.name = name
        self.country = "Russia"
        self.brewery = "some brewery"
        self.ibu = 5
        self.abv = 10
        self.untappd_link = "http://www.no_link.com"
        self.type = "IPA"
        self.bottled = False

    def toString(self):
        result = "[" + self.name + "]" + "(" + self.untappd_link + ")" + config.flag(
            self.country) + "\n" + self.type + "\n" + "IBU: " + str(self.ibu) + ", ABV: " + str(
            self.abv) + '%\n' + self.brewery + '\n\n'
        return result
