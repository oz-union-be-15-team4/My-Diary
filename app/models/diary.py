from tortoise import fields, models
from app.models.user import User


class Diary(models.Model):
    id = fields.IntField(pk=True)
    title = fields.CharField(max_length=255)
    content = fields.TextField()
    created_at = fields.DatetimeField(auto_now_add=True)

    # FK: Diary → User
    user: fields.ForeignKeyRelation[User] = fields.ForeignKeyField(
        "models.User",
        related_name="diaries",
        on_delete=fields.CASCADE,
    )

    class Meta:
        table = "diaries"