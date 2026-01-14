from sqlalchemy import select, update, delete, func, or_
from models.consultations_model import Consultation


class ManagerConsultation:
    def __init__(self, session):
        # gets the database connection from the consultations service.
        self.session = session
        
    
    def register_Consultation(
        self,
        client_id : int,
        consultation_date: str,
        consultation_time: str,
        procedure: str,
        description: str 
    ):
        # save clients answers from consultations_service code into the database.
        new_consultation = Consultation(
            client_id = client_id,
            consultation_date = consultation_date,
            consultation_time = consultation_time,
            procedure = procedure,
            description = description
        )
        return self.session.add(new_consultation)
    

    def get_consultations(self, page: int = 1, limit: int = 10) -> dict:
        if limit > 100:
            limit = 100

        if page <= 0:
            page = 1

        # calculate how many consultations to skip based on the selected page
        offset = (page - 1) * limit
        # count how many consultations has into the database
        records = self.session.scalar(select(func.count()).select_from(Consultation))

        # show all consultations data
        data = self.session.scalars(select(Consultation).order_by(Consultation.consultation_date, 
        Consultation.consultation_time).offset(offset).limit(limit)).all()

        return {
            'page': page,
            'limit': limit,
            'records': records,
            'data': data
        }
    

    def search_consultations(self, search: str, page: int = 1, limit: int = 10) -> dict:
        if limit > 100:
            limit = 100

        if page <= 0:
            page = 1

        # calculate how many clients to skip based on the selected page
        offset = (page - 1) * limit
        """
        count how many consultations has into the database filtering by
        consultation date, consultation time, consultation procedure
        without distinguishing between uppercase and lowercase letters
        """
        records = self.session.scalar(select(func.count()).select_from(Consultation)
               .where(or_(Consultation.consultation_date.ilike(f'%{search}%'), 
               Consultation.consultation_time.ilike(f'%{search}%'), Consultation.procedure.ilike(f'%{search}%'))))
        
        # show all consultations data filtering by consultation date, consultation time and consultation procedure
        data = self.session.scalars(select(Consultation).order_by(Consultation.consultation_date.desc(),
                  Consultation.consultation_time.desc())
                  .where(or_(Consultation.consultation_date.ilike(f'%{search}%'),
                             Consultation.consultation_time.ilike(f'%{search}%'),
                             Consultation.procedure.ilike(f'%{search}%'))).offset(offset).limit(limit)).all()

        return {
            'page': page,
            'limit': limit,
            'records': records,
            'data': data
        }

    
    def update_consultations(
            self,
            id: int,
            consultation_date: str,
            consultation_time: str,
            procedure: str,
            description: str
    ):
        # update consultation data 
        update_consultation = update(Consultation).where(Consultation.id == id).values(
            consultation_date = consultation_date,
            consultation_time = consultation_time,
            procedure = procedure,
            description = description
       )
        return self.session.execute(update_consultation)
    
    
    def delete_consultation(self, id: int):
        # delete consultation data by id
        remove_consultation = delete(Consultation).where(Consultation.id == id)
        return self.session.execute(remove_consultation)