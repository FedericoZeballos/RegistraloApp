# app/admin.py
from fastapi_admin.app import FastAPIAdmin
from fastapi_admin.providers.login import UsernamePasswordProvider
from aioredis import from_url as redis_from_url
import os
from app.models.admin_user import AdminUser
from fastapi_admin.resources import Model as AdminModel
from app.models.compra_tortoise import compras
from starlette.responses import RedirectResponse
from starlette.requests import Request

# Crear admin_app y incluir router de recursos
admin_app = FastAPIAdmin()

# Incluir router de recursos manualmente
from fastapi_admin.routes import router as admin_router
admin_app.include_router(admin_router)


async def init_admin(app):
    # proveedor de login
    provider = UsernamePasswordProvider(
        admin_model=AdminUser,
        login_logo_url="https://fastapi-admin.github.io/img/logo.png",
        login_title="Panel de administración de RegistraloApp",
    )

    # Redis
    redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    redis = redis_from_url(redis_url, decode_responses=True)
    await admin_app.configure(
        redis=redis,
        providers=[provider],
        template_folders=None,
    )

    # Recurso Compra
    class CompraResource(AdminModel):
        label = "Compras"
        model = compras
        page_title = "Gestión de Compras"
        page_pre_title = "Compras"
        fields = [
            "nombre",
            "descripcion",
            "categoria",
            "monto",
            "fecha",
        ]

    admin_app.register_resources(CompraResource)
    
    # Force manual registration in model_resources
    admin_app.model_resources[compras] = CompraResource
    
    # Debug: print what we have
    print(f"Admin setup - Resources: {len(admin_app.resources)}")
    print(f"Model resources: {admin_app.model_resources}")
    from tortoise import Tortoise
    print(f"Tortoise apps: {list(Tortoise.apps.keys())}")
    for app_name, models in Tortoise.apps.items():
        print(f"  {app_name}: {list(models.keys())}")

    # Ruta raíz
    @admin_app.get("", include_in_schema=False)
    @admin_app.get("/", include_in_schema=False)
    async def admin_root(request: Request):
        if getattr(request.state, "admin", None):
            first = next((r for r in admin_app.resources if hasattr(r, "model")), None)
            if first:
                slug = first.model.__name__.lower()  # compras
                return RedirectResponse(
                    url=f"{admin_app.admin_path}/{slug}/list", status_code=303
                )
        return RedirectResponse(url=f"{admin_app.admin_path}/login", status_code=303)
