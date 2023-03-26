from marshmallow import Schema, fields


class PlainItemSchema(Schema):
    # only for output
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)
    price = fields.Float(required=True)


class PlainStoreschema(Schema):
    # only for output
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)


class ItemUpdateSchema(Schema):
    name = fields.Str()
    price = fields.Float()

class ItemSchema(PlainItemSchema):
    # only for output
    store_id = fields.Str(required=True, load_only=True)
    store = fields.Nested(PlainStoreschema(), dump_only=True)


class Storeschema(PlainStoreschema):
    # only for output
    items = fields.List(fields.Nested(PlainItemSchema(), dump_only=True))


