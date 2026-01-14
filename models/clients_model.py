from database.connection import Base
from sqlalchemy import Column, Integer, String, CheckConstraint, CHAR
from sqlalchemy.orm import relationship


class Client(Base):
    __tablename__ = 'clients'

    id = Column(Integer, primary_key= True)
    name = Column(String(50), nullable= False)
    age = Column(Integer, CheckConstraint('age > 0 and age < 120'), nullable= False)
    cpf = Column(CHAR(11), nullable= False, unique= True)
    phone_number = Column(CHAR(10), nullable= False, unique= True)
    email = Column(String(65), nullable= False, unique= True)
    
    consultations = relationship('Consultation', cascade= 'all, delete-orphan')