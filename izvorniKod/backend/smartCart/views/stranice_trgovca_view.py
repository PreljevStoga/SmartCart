from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import View

from .functions import render_form, must_be_trgovac, read_form, stay_on_page, get_artikli_from_trgovina, root_dispatch, \
    redirect_to_home_page, User, get_vlasnik_trgovine, render_template
from ..forms import DodajTrgovinu, DodajArtikl, DodajProizvodaca, DodajArtiklUTrgovinu, PromijeniRadnoVrijeme, \
    UrediArtiklUTrgovini, PromijeniLongLat, PromijeniPrioritet, UploadFileForm
from ..models import *

import datetime


@must_be_trgovac
class TrgovacView(View):
    template_name = 'smartCart/trgovac.html'

    def __init__(self):
        super(TrgovacView, self).__init__()
        self.form = {'trg_form': DodajTrgovinu(), 'art_form': DodajArtikl(), 'pro_form': DodajProizvodaca()}

    def get(self, request, *args, **kwargs):
        trgovine = list(Trgovina.objects.filter(vlasnik__id=request.user.id))
        artikli = list(Artikl.objects.all())
        return render_form(self, request, trgovine=trgovine, artikli=artikli)


@must_be_trgovac
class TrgovinaView(View):
    template_name = 'smartCart/trgovina.html'

    def __init__(self):
        super(TrgovinaView, self).__init__()
        self.form = {
            'artikl_form': DodajArtiklUTrgovinu(),
            'vrijeme_form': PromijeniRadnoVrijeme(),
            'longlat_form': PromijeniLongLat()
        }

    def dispatch(self, request, *args, **kwargs):
        t = Trgovina.objects.get(sif_trgovina=self.kwargs['sif_trgovina'])
        if request.user.id != t.vlasnik.id:
            return redirect_to_home_page(request)
        return root_dispatch(self, request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return render_form(self, request, trgovina=Trgovina.objects.get(sif_trgovina=self.kwargs['sif_trgovina']),
                           artikli=get_artikli_from_trgovina(self.kwargs['sif_trgovina']))

    def post(self, request, *args, **kwargs):
        t = Trgovina.objects.get(sif_trgovina=self.kwargs['sif_trgovina'])
        if read_form(self, request, 'artikl_form'):
            bar_k = request.POST['artikl']
            cijena = request.POST['cijena']
            akcija = True if 'akcija' in request.POST else False
            dostupan = True if 'dostupan' in request.POST else False
            a = Artikl.objects.get(barkod_artikla=bar_k)
            try:
                old_trg_art = TrgovinaArtikli.objects.get(artikl__barkod_artikla=bar_k, trgovina=t)
                old_trg_art.cijena = cijena
                old_trg_art.akcija = akcija
                old_trg_art.dostupan = dostupan
                old_trg_art.save()
            except TrgovinaArtikli.DoesNotExist:
                trg_art = TrgovinaArtikli(trgovina=t,
                                          artikl=a,
                                          cijena=cijena,
                                          akcija=akcija,
                                          dostupan=dostupan)
                trg_art.save()
        if read_form(self, request, 'vrijeme_form'):
            t.radno_vrijeme_pocetak = request.POST['radno_vrijeme_pocetak']
            t.radno_vrijeme_kraj = request.POST['radno_vrijeme_kraj']
            t.save()

        if read_form(self, request, 'longlat_form'):
            t.longitude = request.POST['longitude']
            t.latitude = request.POST['latitude']
            t.save()
        return stay_on_page(request)


@must_be_trgovac
class UrediArtiklView(View):
    template_name = 'smartCart/artikl_u_trgovini.html'

    # form_class = UrediArtiklUTrgovini

    def __init__(self):
        super(UrediArtiklView, self).__init__()
        self.form = {
            'uredi_artikl_u_trgovini_form': UrediArtiklUTrgovini(),
            'prioritet_form': PromijeniPrioritet(),
            'upload_file_form': UploadFileForm()
        }

    def dispatch(self, request, *args, **kwargs):
        self.t_id = TrgovinaArtikli.objects.get(id=self.kwargs['artikl_trgovina']).trgovina.sif_trgovina
        self.old_art = TrgovinaArtikli.objects.get(id=self.kwargs['artikl_trgovina'])
        self.form['uredi_artikl_u_trgovini_form'] = UrediArtiklUTrgovini(initial={
            'cijena': self.old_art.cijena,
            'akcija': self.old_art.akcija,
            'dostupan': self.old_art.dostupan
        })
        t = Trgovina.objects.get(sif_trgovina=self.t_id)
        if request.user.id != t.vlasnik.id:  # Stop "hacking" into trgovina website
            return redirect_to_home_page(request)
        return super(UrediArtiklView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return render_form(self, request,
                           trgovina=Trgovina.objects.get(sif_trgovina=self.t_id),
                           artikl=self.old_art.artikl.barkod_artikla,
                           opisi=self.get_opisi())

    def post(self, request, *args, **kwargs):
        if read_form(self, request, 'upload_file_form', files=True):
            # programmers be like
            # how to do x in one line
            # the line:

            try:
                file = request.FILES['file'].read().decode("utf-8").replace('\r', '').split('\n')

                attributes = file[0].split(',')
                values = file[1].split(',')

                opis = OpisArtikla(
                    autor_opisa=BaseUserModel.objects.get(email=values[0]),
                    artikl=Artikl.objects.get(barkod_artikla=values[1]),

                    vrsta=Vrsta.objects.get(sif_vrsta=values[2]),
                    zemlja_porijekla=Zemlja_porijekla.objects.get(naziv=values[3]),
                    trgovina=Trgovina.objects.get(sif_trgovina=values[4]),
                    trgovina_artikl=TrgovinaArtikli.objects.get(trgovina=values[4], artikl=values[1]),

                    naziv_artikla=values[6],
                    opis_artikla=values[7],
                    broj_glasova=values[8],
                    masa=values[9]

                )
                opis.save()

                dbfile = DBFile(
                    name=request.FILES['file'],
                    data=request.FILES['file'].read(),
                    uploaded_by=BaseUserModel.objects.get(email=values[0]),
                    date=datetime.datetime.now()
                )

                dbfile.save()
            except:
                return render_form(self, request,
                                   trgovina=Trgovina.objects.get(sif_trgovina=self.t_id),
                                   artikl=self.old_art.artikl.naziv_artikla,
                                   opisi=self.get_opisi(),
                                   file_err="Greška pri učitavanju datoteke")
            return redirect(f'/trgovina/{self.t_id}')

        elif read_form(self, request, 'uredi_artikl_u_trgovini_form'):
            old_art = TrgovinaArtikli.objects.get(id=self.kwargs['artikl_trgovina'])
            old_art.cijena = request.POST['cijena']
            old_art.akcija = True if 'akcija' in request.POST else False
            old_art.dostupan = True if 'dostupan' in request.POST else False
            old_art.save()

        elif read_form(self, request, 'prioritet_form'):
            opis_set = OpisArtikla.objects.all()
            for opis in opis_set.iterator():
                if str(opis.id) in request.POST:
                    opis.prioritiziran = True
                else:
                    opis.prioritiziran = False
                opis.save()

        return redirect(f'/trgovina/{self.t_id}')

    def get_opisi(self):
        opisi = OpisArtikla.objects.all().filter(
            trgovina_artikl=TrgovinaArtikli.objects.get(id=self.kwargs['artikl_trgovina']))
        if len(opisi) == 0:
            return ''
        else:
            opisi = sorted(opisi, key=lambda a: (a.prioritiziran, a.broj_glasova), reverse=True)
            for opis in opisi:
                opis.f = PromijeniPrioritet(initial={'prioritiziran': opis.prioritiziran})
            return opisi


@must_be_trgovac
class ObrisiArtiklView(View):
    def dispatch(self, request, *args, **kwargs):
        self.t_id = TrgovinaArtikli.objects.get(id=self.kwargs['artikl_trgovina']).trgovina.sif_trgovina
        t = Trgovina.objects.get(sif_trgovina=self.t_id)
        if request.user.id != t.vlasnik.id:  # Stop "hacking" into trgovina website
            return redirect_to_home_page(request)
        return super(ObrisiArtiklView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        old_art = TrgovinaArtikli.objects.get(id=self.kwargs['artikl_trgovina'])
        old_art.delete()
        return stay_on_page(request)

    def post(self, request, *args, **kwargs):
        return stay_on_page(request)


@must_be_trgovac
class DodajTrgovineView(View):
    form_class = DodajTrgovinu

    def __init__(self):
        super(DodajTrgovineView, self).__init__()
        self.form = DodajTrgovineView.form_class()

    def post(self, request, *args, **kwargs):
        if read_form(self, request):
            trgovina = Trgovina(naz_trgovina=request.POST['naz_trgovina'],
                                adresa_trgovina=request.POST['adresa_trgovina'],
                                vlasnik=get_object_or_404(User, pk=request.user.id),
                                radno_vrijeme_pocetak=request.POST['radno_vrijeme_pocetak'],
                                radno_vrijeme_kraj=request.POST['radno_vrijeme_kraj'],
                                latitude=request.POST['latitude'],
                                longitude=request.POST['longitude'])
            trgovina.save()
        return stay_on_page(request)

    def get(self, request, *args, **kwargs):
        return stay_on_page(request)


@must_be_trgovac
class DodajProizvodaceView(View):
    form_class = DodajProizvodaca

    def __init__(self):
        super(DodajProizvodaceView, self).__init__()
        self.form = DodajProizvodaceView.form_class()

    def post(self, request, *args, **kwargs):
        if read_form(self, request):
            proizvodac_za_dodati = Proizvodac(naziv=request.POST['naziv'])
            proizvodac_za_dodati.save()
        return stay_on_page(request)

    def get(self, request, *args, **kwargs):
        return stay_on_page(request)


@must_be_trgovac
class DodajArtikleView(View):
    form_class = DodajArtikl

    def __init__(self):
        super(DodajArtikleView, self).__init__()
        self.form = DodajArtikleView.form_class()

    def post(self, request, *args, **kwargs):
        if read_form(self, request):
            artikl_za_dodati = Artikl(
                barkod_artikla=request.POST['barkod_artikla'],
            )
            artikl_za_dodati.save()
        return stay_on_page(request)

    def get(self, request, *args, **kwargs):
        return stay_on_page(request)


@must_be_trgovac
class DeleteTrgovinaView(View):
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated and request.user != get_vlasnik_trgovine(self.kwargs['sif_trgovina']):
            return redirect('trgovac')
        Trgovina.objects.filter(sif_trgovina=self.kwargs['sif_trgovina']).delete()
        return redirect('trgovac')


@must_be_trgovac
class ArtiklView(View):
    template_name = 'smartCart/artikl.html'

    def get(self, request, *args, **kwargs):
        opis = OpisArtikla.objects.filter(
            artikl=Artikl.objects.get(barkod_artikla=self.kwargs["barkod_artikla"])).order_by("prioritiziran",
                                                                                              "broj_glasova").last()

        if(opis is None):
            artikl = {"barkod_artikla": self.kwargs["barkod_artikla"]}
        else:
            artikl = {
                "barkod_artikla": self.kwargs["barkod_artikla"],
                "naziv_artikla": opis.naziv_artikla,
                "opis_artikla": opis.opis_artikla,
                "autor_opisa": opis.autor_opisa,
                "broj_glasova": opis.broj_glasova,
                "masa": opis.masa,
                "vrsta": opis.vrsta,
                "zemlja_porijekla": opis.zemlja_porijekla
            }
        form = UploadFileForm
        return render_template(self, request, artikl=artikl, form=form)

    def post(self, request, *args, **kwargs):
        print(request.POST)
        barkod = request.POST['title']
        image_file = request.FILES['file'].read()
        tmp = ArtiklImage(artikl=Artikl.objects.get(barkod_artikla=barkod), image=image_file)
        tmp.save()
        return stay_on_page(request)

from .functions import create_json_response
from django.core import serializers
import json
from django.http import HttpResponse

class ArtiklImageView(View):

    def post(self, request, *args, **kwargs):
        barkod = json.loads(request.body)['barkod']
        print(barkod)
        image_file = ArtiklImage.objects.filter(artikl=Artikl.objects.get(barkod_artikla=barkod))
        if (len(image_file) > 0):
            return create_json_response(200, data=serializers.serialize('json', image_file))
        else:
            res = HttpResponse()
            res.status_code = 404
            return res
    

    """
    def post(self, request, *args, **kwargs):
        image_file = request.FILES['file'].read()
        print(image_file)
        ArtiklImage.objects.create(image=image_file)
        return stay_on_page(request)
    """