from django.urls import path
from .views import RegisterView, LoginView, DogBreedPredictView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("predict/", DogBreedPredictView.as_view(), name="predict"),
]