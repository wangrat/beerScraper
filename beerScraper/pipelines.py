from scrapy.exceptions import DropItem
import json

class DuplicatesPipeline(object):

    def __init__(self):
        self.file = open('beers.jl', 'r')

        items = json.load(self.file)

        self.file.close()

        self.ids_seen = [beer['id'] for beer in items]

        self.ids_seen = set(self.ids_seen)


    def process_item(self, item, spider):
        if item['id'] in self.ids_seen:
            raise DropItem("Duplicate item found: %s" % item)
        else:
            self.ids_seen.add(item['id'])
            return item


class JsonWriterPipeline(object):

    def open_spider(self, spider):
        self.file = open('beers.jl', 'r')

        self.items = json.load(self.file)

        self.file.close()


    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + "\n"
        self.file.write(line)
        return item