from django import forms
from .models import Lectie

class FlashcardUploadForm(forms.Form):
    lectie = forms.ModelChoiceField(queryset=Lectie.objects.all())
    continut_csv = forms.CharField(widget=forms.Textarea, label="Conținut CSV (; separator)")
