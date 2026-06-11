from django import forms

from .models import Prediction, Match

class PredictionForm(forms.ModelForm):

    match = forms.ModelChoiceField(
        queryset=Match.objects.all(),
        widget=forms.HiddenInput
    )

    home_prediction = forms.IntegerField(
        required=False,
        widget= forms.NumberInput(attrs={
            'class': 'w-10 h-10 md:w-12 md:h-12 text-center text-xl font-bold rounded-lg focus:ring-2 focus:ring-emerald-500 outline-none border-none [appearance:textfield] [&::-webkit-outer-spin-button]:appearance-none [&::-webkit-inner-spin-button]:appearance-none',
            'placeholder': '-',
            'min': '0'
        })
    )

    away_prediction = forms.IntegerField(
        required=False,
        widget= forms.NumberInput(attrs={
            'class': 'w-10 h-10 md:w-12 md:h-12 text-center text-xl font-bold rounded-lg focus:ring-2 focus:ring-emerald-500 outline-none border-none [appearance:textfield] [&::-webkit-outer-spin-button]:appearance-none [&::-webkit-inner-spin-button]:appearance-none',
            'placeholder': '-',
            'min': '0'
        }),
    )

    class Meta:
        model = Prediction
        fields = ['home_prediction', 'away_prediction', 'match']