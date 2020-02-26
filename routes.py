from flask_restplus import Namespace, Resource
from flask import session, jsonify

from CTFd.models import Solves, Challenges
from CTFd.cache import cache, make_cache_key
from CTFd.utils.scores import get_standings
from CTFd.utils import get_config
from CTFd.utils.modes import get_model, TEAMS_MODE
from CTFd.utils.dates import unix_time
from CTFd.utils.decorators import (
    during_ctf_time_only
)
from CTFd.utils.decorators.visibility import (
    check_challenge_visibility,
    check_score_visibility,
	check_account_visibility
)
from CTFd.utils.config.visibility import (
    scores_visible,
    accounts_visible,
    challenges_visible,
)
from sqlalchemy.sql import or_, and_, any_

ctftime_namespace = Namespace('ctftime', description="Endpoint to retrieve scores for ctftime")


def unicode_safe(string):
	return string.encode('unicode_escape').decode()

@ctftime_namespace.route('')
class ScoreboardList(Resource):
	@check_challenge_visibility
	@check_score_visibility
	@cache.cached(timeout=60, key_prefix=make_cache_key)
	def get(self):
		response = {
			'tasks': [],
			'standings': []
		}

		mode = get_config("user_mode")
		freeze = get_config("freeze")

		challenges = Challenges.query.filter(
			and_(Challenges.state != 'hidden', Challenges.state != 'locked')
		).order_by(Challenges.value).all()

		challenges_ids={}
		for i, x in enumerate(challenges):
			response['tasks'].append(unicode_safe(x.name)+" "+str(x.value))
			challenges_ids[x.id]=x.name

		if mode == TEAMS_MODE:
			standings = get_standings()
			team_ids = [team.account_id for team in standings]

		solves = Solves.query.filter(Solves.account_id.in_(team_ids))
		if freeze:
			solves = solves.filter(Solves.date < unix_time_to_utc(freeze))	

		for i, team in enumerate(team_ids):
			team_standing = {
				'pos': i+1,
				'team': unicode_safe(standings[i].name),
				'score': float(standings[i].score),
				'taskStats': {}
			}
			team_solves = solves.filter(Solves.account_id == standings[i].account_id)
			for solve in team_solves:
				chall_name = challenges_ids[solve.challenge_id]
				team_standing["taskStats"][unicode_safe(chall_name)] ={
					"points": solve.challenge.value,
					"time": unix_time(solve.date),
				}
			response['standings'].append(team_standing)
		return response
