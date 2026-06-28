from django.shortcuts import get_object_or_404, redirect, render
from django.forms import formset_factory
from django.db.models import Sum, Count, Q
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

from .services.standings import calculate_group_table
from .models import Match, Team, Prediction, User, Score
from .forms import PredictionForm

def index(request):
    
    groups = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L']

    data = {}

    for g in groups:
        matches = Match.objects.filter(
            stage__name="Fase de Grupos",
            group=g
        ).order_by("date")

        teams = Team.objects.filter(local__group=g).union(Team.objects.filter(visitor__group=g))

        data[g] = {
            "fixture":matches,
            "standings": calculate_group_table(matches, teams)
        }

    return render(request, "prode/index.html", {"data":data})

@login_required
def prode(request):

    current_stage = request.GET.get('stage', '16avos de Final')
    current_matchday = request.GET.get('matchday', '')

    if current_matchday:
        matches = Match.objects.filter(stage__name=current_stage, matchday=current_matchday).order_by('date')
    else:
        matches = Match.objects.filter(stage__name=current_stage).order_by('date')

    PredictionFormSet = formset_factory(PredictionForm, extra=0)

    if request.method == 'POST':
        formset = PredictionFormSet(request.POST)

        for form, m in zip(formset, matches):
            if m.home_team and m.away_team:
                form.fields['predicted_winner'].queryset = Team.objects.filter(id__in=[m.home_team.id, m.away_team.id])
            else:
                form.fields['predicted_winner'].queryset = Team.objects.none()

        if formset.is_valid():
            for form in formset:
                data = form.cleaned_data
                match_instance = data.get('match')
                home_pred = data.get('home_prediction')
                away_pred = data.get('away_prediction')
                predicted_winner = data.get('predicted_winner')

                if home_pred is not None and away_pred is not None: # Controla si el usuario realizo predicciones
                    if match_instance.is_open(): # Controla si el partido aun admite predicciones
                        Prediction.objects.update_or_create(
                            user = request.user,
                            match = data['match'],
                            defaults={
                                'home_prediction': data['home_prediction'],
                                'away_prediction': data['away_prediction'],
                                'predicted_winner': data['predicted_winner'],
                            }
                        )

            messages.success(request, 'Tus predicciones se guardaron correctamente. ¡Buena suerte!')

            return redirect('prode')
        else:
            print("Errores del formset: ", formset.errors)
            print("Errores no compartidos: ", formset.non_form_errors())
    else:
        initial_data = []
        for m in matches:
            pred = Prediction.objects.filter(user=request.user, match=m).select_related('match').first()
            initial_data.append({
                'match':m.id,
                'home_prediction':pred.home_prediction if pred else None,
                'away_prediction':pred.away_prediction if pred else None,
                'predicted_winner': pred.predicted_winner.id if pred and pred.predicted_winner else None,
            })
        
        formset = PredictionFormSet(initial=initial_data)

    for form, m in zip(formset, matches):
        if m.home_team and m.away_team:
            form.fields['predicted_winner'].queryset = Team.objects.filter(id__in=[m.home_team.id, m.away_team.id])
        else:
            form.fields['predicted_winner'].queryset = Team.objects.none()

    zipped_data = zip(matches, formset)
    
    return render(request, 'prode/prode.html', {'zipped_data':zipped_data, 'formset':formset, 'current_stage':current_stage, 'current_matchday':current_matchday})


def clasificacion(request):

    standings = User.objects.filter(
        is_active=True,
        is_staff=False
        ).annotate(
            total_points=Sum('scores__points'),
            plenos=Count('scores', filter=Q(scores__points=3))
            ).order_by('-total_points','-plenos','username')

    return render(request, 'prode/clasificacion.html', {'standings':standings})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('prode')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {"form":form})