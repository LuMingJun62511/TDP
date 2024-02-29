from roles.red_defender import RedDefender


def play(red_players, blue_players, ball):
    decisions = []   
    for player in red_players:
        if player['role'] == 'defender' and player['number'] == 1:
            defender = RedDefender(color='red',**player)
            decisions.extend(defender.decide_action(ball, red_players,blue_players))           
    return decisions


