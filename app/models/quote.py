from tortoise import fields, models


class Quote(models.Model):
    id = fields.IntField(pk=True)
    title = fields.CharField(max_length=500)
    content = fields.TextField()
    author = fields.CharField(max_length=255, null=True)
    category = fields.CharField(max_length=255, null=True)
    source_url = fields.CharField(max_length=500, null=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "quotes"
