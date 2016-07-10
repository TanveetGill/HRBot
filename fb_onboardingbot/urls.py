from django.conf.urls import include, url
from .views import OnBoardingBotView

urlpatterns = [
                  url(r'^664033d8cd82824fcacf49b0179ae621e39deee761963a5031/?$', OnBoardingBotView.as_view()) 
               ]