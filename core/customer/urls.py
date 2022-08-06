from django.urls import path
from .views import (
    create_customer_passport,
    update_or_delete_customer,
    read_all_customer_data,
    detail_customer_info,
    get_all_passports,
    passport_read_update_delete
)

urlpatterns = [
    path("create/", create_customer_passport),
    # customer urls
    path("customer/<int:pk>/", update_or_delete_customer),
    path("customer-detail/<int:pk>/", detail_customer_info),
    path("customers/", read_all_customer_data),
    # passport urls
    path('passports/', get_all_passports),
    path('passport/<int:pk>/', passport_read_update_delete)
]
