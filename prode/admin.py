from django.contrib import admin
from .models import Team, Stage, Match, Prediction, Score

admin.site.register(Team)

admin.site.register(Stage)

@admin.action(description="Asignar Matchday 1")
def set_matchday_1(modeladmin, request, queryset):
    queryset.update(matchday=1)

@admin.action(description="Asignar Matchday 2")
def set_matchday_2(modeladmin, request, queryset):
    queryset.update(matchday=2)

@admin.action(description="Asignar Matchday 3")
def set_matchday_3(modeladmin, request, queryset):
    queryset.update(matchday=3)

@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ('home_team','away_team','date','stage', 'group', 'matchday')
    list_filter = ('stage', 'group', 'matchday')
    search_fields = ('home_team__name', 'away_team__name')
    actions = [set_matchday_1, set_matchday_2, set_matchday_3]

@admin.register(Prediction)
class PredictionAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_home_team', 'get_away_team', 'home_prediction', 'away_prediction', 'predicted_winner', 'created_at',)
    list_select_related = ('match', 'user')
    list_filter = ('match__played', 'match__stage__name', 'match__matchday',)
    search_fields = ('user__username',)

    @admin.display(ordering='match__home_team', description='Local')
    def get_home_team(self, obj):
        return obj.match.home_team
    
    @admin.display(ordering='match__away_team', description='Visitante')
    def get_away_team(self, obj):
        return obj.match.away_team
    
@admin.register(Score)
class ScoreAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_home_team', 'get_away_team', 'points')
    list_filter = ('user',)

    @admin.display(ordering='match__home_team', description='Local')
    def get_home_team(self, obj):
        return obj.match.home_team
    
    @admin.display(ordering='match__away_team', description='Visitante')
    def get_away_team(self, obj):
        return obj.match.away_team

