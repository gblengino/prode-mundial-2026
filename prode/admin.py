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

admin.site.register(Prediction)

admin.site.register(Score)

