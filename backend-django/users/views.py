from rest_framework import generics, permissions
from .models import Usuario
from .serializers import UsuarioSerializer
from rest_framework.views import APIView
from rest_framework.response import Response

class CriarUsuarioView(generics.CreateAPIView):
    """
    View para criar (registrar) um novo usuário.
    """
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    # Permite que qualquer usuário (mesmo não autenticado) acesse esta view.
    permission_classes = [permissions.AllowAny]

class ListarUsuariosView(generics.ListAPIView):
    """ View para listar todos os usuários, exceto o próprio usuário logado. """
    serializer_class = UsuarioSerializer
    permission_classes = [permissions.IsAuthenticated] # Só usuários logados podem ver a lista

    def get_queryset(self):
        # Retorna todos os usuários, excluindo o que fez a requisição
        return Usuario.objects.exclude(id=self.request.user.id)

class UsuarioAtualView(APIView):
    """ View para obter os dados do usuário atualmente autenticado. """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = UsuarioSerializer(request.user)
        return Response(serializer.data)        