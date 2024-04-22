from django.shortcuts import render, redirect
from medico.models import DadosMedico, Especialidades, DatasAbertas, is_medico
from datetime import datetime
from django.contrib import messages
from django.contrib.messages import constants
from .models import Consulta
from django.db import transaction


# Create your views here.
def home(request):
    if request.method == "GET":
        medicos = DadosMedico.objects.all()
        especialidades = Especialidades.objects.all()

        medico_filtrar = request.GET.get('medico')
        especialidades_filtrar = request.GET.getlist('especialidades')

        if medico_filtrar:
            medicos = medicos.filter(nome__icontains = medico_filtrar)

        if especialidades_filtrar:
            medicos = medicos.filter(especialidade_id__in=especialidades_filtrar)
        
        minhas_consultas = Consulta.objects.filter(paciente=request.user).filter(data_aberta__data__gte=datetime.now())
        
        for consulta in minhas_consultas:
            diferenca_dias = (consulta.data_aberta.data.date() - datetime.now().date()).days
            consulta.contagem_regressiva = diferenca_dias
    
        return render(request, 'home.html', {'medicos': medicos, 'especialidades': especialidades, 'minhas_consultas': minhas_consultas, 'is_medico': is_medico(request.user)})

def escolher_horario(request, id_dados_medicos):
    if request.method == "GET":
        medico = DadosMedico.objects.get(id=id_dados_medicos)
        datas_abertas = DatasAbertas.objects.filter(user=medico.user).filter(data__gte=datetime.now()).filter(agendado=False)
        
        return render(request, 'escolher_horario.html', {'medico': medico, 'datas_abertas': datas_abertas, 'is_medico': is_medico(request.user)})

@transaction.atomic
def agendar_horario(request, id_data_aberta):
    if request.method == "GET":
        data_aberta = DatasAbertas.objects.get(id=id_data_aberta)

        horario_agendado = Consulta(
            paciente=request.user,
            data_aberta=data_aberta
        )

        horario_agendado.save()

        # TODO: Sugestão Tornar atomico

        data_aberta.agendado = True
        data_aberta.save()

        messages.add_message(request, constants.SUCCESS, 'Horário agendado com sucesso.')

        return redirect('/pacientes/minhas_consultas/')

def minhas_consultas(request):
    if request.method == "GET":
        minhas_consultas = Consulta.objects.filter(paciente=request.user).filter(data_aberta__data__gte=datetime.now())
        
        #  DatasAbertas.objects.filter(user=medico.user).filter(data__gte=datetime.now()).filter(agendado=False)

        return render(request, 'minhas_consultas.html', {'minhas_consultas': minhas_consultas, 'is_medico': is_medico(request.user)})

def consulta(request, id_consulta):
    if request.method == 'GET':
        consulta = Consulta.objects.get(id=id_consulta)
        dado_medico = DadosMedico.objects.get(user=consulta.data_aberta.user)
        
        return render(request, 'consulta.html', {'consulta': consulta, 'dado_medico': dado_medico, 'is_medico': is_medico(request.user)})

def consulta_area_medico(request, id_consulta):
    if not is_medico(request.user):
        messages.add_message(request, constants.WARNING, 'Somente médicos podem acessar essa página.')
        return redirect('/usuarios/sair')
    

    if request.method == "GET":
        consulta = Consulta.objects.get(id=id_consulta)
        return render(request, 'consulta_area_medico.html', {'consulta': consulta,'is_medico': is_medico(request.user)})
