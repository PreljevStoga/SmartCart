import json

from django.contrib.auth import authenticate, logout
from django.contrib.sessions.models import Session
from django.core import serializers
from django.views.generic.base import View

from .functions import create_json_response, get_authorization_level, android_login_function, get_user_from_session, \
    User
from ..models import Artikl, SecretCode, Trgovina


class AndroidArtikliView(View):
    def post(self, request, *args, **kwargs):
        try:
            naziv_artikla = json.loads(request.body)['naziv_artikla']
        except KeyError:
            naziv_artikla = ''
        artikli = Artikl.objects.filter(naziv_artikla__contains='%s' % naziv_artikla)
        return create_json_response(200, data=serializers.serialize('json', artikli), safe=False)


class AndroidPopisView(View):
    def post(self, request, *args, **kwargs):
        barkodovi = json.loads(request.body)['barkod']
        artikli = []
        for barkod in barkodovi:
            artikli += Artikl.objects.filter(barkod_artikla=barkod)
        return create_json_response(200, data=serializers.serialize('json', artikli), safe=False)


class AndroidLogInView(View):
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        email = data['email']
        password = data['password']
        if email == "" or password == "":
            return create_json_response(401, err='Fill out all fields')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            android_login_function(request, user)
            return create_json_response(200, session_id=request.session.session_key,
                                        authorisation_level=get_authorization_level(get_user_from_session(request.session.session_key)))
        else:
            return create_json_response(401, err='Wrong email or password')


class AndroidLogoutView(View):
    def post(self, request, *args, **kwargs):
        user = get_user_from_session(json.loads(request.body)['sessionId'])
        Session.objects.filter(usersession__user=user).delete()
        logout(request=request)
        return create_json_response(200, success='done')


class AndroidSignUpView(View):
    def post(self, request, *args, **kwargs):
        email = json.loads(request.body)['email']
        password = json.loads(request.body)['password']
        secret_code = json.loads(request.body)['secret_code']

        if secret_code:
            authorisation_level = 'trgovac'
        else:
            authorisation_level = 'kupac'

        if email == "" or password == "":
            return create_json_response(401, err='Fill out all fields')

        if User.objects.filter(email=email).exists():
            return create_json_response(401, err='User already exists')

        if authorisation_level == 'kupac':
            User.objects.create_user(email, password, is_kupac=True)
            return create_json_response(200, success='done')

        if authorisation_level == 'trgovac':
            secret_code = SecretCode.objects.filter(value=secret_code)
            if not secret_code.exists():
                return create_json_response(401, err='Wrong secret code')
            secret_code.delete()
            User.objects.create_user(email, password, is_trgovac=True)
            return create_json_response(200, success='done')
        return create_json_response(401, err='Weird error :(')


class AndroidTrgovineView(View):
    def post(self, request, *args, **kwargs):
        try:
            naz_trgovina = json.loads(request.body)['naz_trgovina']
        except KeyError:
            naz_trgovina = ''
        try:
            sif_trgovina = json.loads(request.body)['sif_trgovina']
        except KeyError:
            sif_trgovina = None
        trgovine = Trgovina.objects.filter(naz_trgovina__contains=f'{naz_trgovina}')
        if sif_trgovina is not None:
            trgovine = trgovine.filter(sif_trgovina=sif_trgovina)
        return create_json_response(200, data=serializers.serialize('json', trgovine), safe=False)