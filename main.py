from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from controller import loginController, placesController, productController, reconciliationContoroller
from db.database import Base, engine
from model.reconciliation import Reconciliation
from model.product import Product


Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(loginController.router)
app.include_router(placesController.router)
app.include_router(productController.router)
app.include_router(reconciliationContoroller.router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=['GET', 'POST', 'OPTIONS'],
    allow_headers=["Content-Type", 'Accept']
)

