from sqlalchemy import create_engine
from sqlalchemy import Column, Boolean, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///infotex.sqlite')

db_session = scoped_session(sessionmaker(bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()

class ListOrg(Base):
    __tablename__ = 'list_org'
    firm = Column(String(), primary_key=True)
    director = Column(String())
    inn_kpp = Column(String())
    capital = Column(String())
    employees = Column(String())
    founder = Column(String())
    date_reg = Column(String())
    status = Column(String())


    def __init__(self, firm=None, director=None, inn_kpp=None, capital=None,
                employees=None, founder=None, date_reg=None, status=None):
        self.firm = firm
        self.director = director
        self.inn_kpp = inn_kpp
        self.capital = capital
        self.employees = employees
        self.founder = founder
        self.date_reg = date_reg
        self.status = status

    def __repr__(self):
        return '<Company {} {} {} {} {} {} {} {}>'.format(self.firm, self.director, self.inn_kpp,
                                 self.capital, self.employee, self.founder)


class Habr(Base):
    __tablename__ = 'habr'
    id = Column(Integer(), primary_key=True)
    nick = Column(String())
    date = Column(String())
    title = Column(String())
    text = Column(String())


    def __init__(self, nick=None, date=None, title=None, text=None):
        self.nick = nick
        self.date = date
        self.title = title
        self.text = text


    def __repr__(self):
        return '<Habr {} {} {} {}>'.format(self.nick, self.date, self.title,
                                 self.text)



if __name__ == '__main__':
    Base.metadata.create_all(bind=engine)
