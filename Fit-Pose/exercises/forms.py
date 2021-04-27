from django import forms

class RepsForm(forms.Form):
    max_reps = forms.IntegerField(label='Max reps', initial=10, min_value=1)