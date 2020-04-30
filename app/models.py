import re
from datetime import datetime

from pytz import timezone
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

from app.sa_types.serialized_json import ImmutableSerializedJSON

Base = declarative_base()

gene_splitter = re.compile(r'[ \t\r\n]+')
drug_splitter = re.compile(r'[\t\r\n]+')


class GenesetGene(Base):
    __tablename__ = 'genesets_genes'

    geneset = Column('geneset', Integer, ForeignKey('genesets.id'), primary_key=True)
    gene = Column('gene', Integer, ForeignKey('genes.id'), primary_key=True)


class Gene(Base):
    __tablename__ = 'genes'

    id = Column('id', Integer, primary_key=True)
    symbol = Column('symbol', String(32), nullable=False)

    genesets = relationship('Geneset', secondary='genesets_genes', back_populates='genes')

    @staticmethod
    def create(sess, **kwargs):
        instance = Gene(**kwargs)
        sess.add(instance)
        return instance

    @staticmethod
    def resolve_set(sess, genes):
        genes = {gene.upper() for gene in genes if gene}
        instances = sess.query(Gene).filter(Gene.symbol.in_(tuple(genes))).all()
        found_genes = {instance.symbol for instance in instances}
        remaining_genes = genes - found_genes
        if remaining_genes:
            instances += [
                Gene.create(sess, symbol=gene)
                for gene in remaining_genes
            ]
            sess.commit()
        return instances

    def jsonify(self):
        return self.symbol


class Geneset(Base):
    __tablename__ = 'genesets'

    id = Column('id', Integer, primary_key=True)
    enrichrShortId = Column('enrichrShortId', String(255), nullable=False)
    enrichrUserListId = Column('enrichrUserListId', Integer, nullable=False)
    genes = relationship('Gene', secondary='genesets_genes', back_populates='genesets')
    descrShort = Column('descrShort', String(255), nullable=False)
    descrFull = Column('descrFull', Text, nullable=False)
    authorName = Column('authorName', String(255), nullable=False)
    authorAffiliation = Column('authorAffiliation', String(255))
    authorEmail = Column('authorEmail', String(255))
    showContacts = Column('showContacts', Integer, nullable=False, default=0)
    reviewed = Column('reviewed', Integer, nullable=False, default=0)
    source = Column('source', String(255), default=0)
    date = Column('date', DateTime, default=lambda: datetime.now(timezone('US/Eastern')).strftime('%Y-%m-%d %H:%M:%S'))
    meta = Column('meta', ImmutableSerializedJSON, default=0)

    @staticmethod
    def create(sess, genes=[], **kwargs):
        return Geneset(
            **kwargs,
            genes=Gene.resolve_set(sess, set(genes)),
        )

    def to_gmt(self):
        return '\t'.join([
            f'{self.id}: {self.descrShort}',
            self.descrFull,
            *[
                gene.symbol
                for gene in self.genes
            ],
        ])

    def jsonify(self, deep=True):
        ret = {
            'id': self.id,
            'enrichrShortId': self.enrichrShortId,
            'enrichrUserListId': self.enrichrUserListId,
            'descrShort': self.descrShort,
            'descrFull': self.descrFull,
            'authorName': self.authorName,
            'authorAffiliation': self.authorAffiliation,
            'authorEmail': self.authorEmail,
            'showContacts': self.showContacts,
            'reviewed': self.reviewed,
            'source': self.source,
            'date': self.date,
            'meta': self.meta
        }
        if deep:
            ret['genes'] = sorted({gene.jsonify() for gene in self.genes})
        return ret


class DrugsetDrug(Base):
    __tablename__ = 'drugsets_drugs'

    drugset = Column('drugset', Integer, ForeignKey('drugsets.id'), primary_key=True)
    drug = Column('drug', Integer, ForeignKey('drugs.id'), primary_key=True)


class Drug(Base):
    __tablename__ = 'drugs'

    id = Column('id', Integer, primary_key=True)
    symbol = Column('symbol', String(256), nullable=False)

    drugsets = relationship('Drugset', secondary='drugsets_drugs', back_populates='drugs')

    @staticmethod
    def create(sess, **kwargs):
        instance = Drug(**kwargs)
        sess.add(instance)
        return instance

    @staticmethod
    def resolve_set(sess, drugs):
        drugs = {drug.lower() for drug in drugs if drug}
        instances = sess.query(Drug).filter(Drug.symbol.in_(tuple(drugs))).all()
        found_drugs = {instance.symbol for instance in instances}
        remaining_drugs = drugs - found_drugs
        if remaining_drugs:
            instances += [
                Drug.create(sess, symbol=drug)
                for drug in remaining_drugs
            ]
            sess.commit()
        return instances

    def jsonify(self):
        return self.symbol


class Drugset(Base):
    __tablename__ = 'drugsets'

    id = Column('id', Integer, primary_key=True)
    drugs = relationship('Drug', secondary='drugsets_drugs', back_populates='drugsets')
    descrShort = Column('descrShort', String(255), nullable=False)
    descrFull = Column('descrFull', Text, nullable=False)
    authorName = Column('authorName', String(255), nullable=False)
    authorAffiliation = Column('authorAffiliation', String(255))
    authorEmail = Column('authorEmail', String(255))
    showContacts = Column('showContacts', Integer, nullable=False, default=0)
    reviewed = Column('reviewed', Integer, nullable=False, default=0)
    source = Column('source', String(255), default=0)
    date = Column('date', DateTime, default=lambda: datetime.now(timezone('US/Eastern')).strftime('%Y-%m-%d %H:%M:%S'))
    meta = Column('meta', ImmutableSerializedJSON, default=0)
    category = Column('category', Integer, ForeignKey('categories.id'), nullable=False, default=1)

    @staticmethod
    def create(sess, drugs=[], **kwargs):
        return Drugset(
            **kwargs,
            drugs=Drug.resolve_set(sess, set(drugs)),
        )

    def to_gmt(self):
        return '\t'.join([
            f'{self.id}: {self.descrShort}',
            self.descrFull,
            *[
                drug.symbol
                for drug in self.drugs
            ],
        ])

    def jsonify(self, deep=True):
        ret = {
            'id': self.id,
            'descrShort': self.descrShort,
            'descrFull': self.descrFull,
            'authorName': self.authorName,
            'authorAffiliation': self.authorAffiliation,
            'authorEmail': self.authorEmail,
            'showContacts': self.showContacts,
            'reviewed': self.reviewed,
            'source': self.source,
            'date': self.date,
            'meta': self.meta,
            'category': self.category
        }
        if deep:
            ret['drugs'] = sorted({drug.jsonify() for drug in self.drugs})
        return ret


class Categories(Base):
    __tablename__ = 'categories'

    id = Column('id', Integer, primary_key=True)
    name = Column('name', String(255), nullable=False, default='all')
