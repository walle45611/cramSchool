from django.urls import path
from . import views

app_name = 'cramschool_management'

urlpatterns = [
    path('', views.cramschool_list, name='cramschool_list'),
    # path('update/<int:school_id>/', views.update_address, name='update_address'),
]
