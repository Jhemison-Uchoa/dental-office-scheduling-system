from models.clients_model import Client
from sqlalchemy import select, update, delete, func, or_, cast, String


class ManagerClient:
    def __init__(self, session):
        # gets the database connection from the clients service. 
        self.session = session

    
    def register_clients(self, name: str, age: str, cpf: str, phone_number: str, email: str):
        # save clients answers from clients_service code into the database. 
        new_client = Client(name= name, age= age, cpf= cpf, phone_number= phone_number, email= email)
        self.session.add(new_client)


    def get_clients(self, page: int = 1, limit: int = 10) -> dict:
        if limit > 100:
            limit = 100

        if page <= 0:
            page = 1
        
        # calculate how many clients to skip based on the selected page
        offset = (page - 1) * limit
        # count how many clients has into the database
        records = self.session.scalar(select(func.count()).select_from(Client))
        # show all clients data
        data = self.session.scalars(select(Client).order_by(Client.id.desc()).offset(offset).limit(limit)).all()

        return {
            'page': page,
            'limit': limit,
            'records': records,
            'data': data
        }
    

    def search_clients(self, search: str, page: int = 1, limit: int = 10):
        if limit > 100:
            limit = 100

        if page <= 0:
            page = 1

        # calculate how many clients to skip based on the selected page
        offset = (page - 1) * limit
        """
        count how many clients has into the database filtering by
        client name, client cpf, client age
        without distinguishing between uppercase and lowercase letters
        """
        records = self.session.scalar(select(func.count())
                .where(or_(Client.name.ilike(f'%{search}%'), Client.cpf.ilike(f'%{search}%'),
                           cast(Client.age, String).ilike(f'%{search}%'))))
        
        # show all clients data filtering by client name, client cpf, client age  
        data = self.session.scalars(select(Client).where(or_(Client.name.ilike(f'%{search}%'), 
            Client.cpf.ilike(f'%{search}%'), cast(Client.age, String).ilike(f'%{search}')))
            .order_by(Client.name).offset(offset).limit(limit)).all()
        
        return {
            'page': page,
            'limit': limit,
            'records': records,
            'data': data
        }
        
    
    def update_clients(self, id: int, name: str, age: str, cpf: str, phone_number: str, email: str):
        # update client data 
        update_client = update(Client).where(Client.id == id).values(
        name= name,
        age= age,
        cpf= cpf,
        phone_number= phone_number,
        email= email
    )
        return self.session.execute(update_client)


    def remove_client(self, id: int):
        # delete client data by id
        remove_clients = delete(Client).where(Client.id == id)
        return self.session.execute(remove_clients)  