from fastapi import APIRouter, Depends
from pydantic import BaseModel
from database.connection import get_connection
from services.consultations_service import ConsultationServices
from validations.validate_consultations import (
    ProcedureStr,
    DescriptionStr,
    ConsultationDate,
    ConsultationTime
    )

router = APIRouter()


class ConsultationInput(BaseModel):
    client_id: int
    consultation_date: ConsultationDate
    consultation_time: ConsultationTime
    procedure: ProcedureStr
    description: DescriptionStr


class ConsultationIdInput(BaseModel):
    id: int
    consultation_date: ConsultationDate
    consultation_time: ConsultationTime
    procedure: ProcedureStr
    description: DescriptionStr


@router.post('/register_consultations')
def register_consultations(consultations: ConsultationInput, session = Depends(get_connection)):
    # obtain the connection to execute the request
    manager = ConsultationServices(session)
    manager.insert_consultation(
        consultations.client_id,
        consultations.consultation_date,
        consultations.consultation_time,
        consultations.procedure,
        consultations.description
        )
    return {'msg': 'consultation registered with sucessfuly'}


@router.get('/get_consultation')
def get_consultations(page: int = 1, limit: int = 10, session = Depends(get_connection)):
    # obtain the connection to execute the request
    manager = ConsultationServices(session)
    return manager.get_consultations_list(page, limit)


@router.get('/search_consultation')
def search_consultation(search, page: int = 1, limit: int = 10, session = Depends(get_connection)):
    # obtain the connection to execute the request
    manager = ConsultationServices(session)
    return manager.searcher_consultations(search, page, limit)


@router.put('/update_consultaton')
def update_consultations(consultations: ConsultationIdInput, session = Depends(get_connection)):
    # obtain the connection to execute the request
    manager = ConsultationServices(session)
    manager.edit_consultations(
        consultations.id,
        consultations.consultation_date,
        consultations.consultation_time,
        consultations.procedure,
        consultations.description
    )
    return {'msg': 'consultation updated with sucessfuly'}


@router.delete('/remove_consultation')
def delete_consultation(id: int, session = Depends(get_connection)):
    # obtain the connection to execute the request
    manager = ConsultationServices(session)
    manager.remove_consultation(id)
    return {'msg': 'consultation deleted with sucessfuly'}