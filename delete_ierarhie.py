# delete_ierarhie.py

from myapp.models import Ierarhie

def run():
    Ierarhie.objects.all().delete()
    print("Toată ierarhia a fost ștearsă.")
