from . import db

class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    league_sport_division_team = db.Column(db.String(500), unique=True)
    league = db.Column(db.String(150))
    sport = db.Column(db.String(150))
    division = db.Column(db.Integer)
    team = db.Column(db.String(150))
    wins = db.Column(db.Integer)
    losses = db.Column(db.Integer)
    draws = db.Column(db.Integer)
    games = db.relationship('Game')


class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    your_team = db.Column(db.String(150))
    opponent_team = db.Column(db.String(150))
    your_team_score = db.Column(db.Integer)
    opponent_team_score = db.Column(db.Integer)
    win_lose = db.Column(db.Integer)
    date = db.Column(db.DateTime)
    team_id = db.Column(db.Integer, db.ForeignKey("team.id"))


class BasketballPlayerStats(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    num = db.Column(db.Integer)
    name = db.Column(db.String(100))
    field_goals = db.Column(db.Integer)
    field_goals_attempted = db.Column(db.Integer)
    field_goal_percent = db.Column(db.String(10))
    three_pointers = db.Column(db.Integer)
    three_pointers_attempted = db.Column(db.Integer)
    three_pointer_percent = db.Column(db.String(10))
    free_throws = db.Column(db.Integer)
    free_throws_attempted = db.Column(db.Integer)
    free_throw_percent = db.Column(db.String(10))
    rebounds = db.Column(db.Integer)
    assists = db.Column(db.Integer)
    points = db.Column(db.Integer)
    game_id = db.Column(db.Integer, db.ForeignKey("game.id"))


class SoccerPlayerStats(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    num = db.Column(db.Integer)
    name = db.Column(db.String(100))
    assists = db.Column(db.Integer)
    saves = db.Column(db.Integer)
    shots_taken = db.Column(db.Integer)
    goals = db.Column(db.Integer)
    tackles = db.Column(db.Integer)
    interceptions = db.Column(db.Integer)
    game_id = db.Column(db.Integer, db.ForeignKey("game.id"))
