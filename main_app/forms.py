from django import forms


class VoteForm(forms.Form):
    ans = forms.CharField(label='Ваш ответ')
    voting_id = 0