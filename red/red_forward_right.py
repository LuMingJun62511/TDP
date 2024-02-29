from roles.red_forward import RedForward


def play(red_players, blue_players, ball):
    decisions = []   
    for player in red_players:
        if player['role'] == 'forward' and player['number'] == 4:
            forwrad = RedForward(color='red',**player)
            decisions.extend(forwrad.decide_action(ball, red_players,blue_players))           
    return decisions


