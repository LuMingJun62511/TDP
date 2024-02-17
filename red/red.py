import math
from roles import goalkeeper,defender,forward

def play(red_players, blue_players, ball, scoreboard):
    decisions = []
    goal_position = {'x': 500, 'y': 0}  # Example goal position for scoring

    for player in red_players:
        print('player:',player)
        print(f"Role type: {type(player['role'])}")
        if isinstance(player['role'], goalkeeper.GoalKeeper):
            print(f"Player {player['number']} is a goalkeeper.")
            goalie_decisions = player['role'].decide_action(ball, red_players)
            decisions.extend(goalie_decisions)
        elif isinstance(player['role'], defender.Defender):
            print(f"Player {player['number']} is a defender.")
            defender_decisions = player['role'].decide_action(ball, red_players)
            decisions.extend(defender_decisions)

    return decisions


