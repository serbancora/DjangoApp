from django.db import models
from django.contrib.auth.models import User
from datetime import date, timedelta

# Arbore ierarhic flexibil (Facultate > An > Materie > ...)
class Ierarhie(models.Model):
    nume = models.CharField(max_length=200)
    parinte = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='copii')

    def __str__(self):
        # Returnează numele nodului curent
        return self.nume

    def get_path(self):
        # Returnează calea de la rădăcină la nodul curent
        path = [self.nume]
        p = self.parinte
        while p:
            path.append(p.nume)
            p = p.parinte
        return " > ".join(reversed(path))

# Lecția efectivă, legată de un nod final
class Lectie(models.Model):
    nod_ierarhic = models.ForeignKey(Ierarhie, on_delete=models.CASCADE)
    titlu = models.CharField(max_length=200)

    def __str__(self):
        # Returnează titlul lecției și calea ierarhică
        return f"{self.titlu} ({self.nod_ierarhic.get_path()})"

# Flashcard asociat unei lecții
class Flashcard(models.Model):
    lectie = models.ForeignKey(Lectie, on_delete=models.CASCADE)
    intrebare = models.TextField()
    raspuns = models.TextField()

    def __str__(self):
        return self.intrebare[:80] 

# Progresul utilizatorului pentru algoritmul SM-2
class ReviewState(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    flashcard = models.ForeignKey(Flashcard, on_delete=models.CASCADE)
    last_reviewed = models.DateField(auto_now=True)
    ease_factor = models.FloatField(default=2.5)
    interval = models.IntegerField(default=1)
    repetitions = models.IntegerField(default=0)
    due_date = models.DateField(default=date.today)

    def update_review(self, grade):
        if grade < 3:
            self.repetitions = 0
            self.interval = 1
        else:
            self.repetitions += 1
            self.ease_factor = max(1.3, self.ease_factor + (0.1 - (5 - grade) * (0.08 + (5 - grade) * 0.02)))
            self.interval = int(self.interval * self.ease_factor)
        self.due_date = date.today() + timedelta(days=self.interval)
        self.save()
