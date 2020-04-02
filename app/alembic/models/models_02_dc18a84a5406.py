import re
from datetime import datetime

from pytz import timezone
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

from app.sa_types.scalarlist import ScalarListType

Base = declarative_base()

gene_splitter = re.compile(r'[ \t\r\n]+')
drug_splitter = re.compile(r'[\t\r\n]+')


class Geneset(Base):
    __tablename__ = 'genesets'
    #
    id = Column('id', Integer, primary_key=True)
    enrichrShortId = Column('enrichrShortId', String(255), nullable=False)
    enrichrUserListId = Column('enrichrUserListId', Integer, nullable=False)
    genes = Column('genes', ScalarListType(str, separator='\t', splitter=gene_splitter), nullable=False)
    descrShort = Column('descrShort', String(255), nullable=False)
    descrFull = Column('descrFull', String(255), nullable=False)
    authorName = Column('authorName', String(255), nullable=False)
    authorAffiliation = Column('authorAffiliation', String(255))
    authorEmail = Column('authorEmail', String(255))
    showContacts = Column('showContacts', Integer, nullable=False, default=0)
    reviewed = Column('reviewed', Integer, nullable=False, default=0)
    source = Column('source', String(255), default=0)
    date = Column('date', DateTime, default=lambda: datetime.now(timezone('US/Eastern')).strftime('%Y-%m-%d %H:%M:%S'))

    #
    def jsonify(self):
        return {
            'id': self.id,
            'enrichrShortId': self.enrichrShortId,
            'enrichrUserListId': self.enrichrUserListId,
            'genes': sorted(set(self.genes)),
            'descrShort': self.descrShort,
            'descrFull': self.descrFull,
            'authorName': self.authorName,
            'authorAffiliation': self.authorAffiliation,
            'authorEmail': self.authorEmail,
            'showContacts': self.showContacts,
            'reviewed': self.reviewed,
            'source': self.source,
            'date': self.date
        }


class Drugset(Base):
    __tablename__ = 'drugsets'
    #
    id = Column('id', Integer, primary_key=True)
    drugs = Column('drugs', ScalarListType(str, separator='\t', splitter=drug_splitter), nullable=False)
    descrShort = Column('descrShort', String(255), nullable=False)
    descrFull = Column('descrFull', String(255), nullable=False)
    authorName = Column('authorName', String(255), nullable=False)
    authorAffiliation = Column('authorAffiliation', String(255))
    authorEmail = Column('authorEmail', String(255))
    showContacts = Column('showContacts', Integer, nullable=False, default=0)
    reviewed = Column('reviewed', Integer, nullable=False, default=0)
    source = Column('source', String(255), default=0)
    date = Column('date', DateTime, default=lambda: datetime.now(timezone('US/Eastern')).strftime('%Y-%m-%d %H:%M:%S'))

    #
    def jsonify(self):
        return {
            'id': self.id,
            'drugs': sorted(set(self.drugs)),
            'descrShort': self.descrShort,
            'descrFull': self.descrFull,
            'authorName': self.authorName,
            'authorAffiliation': self.authorAffiliation,
            'authorEmail': self.authorEmail,
            'showContacts': self.showContacts,
            'reviewed': self.reviewed,
            'source': self.source,
            'date': self.date
        }
