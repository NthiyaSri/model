from marshmallow import Schema, fields, validate


class RegisterSchema(Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True, validate=validate.Length(min=6))
    name = fields.String(required=False, allow_none=True)


class LoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True)


class ProductCreateSchema(Schema):
    title = fields.String(required=True)
    short_desc = fields.String(required=False, allow_none=True)
    description = fields.String(required=False, allow_none=True)
    price = fields.Float(required=True)
    category_id = fields.Integer(required=False, allow_none=True)
    image_url = fields.String(required=False, allow_none=True)


class CartAddSchema(Schema):
    product_id = fields.Integer(required=True)
    quantity = fields.Integer(required=True, validate=validate.Range(min=1))


class CheckoutSchema(Schema):
    shipping_address = fields.String(required=True)
    payment_token = fields.String(required=False)


class AIDescriptionSchema(Schema):
    title = fields.String(required=True)
    features = fields.List(fields.String(), required=False)
    short_desc = fields.String(required=False, allow_none=True)
