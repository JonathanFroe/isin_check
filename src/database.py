import online_check

from datetime import datetime, timedelta, date

from sqlalchemy import create_engine
from sqlalchemy.sql import text

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Float, String, Date

Base = declarative_base()
class ISIN(Base):
    __tablename__='isin'

    isin = Column(String(12), primary_key=True)
    name = Column(String(500))
    wkn = Column(String(6))
    url = Column(String(500))
    vola_1m = Column(Float)
    vola_3m = Column(Float)
    vola_1y = Column(Float)
    vola_3y = Column(Float)
    vola_5y = Column(Float)
    vola_10y = Column(Float)
    perf_1m = Column(Float)
    perf_3m = Column(Float)
    perf_1y = Column(Float)
    perf_3y = Column(Float)
    perf_5y = Column(Float)
    perf_10y = Column(Float)
    tag1 = Column(String(120), default = "New")
    tag2 = Column(String(120), default = "")
    tag3 = Column(String(120), default = "")
    lastupdate = Column(Date)
    
    def update(self, name, wkn, url, vola, perf):
        self.name = name
        self.wkn = wkn
        self.url = url
        self.vola_1m = vola[0]
        self.vola_3m = vola[1]
        self.vola_1y = vola[2]
        self.vola_3y = vola[3]
        self.vola_5y = vola[4]
        self.vola_10y = vola[5]
        self.perf_1m = perf[0]
        self.perf_3m = perf[1]
        self.perf_1y = perf[2]
        self.perf_3y = perf[3]
        self.perf_5y = perf[4]
        self.perf_10y = perf[5]
        self.lastupdate = datetime.now()

    def change_tag1(self, new_tag):
        self.tag1 = new_tag
        
    def change_tag2(self, new_tag):
        self.tag2 = new_tag
        
    def change_tag3(self, new_tag):
        self.tag3 = new_tag
        
    def check_timedelta(self, delta_days):
        now = date.today()
        if now - self.lastupdate > timedelta(days=delta_days):
            return True
        return False
 
session = None 
engine = None          
def init_db(filename):
    global session, engine
    print(filename)
    engine = create_engine('sqlite:///'+filename, echo=False) #todo turn of echo
    
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind = engine)
    session = Session()

def close_db():
    global session, engine
    if session is not None and engine is not None:
        session.close()
        engine.dispose()

from sqlalchemy.orm import sessionmaker

def get_isinobject(isin):
    return session.query(ISIN).filter_by(isin=isin).first()

def get_all_data(sortedby, desc):
    if desc:
        return session.query(ISIN).order_by(text(sortedby + " desc")).all()
    else:
        return session.query(ISIN).order_by(sortedby).all()

def add_to_database(isin, tmpsession):
    isinobject = tmpsession.query(ISIN).filter_by(isin=isin).first()
    if isinobject is not None:
        return False
    name, wkn, url, vola, perf = online_check.get_data(isin)
    if name is not None and wkn is not None and url is not None and vola is not None and perf is not None:
        for i in range(len(vola)):
            if vola[i] is None:
                vola[i] = 0
        for i in range(len(perf)):
            if perf[i] is None:
                perf[i] = 0
        new_isin = ISIN(isin=isin,  name = name, wkn = wkn, url = url, vola_1m = vola[0], vola_3m = vola[1], vola_1y = vola[2], vola_3y = vola[3], vola_5y = vola[4], vola_10y = vola[5], perf_1m = perf[0], perf_3m = perf[1], perf_1y = perf[2], perf_3y = perf[3], perf_5y = perf[4], perf_10y = perf[5], lastupdate=datetime.now())
        tmpsession.add(new_isin)
        tmpsession.commit()
        return True
    return False

def delete_from_database(isin):
    isinobject = session.query(ISIN).filter_by(isin=isin).first()
    if isinobject is None:
        return False
    session.delete(isinobject)
    session.commit()
    return True

def change_tag_in_database(isin, new_tag, tagnumber):
    isinobject = session.query(ISIN).filter_by(isin=isin).first()
    if isinobject is None:
        return False
    if tagnumber==1:
        isinobject.change_tag1(new_tag)
    if tagnumber==2:
        isinobject.change_tag2(new_tag)
    if tagnumber==3:
        isinobject.change_tag3(new_tag)
    session.commit()

def update_in_database(isin, create_new=True):
    TempSession = sessionmaker(bind = engine)
    tmpsession = TempSession()
    isinobject = tmpsession.query(ISIN).filter_by(isin=isin).first()
    if isinobject is None:
        if create_new:
            return add_to_database(isin, tmpsession)
        return False
    name, wkn, url, vola, perf = online_check.get_data(isin)
    if  name is not None and wkn is not None and url is not None and vola is not None and perf is not None:
        isinobject.update(name, wkn, url, vola, perf)
        tmpsession.commit()
        return True
    return False
