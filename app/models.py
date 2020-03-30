from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Geneset(Base):
  __tablename__ = 'genesets'
  #
  id = Column('id', Integer, primary_key=True)
  enrichrShortId = Column('enrichrShortId', String(255), nullable=False)
  enrichrUserListId = Column('enrichrUserListId', Integer, nullable=False)
  genes = Column('genes', Text, nullable=False)
  descrShort = Column('descrShort', String(255), nullable=False)
  descrFull = Column('descrFull', String(255), nullable=False)
  authorName = Column('authorName', String(255), nullable=False)
  authorAffiliation = Column('authorAffiliation', String(255))
  authorEmail = Column('authorEmail', String(255))
  showContacts = Column('showContacts', Integer, nullable=False, default=0)
  reviewed = Column('reviewed', Integer, nullable=False, default=0)
  source = Column('source', String(255), default=0)
  #
  def jsonify(self):
    return {
      'id': self.id,
      'enrichrShortId': self.enrichrShortId,
      'enrichrUserListId': self.enrichrUserListId,
      'genes': self.genes,
      'descrShort': self.descrShort,
      'descrFull': self.descrFull,
      'authorName': self.authorName,
      'authorAffiliation': self.authorAffiliation,
      'authorEmail': self.authorEmail,
      'showContacts': self.showContacts,
      'reviewed': self.reviewed,
      'source': self.source,
    }
