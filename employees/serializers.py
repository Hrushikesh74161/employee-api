from rest_framework import serializers
from django.contrib.auth.models import User
from employees.models import Employee
from django.contrib.auth.password_validation import get_default_password_validators
from rest_framework.exceptions import APIException
from django.contrib.auth.password_validation import (
    UserAttributeSimilarityValidator,
    MinimumLengthValidator,
    CommonPasswordValidator,
    NumericPasswordValidator,
)


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = "__all__"

    def validate_age(self, age):
        if age > 60:
            raise APIException("Age should be less than or equal to 60.")
        return age


class UserSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("email", "username", "password")

    def validate_password(self, password):
        password_validators = get_default_password_validators()

        for validator in password_validators:
            try:
                validator.validate(password)
            except:
                if isinstance(validator, UserAttributeSimilarityValidator):
                    raise APIException("Password similar to username.")
                if isinstance(validator, MinimumLengthValidator):
                    raise APIException(
                        "Password is short. Should be atleast 8 characters."
                    )
                if isinstance(validator, CommonPasswordValidator):
                    raise APIException("Password is too common.")
                if isinstance(validator, NumericPasswordValidator):
                    raise APIException("Password is all numeric.")

        return password
