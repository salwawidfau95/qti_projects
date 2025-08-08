from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from app.routers import auth, users, content

app = FastAPI()

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(content.router)

@app.get("/")
def root():
    return {"message": "Backend QTI API Running!"}

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title="Project QTI API",
        version="1.0.0",
        description="API for QTI Backend",
        routes=app.routes,
    )
    
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }

    # Hanya terapkan BearerAuth ke path yang bukan /auth/*
    for path, methods in openapi_schema["paths"].items():
        if not path.startswith("/auth"):
            for method in methods.values():
                method.setdefault("security", [{"BearerAuth": []}])

    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi
