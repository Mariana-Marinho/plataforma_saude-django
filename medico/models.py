from django.db import models
from django.contrib.auth.models import User


def is_medico(user):
    return DadosMedico.objects.filter(user=user).exists()

class Especialidades(models.Model):
    especialidade = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.especialidade
    
class DadosMedico(models.Model):
    crm = models.CharField(max_length=15)
    nome = models.CharField(max_length=100)
    cep = models.CharField(max_length=15)
    rua = models.CharField(max_length=100)
    bairro = models.CharField(max_length=100)
    numero = models.IntegerField()
    rg = models.ImageField(upload_to="rg")
    cedula_identidade_medica = models.ImageField(upload_to='cim')
    foto = models.ImageField(upload_to="foto_perfil")
    descricao = models.TextField(null=True, blank=True)
    valor_consulta = models.FloatField(default=100)
    especialidade = models.ForeignKey(Especialidades, on_delete=models.DO_NOTHING, null=True, blank=True)

    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.user.username 
