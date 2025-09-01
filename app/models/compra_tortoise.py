from tortoise import fields
from tortoise.models import Model


class compras(Model):  # Nombre que coincide con fastapi-admin URL
    class Meta:
        table = "compras"

    id = fields.IntField(pk=True)
    nombre = fields.CharField(max_length=255, index=True, null=True)
    descripcion = fields.TextField(null=False)
    categoria = fields.CharField(max_length=100, index=True, null=True)
    monto = fields.FloatField(null=False)
    fecha = fields.DatetimeField(auto_now_add=True)


