import config


class Beer:
    """
    Just a class for my beer
    """

    def __init__(self, name, country, brewery, ibu, abv, untappd_link, type):
        self.name = name
        self.country = country
        self.brewery = brewery
        self.ibu = ibu
        self.abv = abv
        self.untappd_link = untappd_link
        self.type = type

    def toString(self):
        result = "[" + self.name + "]" + "(" + self.untappd_link + ")" + config.flag(
            self.country) + "\n" + self.type + "\n" + "IBU: " + str(self.ibu) + ", ABV: " + str(
            self.abv) + '%\n' + self.brewery + '\n\n'
        return result
