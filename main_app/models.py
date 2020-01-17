from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
from main_app.views import convert_base, url_alph, get_suffix


class Voting(models.Model):
    question = models.CharField(max_length=50)
    type = models.CharField(max_length=20, default='radio')  # radio, checkbox, text_input
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    def options(self):
        return Options.objects.filter(voting_id=self.id)

    def users(self):
        return {e.user_id for e in Vote.objects.filter(voting_id=self.id)}

    def users_text(self):
        return {e.user_id for e in TextOption.objects.filter(voting_id=self.id)}

    def voting_view(self):
        return "/voting/" + str(self.id)


class Options(models.Model):
    voting = models.ForeignKey(to=Voting, on_delete=models.CASCADE)
    option = models.CharField(max_length=50)

    def votes(self):
        return {e.id for e in Vote.objects.filter(option_id=self.id)}

    def users(self):
        return {e.id for e in Vote.objects.filter(voting_id=self.voting_id)}

    def get_votes_percentage(self):
        return int(len(self.votes())/len(self.users())*100)

    # def get_votes_percentage_t(self):
    #     a = len(self.votes())/len(self.voting.users())*100
    #     return "{0:.2f}%".format(a) if not a in [0, 25, 50, 75, 100] else f"{int(a)}%"

    def get_votes_count_t(self):
        a = len(self.votes())
        return f"(Выбор {a}-{get_suffix(a, 'х', 'го', 'х')} пользовател{get_suffix(a, 'ей', 'я', 'ей')})"\
            if a else "(Никто ещё не выбирал этот вариант)"


class Vote(models.Model):
    voting = models.ForeignKey(Voting, on_delete=models.CASCADE)
    option = models.ForeignKey(Options, on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)


class TextOption(models.Model):
    voting = models.ForeignKey(Voting, on_delete=models.CASCADE)
    answer = models.CharField(max_length=1000)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)


