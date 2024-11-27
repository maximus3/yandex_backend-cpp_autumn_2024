from tortoise.contrib.pydantic import pydantic_model_creator

from enterprise.models import (
    User,
    Company,
    Job,
    Order,
)

UserSerializer = pydantic_model_creator(User)
CompanySerializer = pydantic_model_creator(Company)
JobSerializer = pydantic_model_creator(Job)
OrderSerializer = pydantic_model_creator(Order)
