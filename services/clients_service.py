from repositories.clients_crud import ManagerClient
from fastapi import HTTPException
from validations.validate_clients import validate_cpf, validate_phone_number
from sqlalchemy.exc import IntegrityError

class ClientServices:
    def __init__(self, session):
        # gets the database connection from the clients routes.
        self.session = ManagerClient(session)
        self.manager = session


    def insert_clients(self, name: str, age: str, cpf: str, phone_number: str, email: str):
        try:            
            validate_cpf(cpf)
            validate_phone_number(phone_number)
            self.session.register_clients(name, age, cpf, phone_number, email)
            self.manager.commit()
        
        except ValueError as e:
            self.manager.rollback()
            raise HTTPException(status_code = 422, detail= {'error': f'{e}'})
     
        except IntegrityError:
            self.manager.rollback()
            raise HTTPException(status_code = 422, detail = {'error': 'repeated data'})


    def get_clients_list(self, page: int = 1, limit: int = 10):
        return self.session.get_clients(page, limit)

    
    def find_clients(self, search: str, page: int = 1, limit: int = 10):
        return self.session.search_clients(search, page, limit)


    def edit_clients(self, id: int, name: str, age: str, cpf: str, phone_number: str, email: str):
        try:
            validate_cpf(cpf)
            validate_phone_number(phone_number)

            result = self.session.update_clients(id, name, age, cpf, phone_number, email)
            # if no rows in the database have been changed, it will cause an error.
            if result.rowcount == 0:
                raise HTTPException(status_code = 404, detail = {'erro': 'user id not found'}) 
            self.manager.commit()

         
        except ValueError:
            self.manager.rollback()
        

    def delete_clients(self, id: int):
        result = self.session.remove_client(id)

        # if no rows in the database have been changed, it will cause an error.
        if result.rowcount == 0:
            self.manager.rollback()
            raise HTTPException(status_code= 404, detail= {'error': 'user not found'})    
            
        self.manager.commit()