from tortoise import fields
from fastapi_admin.models import AbstractAdmin


class AdminUser(AbstractAdmin):
    id = fields.IntField(pk=True)
    is_superuser = fields.BooleanField(default=True)