from django.urls import path
from .views import *

urlpatterns = [
	path("login/", LoginUser.as_view(), name="login"),
	path("home/", Home.as_view(), name="home_page"),
	path("logout/", logout_func, name="logout"),
	path("edit_<str:user_id>/", EditUser.as_view(), name="edit_page"),
	path("delete_obj_<str:user_id>/", delete_user, name="delete_page"),
	path("create_account/", CreateAccount.as_view(), name="create_account"),
	path("profile_your/", ProfilePage.as_view(), name="profile_page"),
	path("password/", ChangePassword.as_view(), name="change_password")
]