from repositories.consultations_crud import ManagerConsultation
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from validations.validate_consultations import (
    validate_consultation_date,
    validate_consultation_time
    )


class ConsultationServices:
    def __init__(self, session):
        # gets the database connection from the consultations routes.
        self.manager = ManagerConsultation(session) 
        self.session = session

    
    def insert_consultation(
            self,
            client_id: int,
            consultation_date: str,
            consultation_time: str,
            procedure: str,
            description: str
            ):
        
        try:
            validate_consultation_date(consultation_date)
            validate_consultation_time(consultation_time)
            self.manager.register_Consultation(
                client_id,
                consultation_date,
                consultation_time,
                procedure,
                description
                )
            self.session.commit()            

        except ValueError as v:
            self.session.rollback()
            raise HTTPException(status_code = 422, detail = {'error': f'{v}'})

        except IntegrityError:
            raise HTTPException(status_code = 422, detail = {'error': 'client id not found'})

    
    def get_consultations_list(self, page: int = 1, limit: int = 10):
        return self.manager.get_consultations(page, limit)
    

    def searcher_consultations(self, search: str, page: int = 1, limit: int = 10):
        return self.manager.search_consultations(search, page, limit)
    

    def edit_consultations(
            self,
            id: int,
            consultation_date: str,
            consultation_time: str,
            procedure: str,
            description: str
            ):
        try:
            validate_consultation_date(consultation_date)
            validate_consultation_time(consultation_time)

            result = self.manager.update_consultations(
                id,
                consultation_date,
                consultation_time,
                procedure,
                description
                )
            
            # if no rows in the database have been changed, it will cause an error.
            if result.rowcount == 0:
                self.session.rollback()
                raise HTTPException(status_code = 404, detail = {'error': 'consultation not found'})
            
            self.session.commit()
        

        except ValueError as v:
            self.session.rollback()
            raise HTTPException(status_code = 422, detail = {'erro': f'{v}'})
    

    def remove_consultation(self, id: int):
        result = self.manager.delete_consultation(id)
        # if no rows in the database have been changed, it will cause an error.
        if result.rowcount == 0:
            self.session.rollback()
            raise HTTPException(status_code = 404, detail= {'error': 'consultation not found'})
        self.session.commit()