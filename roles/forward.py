# forward.py
from utils import get_direction, get_distance
from .role import Role
from models import player

class Forward(player.Player):
    def __init__(self, x,y,name, number, color,radius,img=None, ban_cycles=0,role=None,direction=0):
        super().__init__(x,y,name, number, color,radius,img, ban_cycles,role,direction)

    def decide_action(self, ball, players):
        decisions = []
        if ball['owner_color'] == self.color:
            print(ball['x'],ball['y'],"当前球的位置")
            if ball['owner_color'] == self.color:
                if self.owns_ball(ball):
                    pass_decision = self.pass_to_teammates(players, ball)
                    if pass_decision:
                        #print("Defender is passing the ball")
                        decisions.append(pass_decision)
                    else:
                        #print("Defender is moving towards goal")
                        decisions.append(self.move_towards_goal(ball))
        else:
            decisions.append(self.move_towards_ball(ball))
        return decisions
            #elif not self.in_strategic_position():
            #    decisions.append(self.move_to_strategic_position(strategic_position))
            #else:
            #    decisions.append(self.face_ball_direction(ball))

    def move_towards_ball(self,ball):
        # Example action to move towards the ball
        print(f"Forward {self.number} moving towards the ball at {ball['x']}, {ball['y']}")
        direction = get_direction({'x': self.x, 'y': self.y}, {'x': ball['x'], 'y': ball['y']})
        return {
            'type': 'move',
            'player_number': self.number,
            'destination': ball,
            'direction': direction,
            'speed': 10,  # Speed might be adjusted based on the situation
        }

    def attempt_to_score(self, player, goal_position):
        # Example action to attempt scoring
        print(f"Forward {self.number} attempting to score")
        direction = get_direction(player, goal_position)
        return {
            'type': 'kick',
            'player_number': self.number,
            'direction': direction,
            'power': 60,  # Power might be adjusted based on distance to goal
        }
    

    def owns_ball(self, ball):
        return ball['owner_number'] == self.number
    
    def pass_to_teammates(self, players, ball):
        most_advanced_teammate = None
        max_advance_x = -float('inf')  # Initialize with a very small number

        for player in players:
            if player['number'] != self.number and player['role'] != 'goalkeeper':
                # Check if this player is more advanced towards the opponent's goal
                if player['x'] > max_advance_x:
                    most_advanced_teammate = player
                    max_advance_x = player['x']
        
        if most_advanced_teammate:
            direction_to_teammate = get_direction({'x': self.x, 'y': self.y}, {'x': most_advanced_teammate['x'], 'y': most_advanced_teammate['y']})
            return {
                'type': 'kick',
                'player_number': self.number,
                'direction': direction_to_teammate,
                'power': 50  # Adjust power as necessary
            }
        else:
            return None
        
    def move_towards_goal(self, ball):
        goal_position = {'x': 500, 'y': 0}
        direction_to_goal = get_direction({'x': self.x, 'y': self.y}, goal_position)
        return {'type': 'move', 'player_number': self.number, 'destination': goal_position, 'direction': direction_to_goal, 'speed': 7}
