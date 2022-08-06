from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from .models import Customer, Passport
from .serializers import (
    CustomerPassportSerializer,
    CustomerSerializer,
    CustomerDetailSerializer,
    PassportSerializer
)
from rest_framework.permissions import IsAuthenticated
from stories import State
from .stories import CustomerStory as CS, CheckPassportIdStory as PSI, PassportStory as PS
from rest_framework.status import (
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_204_NO_CONTENT,
    HTTP_200_OK,
)
import os
import json
from django.core.serializers import serialize
from django.http.response import JsonResponse



# ::::::::::::::::::::::::::::::::: CUSTOMER VIEWS :::::::::::::::::::::::::::::::::::::::

class CustomerOrPassportCreateAPIView(APIView):
    def post(self, request):
        serializer = CustomerPassportSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class CustomerUpdateDeleteAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        """ we check if customer is exists or not via using below story """
        customer_story = CS()
        state = State(pk=pk)
        customer_story(state)
        return Customer.objects.get(pk=pk)

    def put(self, request, pk):
        customer = self.get_object(pk=pk)
        serializer = CustomerSerializer(customer, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        customer = self.get_object(pk)
        customer.delete()
        return Response(status=HTTP_204_NO_CONTENT)


class CustomerDetailAPIView(APIView):
    def get_object(self, pk):
        customer_story = CS()
        state = State(pk=pk)
        customer_story(state)
        return Customer.objects.get(pk=pk)

    def get(self, request, pk):
        print("token >>> ", os.getenv('MRZ_URL'))
        customer = self.get_object(pk=pk)
        serializer = CustomerDetailSerializer(customer)
        return Response(serializer.data, status=HTTP_200_OK)


class CustomerListAPIView(ListAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


##############################################################################
create_customer_passport = CustomerOrPassportCreateAPIView.as_view()
read_all_customer_data = CustomerListAPIView.as_view()
update_or_delete_customer = CustomerUpdateDeleteAPIView.as_view()
detail_customer_info = CustomerDetailAPIView.as_view()



# :::::::::::::::::::::::::::::::::: PASSPORT VIEWS :::::::::::::::::::::::::::::::::::::::

class PassportListAPIView(ListAPIView):
    queryset = Passport.objects.all()
    serializer_class = PassportSerializer


class PassportReadUpdateDeleteAPIView(APIView):
    
    def get_object(self ,pk):
        """ we check if customer is exists or not via using below story """
        passport_story = PSI()
        passport_state = State(pk=pk)
        passport_story(passport_state)
        return Passport.objects.get(pk=pk)

    
    def json_serialize_passport(self, pk):
        """ we are serializing Passport model in this function. Because if we don't
            use this method we cannot return updated data in the 'PUT' method.
            Otherwise we return previous data.
        """
        passport_queryset = Passport.objects.filter(pk=pk)
        return json.loads(serialize('json', passport_queryset))

    def get(self, request, pk):
        passport = self.get_object(pk=pk)
        serializer = PassportSerializer(passport)
        return Response(serializer.data, status=HTTP_200_OK)

    def put(self, request, pk):
        passport = self.get_object(pk=pk)
        serializer = PassportSerializer(passport, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        """ We use this story for load passport data from scan_file """
        if serializer.validated_data.get('scan_file'):
            story = PS()
            state = State(
                passport_id=pk,
                scan_file=passport.scan_file.path,
                token=os.getenv('TOKEN'),
                mrz_url=os.getenv('MRZ_URL'),
                task_status_url=os.getenv('TASK_STATUS_URL'),
            )

            story(state)
        return JsonResponse(self.json_serialize_passport(pk), safe=False)


    def delete(self, request, pk):
        passport = self.get_object(pk=pk)
        passport.delete()
        return Response(status=HTTP_204_NO_CONTENT)

#########################################################################
get_all_passports = PassportListAPIView.as_view()
passport_read_update_delete = PassportReadUpdateDeleteAPIView.as_view()

