from django.urls import path
from django.urls.conf import include

from users.views import (
    Login,
    Registration,
    UpdateProfile,
    UpdatePassword,
    Logout,
    Profile,
)

urlpatterns = [
    path('', Profile.as_view(), name='profile'),
    path('login/', Login.as_view(), name="login"),
    path('logout/', Logout.as_view(), name='logout'),
    path('registration/', Registration.as_view(), name='registration'),
    path('update/', UpdateProfile.as_view(), name="update-profile"),
    path('password/', UpdatePassword.as_view(), name='update-password'),
]
