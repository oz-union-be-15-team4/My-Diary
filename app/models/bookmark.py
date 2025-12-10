from tortoise import fields, models
from app.models.user import User
from app.models.quote import Quote

class Bookmark(models.Model):
    id = fields.IntField(pk=True)

    # FK: Bookmark → User
    user: fields.ForeignKeyRelation[User] = fields.ForeignKeyField(
        "models.User",
        related_name="bookmarks",
        on_delete=fields.CASCADE,
    )

    # FK: Bookmark → Quote
    quote: fields.ForeignKeyRelation[Quote] = fields.ForeignKeyField(
        "models.Quote",
        related_name="bookmarks",
        on_delete=fields.CASCADE,
    )

    class Meta:
        table = "bookmarks"