from database.connection import create_tables
import models
from fastapi import FastAPI
from routes.route_clients import router as router_clients
from routes.route_consultations import router as router_consultations

app = FastAPI()

app.on_event('create_tables')

app.include_router(router_clients)
app.include_router(router_consultations)