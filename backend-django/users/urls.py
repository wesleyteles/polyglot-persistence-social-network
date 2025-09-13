from django.urls import path
from .views import CriarUsuarioView, ListarUsuariosView,  UsuarioAtualView

urlpatterns = [
    path('register/', CriarUsuarioView.as_view(), name='register'),
    path('me/', UsuarioAtualView.as_view(), name='current-user'),
    path('', ListarUsuariosView.as_view(), name='list-users'),
]