from database.connection import Base
from sqlalchemy import Column, String, BigInteger, ForeignKey

class Consultation(Base):
    __tablename__ = 'consultations'

    id = Column(BigInteger, primary_key= True)
    client_id = Column(ForeignKey('clients.id'))
    consultation_date = Column(String(10), nullable= False)
    consultation_time = Column(String(5), nullable= False) 
    procedure = Column(String(60), nullable= False)
    description = Column(String(500))