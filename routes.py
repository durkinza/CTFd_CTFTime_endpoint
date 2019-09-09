from flask_restplus import Namespace, Resource
from flask import session, jsonify

from CTFd.models import Challenges
from CTFd.cache import cache, make_cache_key
from CTFd.utils.scores import get_standings
from CTFd.utils import get_config
from CTFd.utils.modes import get_mode_as_word, TEAMS_MODE
from CTFd.utils.dates import isoformat
from CTFd.utils.decorators import (
    during_ctf_time_only
)
from CTFd.utils.decorators.visibility import (
    check_challenge_visibility,
    check_score_visibility,
)
from CTFd.utils.config.visibility import (
    scores_visible,
    accounts_visible,
    challenges_visible,
)
from sqlalchemy.sql import or_, and_, any_

ctftime_namespace = Namespace('ctftime', description="Endpoint to retrieve scores for ctftime")


@ctftime_namespace.route('')
class ScoreboardList(Resource):
    @check_challenge_visibility
    @during_ctf_time_only
    @check_score_visibility
    @cache.cached(timeout=60, key_prefix=make_cache_key)
    def get(self):
        response = {
            'tasks': [],
            'standings': []
        }

        mode = get_config("user_mode")
        account_type = get_mode_as_word()

        challenges = Challenges.query.filter(
            and_(Challenges.state != 'hidden', Challenges.state != 'locked')
        ).order_by(Challenges.value).all()

        for i, x in enumerate(challenges):
            response['tasks'].append(x.name+" "+str(x.value))

        if mode == TEAMS_MODE:
            standings = get_standings()
            team_ids = [team.account_id for team in standings]

        for i, team in enumerate(team_ids):
            response['standings'].append({
                'pos': i+1,
                'team': standings[i].name,
                'score': float(standings[i].score)
            })

        return response
