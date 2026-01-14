from fastapi import APIRouter, Depends
from pydantic import BaseModel, EmailStr
from services.clients_service import ClientServices
from database.connection import get_connection
from validations.validate_clients import NameStr, CpfStr, PhoneNumberStr


router = APIRouter()


class ClientsInput(BaseModel):
    name: NameStr
    age : int
    cpf : CpfStr
    phone_number : PhoneNumberStr
    email : EmailStr


class ClientsIdInput(BaseModel):
    id : int
    name : NameStr
    age : int
    cpf : CpfStr
    phone_number: PhoneNumberStr
    email : EmailStr


@router.post('/register_clients')
def register_clients(Clients: ClientsInput, session = Depends(get_connection)):
    # obtain the connection to execute the request  
    manager = ClientServices(session)
    manager.insert_clients(Clients.name, Clients.age, Clients.cpf, Clients.phone_number, Clients.email)
    return {'msg': 'successfully registered client'}


@router.get('/get_clients')
def get_clients(page: int = 1, limit: int = 10, session = Depends(get_connection)):
    # obtain the connection to execute the request
    manager = ClientServices(session)
    return manager.get_clients_list(page, limit)


@router.get('/search_clients')
def search_clients(search: str, page: int = 1, limit: int = 10, session = Depends(get_connection)):
    # obtain the connection to execute the request
    manager = ClientServices(session)
    return manager.find_clients(search, page, limit)


@router.put('/update_clients')
def update_clients(Clients: ClientsIdInput, session = Depends(get_connection)):
    # obtain the connection to execute the request
    manager = ClientServices(session)
    manager.edit_clients(Clients.id, Clients.name, Clients.age, Clients.cpf, Clients.phone_number, Clients.email)
    return {'msg': 'successfully updated client'} 


@router.delete('/delete_clients')
def delete_clients(id: int, session = Depends(get_connection)):
    # obtain the connection to execute the request
    manager = ClientServices(session)
    manager.delete_clients(id)
    return {'msg': 'successfully deleted client'}