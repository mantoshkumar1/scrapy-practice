# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import logging

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker

from database_setup import engine
from models import Quotes, Author


class ScrapersPipeline:
    """ScrapersPipeline pipeline is for storing scraped items in the database"""

    def __init__(self, db_engine=engine):
        """Initializes sessionmaker"""
        self.engine = db_engine
        self.logger = logging.getLogger(__name__)

    def open_spider(self, spider):
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def close_spider(self, spider):
        self.session.close()

    def process_item(self, item, spider):
        """Save models data in the database.
        This method is called for every item pipeline component.
        """

        # Get/create Author instance using unique fields of Author
        is_exist, author = self._get_db_instance(Author, name=item.get('name'))
        if not is_exist:
            author.author_url = item.get('author_url', '')
            self.session.add(author)
            self.safely_commit(author)

        # create Quotes instance using unique fields of Author
        quote = Quotes()
        quote.content = item.get('content')
        quote.tags = item.get('tags', '')
        quote.author_id = author.id
        self.session.add(quote)
        self.safely_commit(quote)

        return item

    def _get_db_instance(self, obj, **kwargs):
        """
        Get/create obj model instance using unique fields of db model.
        If obj filtered by kwargs exist then return it otherwise create and
        return an object with given keyword args.
        :parameter
        obj : is the sql alchemy model object which existence is being checked.
        kwargs: should ideally contain unique keyword-ed fields of obj model.
        :returns
        boolean and
        sql alchemy model object: First/new instance of model object
        """
        db_obj = (
            self.session.query(obj)
                .filter_by(**kwargs)
                .first()
        )

        # if db_obj does not exist then create an instance of
        # obj model and return is_existed=False and created instance.
        # otherwise return is_existed=True and the existing obj instance.
        if not db_obj:
            return False, obj(**kwargs)
        return True, db_obj

    def safely_commit(self, model_instance):
        try:
            self.session.commit()
        except IntegrityError:
            self.session.rollback()
            self.logger.info(
                f"Database IntegrityError: {model_instance} is not committed")
            raise
