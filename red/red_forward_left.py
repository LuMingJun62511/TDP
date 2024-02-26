from roles.red_forward import RedForward


def play(red_players, blue_players, ball):
    decisions = []   
    # Loop through each player in the red team
    for player in red_players:
        if player['role'] == 'forward':
            # Forwards could have their own logic for attacking plays or positioning
            # This could involve moving towards the goal, attempting shots, or positioning for passes
            forwrad = RedForward(color='red',**player)
            decisions.extend(forwrad.decide_action(ball, red_players,blue_players))           
    return decisions


