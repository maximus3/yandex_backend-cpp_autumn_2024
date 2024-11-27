from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse
from tortoise.expressions import Q
from tortoise.contrib.fastapi import register_tortoise

from config import TORTOISE_ORM


from enterprise.models import (
    Company,
    Job,
    Order,
    User,
)
from enterprise.serializers import (
    CompanySerializer,
    JobSerializer,
    OrderSerializer,
    UserSerializer,
)

app = FastAPI()

register_tortoise(
    app,
    config=TORTOISE_ORM,
    generate_schemas=False,
    add_exception_handlers=True,
)

@app.get("/")
async def home_view():
    return HTMLResponse("<h1>Hello Student!</h1>")


@app.get("/v1/users/", response_model=list[UserSerializer])
async def list_users_v1(search: str | None = Query(None)):
    query = User.all()

    if search:
        query = query.filter(
            (
                Q(first_name__istartswith=search)
                | Q(last_name__istartswith=search)
            )
        ).order_by("last_name")

    return await UserSerializer.from_queryset(query)


@app.get("/v2/users/", response_model=list[UserSerializer])
async def list_users_v2(search: str | None = Query(None)):
    query = User.all().order_by("last_name")

    if search:
        query = query.filter(
            Q(first_name__icontains=search)
            | Q(last_name__icontains=search)
            | Q(phone_number__istartswith=search)
            | Q(email__icontains=search)
        )

    return await UserSerializer.from_queryset(query)


@app.get("/companies", response_model=list[JobSerializer])
async def list_companies(search: str | None = Query(None)):
    query = Company.all()

    if search:
        query = query.filter(
            Q(title__istartswith=search) | Q(address__icontains=search)
        ).order_by("title")

    return await CompanySerializer.from_queryset(query)


@app.get("/jobs", response_model=list[JobSerializer])
async def list_jobs(search: str | None = Query(None)):
    query = Job.all()

    if search:
        query = query.filter(Q(title__istartswith=search)).order_by("title")

    return await JobSerializer.from_queryset(query)

@app.get("/pending_orders", response_model=list[OrderSerializer])
async def list_pending_orders():
    orders = Order.filter(status='Pending').order_by("order_date").limit(10).all()
    return await OrderSerializer.from_queryset(orders)
