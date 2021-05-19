

from django.urls import path, re_path
from app import views

urlpatterns = [

    # The home page
    path('mainadmin', views.index, name='home'),
    path('', views.webindex, name='webindex'),
    path('patient-registration', views.patientreg, name='patientreg'),
    path('predictions-report', views.predictions, name='predictions'),
    path('pneumonia-reporting', views.pneumonia_reporting,name='pneumonia_reporting'),
    path('covid-reporting', views.covid_reporting, name='covid_reporting'),
    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),

]
