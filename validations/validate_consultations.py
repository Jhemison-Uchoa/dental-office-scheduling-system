from pydantic import constr
from datetime import datetime

# accepts only numbers and the character /
ConsultationDate = constr(min_length= 10, max_length= 10, pattern = r'^[0-9/]+$')
def validate_consultation_date(consultation_date: str) -> bool:
    # function to transform consultation date into date format with validations.
    if not datetime.strptime(f'{consultation_date}', '%d/%m/%Y').date():
        raise ValueError()
        
# accepts only numbers and the character :
ConsultationTime = constr(min_length= 5, max_length= 5, pattern = r'^[0-9:]+$')
def validate_consultation_time(consultation_time: str) -> bool:
    # function to transform consultation time into time format with validations.
    if not datetime.strptime(f'{consultation_time}', '%H:%M').time():
        raise ValueError()

ProcedureStr = constr(min_length= 3, max_length= 60)


DescriptionStr = constr(min_length= 3, max_length= 500)