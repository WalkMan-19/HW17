from marshmallow import Schema, fields


class MovieSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str()
    trailer = fields.Str()
    year = fields.Str()
    rating = fields.Int()
    genre = fields.Str()
    director = fields.Str()
    description = fields.Str()


class GenreSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()


class DirectorSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()
