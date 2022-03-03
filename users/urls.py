from django.urls import path
from django.urls.conf import include

from users.views import (
    Login,
    PasswordReset,
    PasswordResetConfirm,
    PasswordResetDone,
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
    path('password/reset/', PasswordReset.as_view(), name="password-reset"),
    path('password/reset/done', PasswordResetDone.as_view(), name="password-reset-done"),
    path('password/reset/<uidb64>/<token>', PasswordResetConfirm.as_view(),
         name="password-reset-confirm")
]
