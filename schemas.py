from marshmallow import Schema, fields


class PlainItemSchema(Schema):
    # only for output
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    price = fields.Float(required=True)


class PlainStoreSchema(Schema):
    # only for output
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)

class PlainTagSchema(Schema):
    # only for output
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)


class ItemUpdateSchema(Schema):
    name = fields.Str()
    price = fields.Float()

class ItemSchema(PlainItemSchema):
    # only for output
    store_id = fields.Str(required=True, load_only=True)
    store = fields.Nested(PlainStoreSchema(), dump_only=True)
    tags = fields.Nested(PlainTagSchema(), dump_only=True)


class Storeschema(PlainStoreSchema):
    # only for output
    items = fields.List(fields.Nested(PlainItemSchema(), dump_only=True))
    tags = fields.List(fields.Nested(PlainTagSchema(), dump_only=True))


class TagSchema(PlainTagSchema):
    # only for output
    store_id = fields.Str(required=False, load_only=True)
    store = fields.Nested(PlainStoreSchema(), dump_only=True)
    items = fields.List(fields.Nested(PlainItemSchema(), dump_only=True))


class TagAndItemSchema(Schema):
    message = fields.Str()
    item = fields.Nested(ItemSchema)
    tag = fields.Nested(TagSchema)
