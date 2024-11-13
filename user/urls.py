from django.urls import path
from .views import Registration,Login,VerifyOTP,ResetPasswordEmail,ResetPassword



urlpatterns = [
    path('register/',Registration.as_view(),name='register' ),
    path('login/',Login.as_view(),name='login'),
    path('verifyotp/',VerifyOTP.as_view(),name='verifyotp'),
    path('resetpasswordemail/',ResetPasswordEmail.as_view(),name='reset-password-email'),
    path('resetpassword/<uid>/<token>/',ResetPassword.as_view(),name='reset-password')
]