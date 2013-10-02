from urllib2 import urlopen
import re
import time
import logging
logging.basicConfig(filename='logs/system.log',level=logging.DEBUG)

class Forex():

    url = "http://www.forexrate.co.uk/"
    duration = 300
    train = 'data/train.csv'
    last_scrape = time.time()
    log = logging.getLogger('Forex')

    @classmethod
    def current_rates(self):
        self.last_scrape = time.time()
        self.log.info("Beginning scrape. last_scrape={0}".format(self.last_scrape))
        html = urlopen(self.url).read()
        rate_names = ["GBPUSD_rate", "EURUSD_rate", "GBPEUR_rate", "AUDUSD_rate", "NZDUSD_rate"]
        rates = []
        for name in rate_names:
            regex = 'span id=\"{0}\">(.*)<\/span> <img'.format(name)
            match = re.search(regex, html)
            if match:
                rate = match.groups()[0]
                rates.append(rate)
            else:
                self.log.error("There were no match groups for regex '{0}'".format(regex))
                rates.append('') # so that it puts in a comma into the train.csv file
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
            until_next_scrape = (self.last_scrape + self.duration) - time.time()
            if until_next_scrape > 0:
                time.sleep(until_next_scrape)
            else:
                self.log.warn("It took longer than {0} seconds to run the scrape. It took {1} seconds".format(self.duration, (time.time() - self.last_scrape)))

if __name__ == "__main__":
    Forex.scrape()
