from django.contrib.auth.models import User
from django.db import models

from django.utils import timezone

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

class Team(models.Model):
    name = models.CharField(max_length=50)
    fifa_code = models.CharField(max_length=3)
    flag_code = models.CharField(max_length=6)

    active = models.BooleanField(default=True)

    def flag_url(self):
        return f"https://flagcdn.com/{self.flag_code}.svg"

    def __str__(self):
        return self.name

class Stage(models.Model):
    name = models.CharField(max_length=50)
    order = models.IntegerField()

    def __str__(self):
        return self.name

class Match(models.Model):
    home_team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name="local",
        blank=True,
        null=True
    )
    away_team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name="visitor",
        blank=True,
        null=True
    )
    stage = models.ForeignKey(
        Stage,
        on_delete=models.CASCADE
    )

    matchday = models.IntegerField(null=True, blank=True)

    date = models.DateTimeField()
    home_score = models.IntegerField(null=True, blank=True)
    away_score = models.IntegerField(null=True, blank=True)
    group = models.CharField(max_length=1, null=True, blank=True)
    
    locked = models.BooleanField(default=False)
    played = models.BooleanField(default=False)

    def is_open(self):
        return not self.locked and not self.played and timezone.now() < self.date
    
    def calculate_scores(self):
        if not self.played or self.home_score is None or self.away_score is None:
            return
        
        predictions = self.predictions.all()

        if self.home_score > self.away_score:
            real_result = 1
        elif self.home_score < self.away_score:
            real_result = -1
        else:
            real_result = 0

        for pred in predictions:
            points_earned = 0

            if pred.home_prediction == self.home_score and pred.away_prediction == self.away_score:
                points_earned = 3
            else:
                if pred.home_prediction > pred.away_prediction:
                    pred_result = 1
                elif pred.home_prediction < pred.away_prediction:
                    pred_result = -1
                else:
                    pred_result = 0
            
                if pred_result == real_result:
                    points_earned = 1
        
            Score.objects.update_or_create(
                user=pred.user,
                match=self,
                defaults={'points': points_earned}
            )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.played:
            self.calculate_scores()
    
class Score(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="scores"
    )
    match = models.ForeignKey(
        Match,
        on_delete=models.CASCADE,
        related_name="scores"
    )
    points = models.IntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'match'], name='unique_user_match_score')
        ]

class Prediction(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="predictions"
    )
    match = models.ForeignKey(
        Match,
        on_delete=models.CASCADE,
        related_name="predictions"
    )
    home_prediction = models.IntegerField()
    away_prediction = models.IntegerField()
    created_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'match'], name='unique_user_match_predictions')
        ]