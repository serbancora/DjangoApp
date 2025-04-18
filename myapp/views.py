from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .models import Feature, Flashcard, Ierarhie
from .forms import FlashcardUploadForm

# Create your views here.
def index(request):
    root = Ierarhie.objects.get(nume="FlashCarduri")
    context = {"ierarhie": build_tree(root)}
    return render(request, "index.html", context)

def counter(request):
    text = request.POST['text']
    amount_of_words = len(text.split())
    return render(request, 'counter.html',{'amount': amount_of_words})

def post(request, pk):
    return render(request, 'post.html', {'pk': pk})

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        email = request.POST['email']

        if password == confirm_password:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Username taken')
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'Email taken')
                return redirect('register')
            else:
                user = User.objects.create_user(username=username, password=password, email=email)
                user.save()
                print('User created')
                return redirect('login')
        else:
            messages.info(request, 'Password not matching')
            return redirect('register')

    return render(request, 'register.html')

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('index')
        else:
            messages.info(request, 'Invalid credentials')
            return redirect('login')
    else:
        return render(request, 'login.html')
    
def logout(request):
    auth.logout(request)
    return redirect('index')

def courses(request):
    return render(request, 'courses.html')

def about(request):
    return render(request, 'about.html')

def upload_flashcards(request):
    if request.method == 'POST':
        form = FlashcardUploadForm(request.POST)
        if form.is_valid():
            lectie = form.cleaned_data['lectie']
            continut = form.cleaned_data['continut_csv']

            linii = continut.strip().split('\n')
            for linie in linii:
                if ';' in linie:
                    intrebare, raspuns = linie.split(';', 1)
                    Flashcard.objects.create(lectie=lectie, intrebare=intrebare.strip(), raspuns=raspuns.strip())

            return render(request, 'upload_success.html')
    else:
        form = FlashcardUploadForm()
    return render(request, 'upload_flashcards.html', {'form': form})

def serialize_ierarhie(nod):
    return {
        "id": nod.id,
        "nume": nod.nume,
        "copii": [serialize_ierarhie(copil) for copil in nod.copii.all()]
    }

def ierarhie_json(request):
    radacina = Ierarhie.objects.get(nume="FlashCarduri")
    data = serialize_ierarhie(radacina)
    return JsonResponse(data, safe=False)

def build_tree(nod):
    return {
        "nume": nod.nume,
        "copii": [build_tree(c) for c in nod.copii.all()]
    }
