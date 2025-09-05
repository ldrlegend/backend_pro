from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.api.v1 import user, product, vendor, operator, country, attribute, attribute_option
from app.db.init_db import init_db
from fastapi.middleware.cors import CORSMiddleware

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    init_db()
    yield
    # Shutdown cleanup (if needed)

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user.router, prefix="/users", tags=["users"])
app.include_router(product.router, prefix="/products", tags=["products"])
app.include_router(vendor.router, prefix="/vendors", tags=["vendors"])
app.include_router(operator.router, prefix="/operators", tags=["operators"])
app.include_router(country.router, prefix="/countries", tags=["countries"])
app.include_router(attribute.router, prefix="/attributes", tags=["attributes"])
app.include_router(attribute_option.router, prefix="/attribute_options", tags=["attribute_options"])