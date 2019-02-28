from scrapy.exceptions import DropItem
import json

class DuplicatesPipeline(object):

    def __init__(self):
        self.file = open('beers.json', 'r')

        beers = json.load(self.file)

        self.file.close()

        self.ids_seen = [beer['id'] for beer in beers['beers']]

        self.ids_seen = set(self.ids_seen)

    def process_item(self, item, spider):
        if item['id'] in self.ids_seen:
            raise DropItem("Duplicate item found: %s" % item)
        else:
            self.ids_seen.add(item['id'])
            return item


class JsonWriterPipeline(object):

    def __init__(self):
        self.file = open('beers.json', 'r')

        self.beers = json.load(self.file)

        self.file.close()


    def close_spider(self, spider):
        self.file = open('beers.json', 'w+')

        self.file.write(json.dumps(self.beers))

        self.file.close()

    def process_item(self, item, spider):
        self.beers['beers'].append(dict(item))
        self.beers['count'] += 1
        return item
