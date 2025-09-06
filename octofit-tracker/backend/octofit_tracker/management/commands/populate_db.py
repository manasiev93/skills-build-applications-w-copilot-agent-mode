from django.core.management.base import BaseCommand
from django.conf import settings
from djongo import models
from pymongo import MongoClient

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        client = MongoClient('localhost', 27017)
        db = client['octofit_db']

        # Drop collections if they exist
        db.users.drop()
        db.teams.drop()
        db.activities.drop()
        db.leaderboard.drop()
        db.workouts.drop()

        # Create unique index on email for users
        db.users.create_index([("email", 1)], unique=True)

        # Sample users (super heroes)
        users = [
            {"name": "Iron Man", "email": "ironman@marvel.com", "team": "marvel"},
            {"name": "Captain America", "email": "cap@marvel.com", "team": "marvel"},
            {"name": "Spider-Man", "email": "spiderman@marvel.com", "team": "marvel"},
            {"name": "Batman", "email": "batman@dc.com", "team": "dc"},
            {"name": "Superman", "email": "superman@dc.com", "team": "dc"},
            {"name": "Wonder Woman", "email": "wonderwoman@dc.com", "team": "dc"},
        ]
        db.users.insert_many(users)

        # Sample teams
        teams = [
            {"name": "marvel", "members": [u["email"] for u in users if u["team"] == "marvel"]},
            {"name": "dc", "members": [u["email"] for u in users if u["team"] == "dc"]},
        ]
        db.teams.insert_many(teams)

        # Sample activities
        activities = [
            {"user": "ironman@marvel.com", "activity": "Running", "duration": 30},
            {"user": "batman@dc.com", "activity": "Cycling", "duration": 45},
            {"user": "spiderman@marvel.com", "activity": "Swimming", "duration": 20},
            {"user": "superman@dc.com", "activity": "Flying", "duration": 60},
        ]
        db.activities.insert_many(activities)

        # Sample leaderboard
        leaderboard = [
            {"team": "marvel", "points": 120},
            {"team": "dc", "points": 110},
        ]
        db.leaderboard.insert_many(leaderboard)

        # Sample workouts
        workouts = [
            {"user": "ironman@marvel.com", "workout": "Chest Press", "reps": 10},
            {"user": "wonderwoman@dc.com", "workout": "Deadlift", "reps": 12},
        ]
        db.workouts.insert_many(workouts)

        self.stdout.write(self.style.SUCCESS('octofit_db database populated with test data.'))
