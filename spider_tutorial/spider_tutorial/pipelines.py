# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import logging
import pymongo
import sqlite3

class MongoDBPipeline:
    collection_name = 'transcripts'

    def open_spider(self, spider):
        logging.warning('Spider Opened! - Pipeline')
        self.client = pymongo.MongoClient("mongodb+srv://harsh:harsh@clusterwebscraping.jwfazqh.mongodb.net/?retryWrites=true&w=majority")
        self.db = self.client['My_Database']

    def close_spider(self, spider):
        self.client.close()
        logging.warning('Spider Closed! - Pipeline')

    def process_item(self, item, spider):
        self.db[self.collection_name].insert(item)
        return item


class SQLitePipeline:

    def open_spider(self, spider):
        logging.warning('Spider Opened! - Pipeline')
        self.connection = sqlite3.connect('transcripts.db')
        self.c = self.connection.cursor()
        # above is a cursor to execute queries
        try:
            self.c.execute('''
                CREATE TABLE transcripts(
                    title TEXT,
                    plot TEXT,
                    transcript TEXT,
                    url TEXT
                )
            ''')
            self.connection.commit()
        except sqlite3.OperationalError:
            pass

    def close_spider(self, spider):
        self.connection.close()
        logging.warning('Spider Closed! - Pipeline')

    def process_item(self, item, spider):
        self.c.execute('''
            INSERT INTO transcripts (title,plot,transcript,url) VALUES(?,?,?,?)
        ''', (
            item.get('title'),
            item.get('plot'),
            item.get('transcript'),
            item.get('url'),
        ))
        self.connection.commit()
        return item