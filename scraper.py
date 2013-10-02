from urllib2 import urlopen
import re
import time

class Forex():

    url = "http://www.forexrate.co.uk/"
    duration = 30
    train = 'data/train.csv'
    last_scrape = time.time()

    @classmethod
    def current_rates(self):
        self.last_scrape = time.time()
        html = urlopen(self.url).read()
        rate_names = ["GBPUSD_rate", "EURUSD_rate", "GBPEUR_rate", "AUDUSD_rate", "NZDUSD_rate"]
        rates = []
        for name in rate_names:
            regex = 'span id=\"{0}\">(.*)<\/span> <img'.format(name)
            match = re.search(regex, html)
            rate = match.groups()[0]
            rates.append(rate)
        return rates

    @classmethod
    def write(self, data):
        """
        Accepts a list of data and writes it to the training file.
        """
        timestamp = str(int(self.last_scrape))
        string = "\n" + timestamp + "," + ",".join(data)
        with open(self.train, 'a') as myfile:
            myfile.write(string)

    @classmethod
    def scrape(self):
        """
        Main method to scrape the site on a loop.
        """
        while True:
            rates = Forex.current_rates()
            self.write(rates)
            until_next_scrape = (self.last_scrape + 30) - time.time()
            time.sleep(until_next_scrape)

if __name__ == "__main__":
    Forex.scrape()
