from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base 

Base = declarative_base()

class GlossaryModel(Base):
    __tablename__ = 'terms'
    id = Column(Integer, 
                primary_key=True, 
                autoincrement=True,
                unique=True,
                )
    term = Column(String)
    term_en = Column(String)
    desc_en = Column(String)
    desc_other = Column(String)
    notes_en = Column(String)
    notes_other = Column(String)
    approval_status = Column(String)

# Initialize database and session outside of the class
engine = create_engine('sqlite:///Data/glossary.db', echo=True)
Session = sessionmaker(bind=engine, autoflush=True, expire_on_commit=True) 
session = Session() 

Base.metadata.create_all(engine)
