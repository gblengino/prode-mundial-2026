from django import forms

from .models import Prediction, Match, Team

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

    predicted_winner = forms.ModelChoiceField(
        queryset=Team.objects.none(),
        required=False,
        label="Quien clasifica?",
        widget=forms.RadioSelect
    )

    class Meta:
        model = Prediction
        fields = ['home_prediction', 'away_prediction','predicted_winner', 'match']
    
    def __init__(self, *args, **kwargs):
        match_instance = kwargs.pop('match_instance', None)
        super().__init__(*args, **kwargs)
        
        if match_instance and match_instance.home_team and match_instance.away_team:
            # Filtramos el combo para que SOLO muestre los dos equipos que juegan
            self.fields['predicted_winner'].queryset = Team.objects.filter(
                id__in=[match_instance.home_team.id, match_instance.away_team.id]
            )