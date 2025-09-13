from rest_framework import serializers
from .models import Usuario

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        # Campos que serão usados no processo de serialização
        fields = ['id', 'username', 'email', 'password', 'data_nascimento', 'biografia']
        # Configurações extras para campos específicos
        extra_kwargs = {
            'password': {'write_only': True} # A senha só pode ser escrita, nunca lida
        }

    def create(self, validated_data):
        """
        Sobrescreve o método create para hashear a senha antes de salvar.
        """
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            # O método set_password cuida do hashing
            instance.set_password(password)
        instance.save()
        return instance