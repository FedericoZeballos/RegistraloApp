from fastapi import FastAPI
from app.routers import compra
from app.admin import init_admin, admin_app
from tortoise import Tortoise
from app.core.database import DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME

app = FastAPI(title="RegistraloApp")

# Registrar rutas de negocio
app.include_router(compra.router)

@app.on_event("startup")
async def on_startup():
    # Inicializar Tortoise PRIMERO
    db_url = f"postgres://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    await Tortoise.init(
        db_url=db_url,
        modules={"models": ["app.models.admin_user", "app.models.compra_tortoise"]},
    )
    await Tortoise.generate_schemas()
    
    # Luego inicializar admin (cuando Tortoise ya está listo)
    await init_admin(app)

@app.on_event("shutdown")
async def on_shutdown():
    await Tortoise.close_connections()

# Montar admin en /admin
app.mount("/admin", admin_app)

# Debug endpoint
@app.get("/debug/admin-routes")
async def debug_admin_routes():
    routes = []
    for route in admin_app.routes:
        routes.append({
            "path": getattr(route, 'path', 'unknown'),
            "name": getattr(route, 'name', 'unknown'),
            "methods": getattr(route, 'methods', [])  
        })
    return {
        "admin_app_routes": len(admin_app.routes),
        "routes": routes,
        "admin_resources": len(admin_app.resources)
    }

@app.get("/")
def root():
    return {"mensaje": "Bienvenido a RegistraloApp 🚀"}
