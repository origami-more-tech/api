from fastapi import FastAPI
from user.router import router as user_router
from office.router import router as office_router
from atm.router import router as atm_router
from fastapi.middleware.cors import CORSMiddleware

# To run project run commands below from api/ dir
# export PYTHONPATH=$(pwd)/src
# uvicorn src.main:app --host 0.0.0.0 --port 8080 --reload
# and checkout in your browser http://0.0.0.0:8080/docs

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router, prefix="/user")
app.include_router(office_router, prefix="/office")
app.include_router(atm_router, prefix="/atm")
