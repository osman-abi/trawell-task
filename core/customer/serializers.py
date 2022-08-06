from rest_framework import serializers
from .models import Customer, Passport
from stories import State
from .stories import CustomerStory as CS, PassportStory as PS
from django.core.serializers import serialize
import json
import os


class CustomerPassportSerializer(serializers.Serializer):
    """This class is used for creating 'Customer' or 'Passport' models"""

    key = serializers.CharField(required=False)
    # customer fields
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(required=False)
    surname = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)
    phone = serializers.CharField(required=False)
    # passport fields
    customer_id = serializers.IntegerField(required=False)
    scan_file = serializers.ImageField(required=False)

    def create(self, validated_data):
        """In this function we're checking 'key'. If 'key' is 'customer' then
        'Customer' model will be created, but if 'ket' is 'passport' then
        'Passport' model will be created.
        """
        key = validated_data.get("key")
        if key == "customer":
            return Customer.objects.create(
                name=validated_data.get("name"),
                surname=validated_data.get("surname"),
                email=validated_data.get("email"),
                phone=validated_data.get("phone"),
            )
        elif key == "passport":
            """At this point we instanciate Customer Story to check if 'customer'
            is exists or not via given 'id'
            """
            customer_story = CS()
            state_customer = State(pk=validated_data.get("customer_id"))
            # check if customer is exists
            customer_story(state_customer)

            passport = Passport.objects.create(
                customer_id=validated_data.get("customer_id"),
                scan_file=validated_data.get("scan_file"),
            )

            # extract passport
            """ At this point we instaciate Passport Story to extract datas from
                passport file and handle errors
            """

            passport_story = PS()
            state_passport = State(
                passport_id=passport.id,
                scan_file=passport.scan_file.path,
                token=os.getenv('TOKEN'),
                mrz_url=os.getenv('MRZ_URL'),
                task_status_url=os.getenv('TASK_STATUS_URL'),
            )

            passport_story(state_passport)

            return passport


class CustomerSerializer(serializers.ModelSerializer):
    """This class is used for update, delete, read 'Customer' model"""

    class Meta:
        model = Customer
        fields = "__all__"


class CustomerDetailSerializer(serializers.ModelSerializer):
    """This class is used for read 'Customer' detail info"""

    passports = serializers.SerializerMethodField()

    class Meta:
        model = Customer
        fields = ["id", "name", "surname", "phone", "passports"]

    def get_passports(self, obj):
        data = json.loads(serialize("json", obj.passport_set.all()))
        return data


class PassportSerializer(serializers.ModelSerializer):
    """ This class is used for Read, Update, Delete 'Passport' model """

    class Meta:
        model = Passport
        fields = '__all__'