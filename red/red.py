from roles.red_goalkeeper import RedGoalKeeper
from roles.red_defender import RedDefender
from roles.red_forward import RedForward


def play(red_players, blue_players, ball):
    decisions = []   
    # Loop through each player in the red team
    for player in red_players:
        # Depending on the role, call the appropriate decision-making function
        if player['role'] == 'goalkeeper':
            goalkeeper = RedGoalKeeper(color='red',**player)
            decisions.extend(goalkeeper.decide_action(ball, red_players))
        elif player['role'] == 'defender':
            # Defenders make decisions based on ball possession and strategic positioning
            defender = RedDefender(color='red',**player)
            decisions.extend(defender.decide_action(ball, red_players))
    return decisions


