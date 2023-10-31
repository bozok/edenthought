from django.urls import path

from . import views

from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login, name="login"),
    path("logout", views.logout, name="logout"),
    path("register", views.register, name="register"),
    path("dashboard", views.dashboard, name="dashboard"),
    path("new-thought", views.new_thought, name="new-thought"),
    path("my-thoughts", views.my_thoughts, name="my-thoughts"),
    path("update-thought/<str:pk>", views.update_thought, name="update-thought"),
    path("delete-thought/<str:pk>", views.delete_thought, name="delete-thought"), 
    path("profile-management", views.profile_management, name="profile-management"),
    path("delete-account", views.delete_account, name="delete-account"),
    
    # Password management
    
    # 1 - Allow us to enter our email to receive a password reset link
    path("reset_password", auth_views.PasswordResetView.as_view(template_name="journal/password-reset.html"), name="reset_password"),
    # 2 - Show a success message stating that an email was sent to reset our password
    path("reset_password_sent", auth_views.PasswordResetDoneView.as_view(template_name="journal/password-reset-send.html"), name="password_reset_done"),
    # 3 - Send a link to our email so that we can reset our password
    path("reset/<uidb64>/<token>", auth_views.PasswordResetConfirmView.as_view(template_name="journal/password-reset-form.html"), name="password_reset_confirm"),
    # 4 - Show a success message that our password was changed
    path("password_reset_complete", auth_views.PasswordResetCompleteView.as_view(template_name="journal/password-reset-complete.html"), name="password_reset_complete"),
]