from app.accounts.routes import router as accounts_router
from app.project.routes import router as project_router
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_pagination import add_pagination

origins = [
    "http://localhost:8000",
    "http://localhost:5173",
]

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_origin_regex="http://localhost:*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

add_pagination(app)


app.include_router(accounts_router, prefix="/accounts", tags=["users"])

app.include_router(project_router, prefix="/projects", tags=["projects"])
