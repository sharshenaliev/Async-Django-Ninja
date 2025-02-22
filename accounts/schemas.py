from ninja import ModelSchema, Schema
from pydantic import EmailStr
from django.contrib.auth import get_user_model


class UserRegister(Schema):
    email: EmailStr
    password: str


class UserSchema(ModelSchema):
    class Meta:
        model = get_user_model()
        fields = ('id', 'email', 'date_joined', 'username')


class UserUpdateSchema(ModelSchema):
    class Meta:
        model = get_user_model()
        fields = ('email', )
