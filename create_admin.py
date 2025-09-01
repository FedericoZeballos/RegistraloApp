import sys
import os
import asyncio
from tortoise import Tortoise
from app.core.database import DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME
from app.models.admin_user import AdminUser
import fastapi_admin.utils as fa_utils


async def init_orm():
    db_url = os.getenv(
        "TORTOISE_DB_URL",
        f"postgres://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}",
    )
    await Tortoise.init(
        db_url=db_url,
        modules={"models": ["app.models.admin_user"]},
    )
    await Tortoise.generate_schemas()


async def create_admin():
    await init_orm()

    password = os.getenv("ADMIN_PASSWORD", "admin")
    # Usar el hash por defecto de fastapi-admin (bcrypt)
    hashed_password = fa_utils.hash_password(password)

    existing = await AdminUser.get_or_none(username="admin")
    if existing:
        # Actualizar contraseña al formato bcrypt por si fue creada con otro algoritmo
        existing.password = hashed_password
        await existing.save()
        print("Contraseña del usuario admin actualizada.")
    else:
        await AdminUser.create(username="admin", password=hashed_password, is_superuser=True)
        print("Usuario admin creado: admin")

    await Tortoise.close_connections()


if __name__ == "__main__":
    if sys.platform.startswith("win"):
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(create_admin())
