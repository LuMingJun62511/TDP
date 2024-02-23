from utils import get_direction, get_distance
from models.player import Player


class BlueDefender(Player):
    def __init__(self, x, y, name, number, color, radius, img=None, ban_cycles=0, role=None, direction=0):
        super().__init__(x, y, name, number, color, radius, img, ban_cycles, role, direction)

    def decide_action(self, ball, players):
        decisions = []
        strategic_position = self.calculate_strategic_position(ball, players)
        # 挨个写测试案例，保证每个分支都被测试到了
        if self.own_half(ball):  # For blue team, the own half is the positive x 
            if ball['owner_color'] == self.color:
                if self.owns_ball(ball): #传球这几条没问题
                    pass_decision = self.pass_to_teammates(players, ball)
                    if pass_decision:
                        decisions.append(pass_decision)
                    else:
                        decisions.append(self.move_towards_goal(ball))
                else: #跑点至少跑到了，就看这个move_to_strategic_position
                    decisions.append(self.move_to_strategic_position(strategic_position))
            elif self.is_closest_to_ball(players, ball): 
                decisions.append(self.intercept_ball(ball, players))
        elif not self.in_strategic_position():
            decisions.append(self.move_to_strategic_position(strategic_position))
        else:
            decisions.append(self.face_ball_direction(ball)) #行吧，这里有问题，这里会一直背对着球，这显然不合适

        return decisions

    def calculate_strategic_position(self, ball, players):
        if not self.own_half(ball):  # For blue team, the own half is the positive x
            if ball['owner_color'] == self.color:
                return self.calculate_offensive_strategic_position(ball, players)
            else:
                return self.calculate_defensive_strategic_position(ball, players)
        else:
            return self.default_strategic_position()

    def default_strategic_position(self):
        # Adjust for blue team orientation
        return {'x': 300, 'y': -100}  # Adjusted example value for blue team

    def calculate_defensive_strategic_position(self, ball, players):
        goal_x = 450  # Goal location for blue team
        goal_y = 0
        midpoint_x = (ball['x'] + goal_x) / 2
        midpoint_y = (ball['y'] + goal_y) / 2
        adjusted_x = min(max(midpoint_x, 300), 350)  # Adjusted for blue team's defensive zone
        adjusted_y = max(min(midpoint_y, 100), -300)  # Adjust y-axis positioning
        return {'x': adjusted_x, 'y': adjusted_y}

    def calculate_offensive_strategic_position(self, ball, players):
        if self.owns_ball(ball):
            return {'x': self.x, 'y': self.y}  # Maintain current position if the defender owns the ball
        else:
            supporting_x = max(self.x - 100, -300)  # Adjusted logic for blue team moving forward
            supporting_y = self.y  # Maintain y position
            return {'x': supporting_x, 'y': supporting_y}

    def in_strategic_position(self):
        # Adjust for blue team's strategic positioning checks
        strategic_x_min, strategic_x_max = 0, 400  # Adjusted range for blue team
        strategic_y_min, strategic_y_max = -100, 100
        return strategic_x_min <= self.x <= strategic_x_max and strategic_y_min <= self.y <= strategic_y_max

    # Example method to adjust for new strategic positioning
    def move_to_strategic_position(self, strategic_pos):
        direction_to_strategic_pos = get_direction({'x': self.x, 'y': self.y}, strategic_pos)
        return {
            'type': 'move',
            'player_number': self.number,
            'destination': strategic_pos,
            'direction': direction_to_strategic_pos,
            'speed': 7,  # Adjust speed based on the urgency of repositioning
            'has_ball':False
        }

    def move_to_middle(self,ball,players):
        for player in players:
            if player['role'] == 'defender' and player['number'] != self.number:
                another_defender = player
        destination = {'x':(ball['x'] + another_defender['x']) / 2,'y':(ball['y'] + another_defender['y']) / 2}
        return {
            'type': 'move',
            'player_number': self.number,
            'destination': destination,
            'direction': get_direction({'x': self.x, 'y': self.y},destination),
            'speed': 7,  # Adjust speed based on the urgency of repositioning
            'has_ball':False
        }

    def owns_ball(self, ball):
        return ball['owner_number'] == self.number and ball['owner_color'] == self.color
    
    def pass_to_teammates(self, players, ball):
        most_advanced_teammate = None
        max_advance_x = float('inf')  # Initialize with a very small number

        for player in players:
            if player['number'] != self.number and player['role'] != 'goalkeeper':
                # Check if this player is more advanced towards the opponent's goal
                if player['x'] < max_advance_x:
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
        if self.color == 'red':
            goal_position = {'x': 450, 'y': 0}
        else:
            goal_position = {'x': -450, 'y': 0}
        direction_to_goal = get_direction({'x': self.x, 'y': self.y}, goal_position)
        return {
            'type': 'move', 
            'player_number': self.number, 
            'destination': goal_position, 
            'direction': direction_to_goal, 
            'speed': 7,
            'has_ball':True
        }

    def face_ball_direction(self, ball):
        direction_to_ball = get_direction({'x': self.x, 'y': self.y}, {'x': ball['x'], 'y': ball['y']})
        return {
            'type': 'move', 
            'player_number': self.number, 
            'destination': {'x': self.x, 'y': self.y}, 
            'direction': direction_to_ball,
            'speed': 1,
            'has_ball':False
        }

    def move_to_strategic_position(self, strategic_position):
        strategic_pos = strategic_position
        direction_to_strategic_pos = get_direction({'x': self.x, 'y': self.y}, strategic_pos)
        return {
            'type': 'move', 
            'player_number': self.number, 
            'destination': strategic_pos, 
            'direction': direction_to_strategic_pos, 
            'speed': 7,
            'has_ball':False
        }

    def is_closest_to_ball(self, players, ball):
        """Check if this forward is the closest to the ball among two forwards."""
        own_distance = get_distance({'x': self.x, 'y': self.y}, {'x': ball['x'], 'y': ball['y']})
        other_forward = [player for player in players if player['role'] == 'forward' and player['number'] != self.number][0]
        other_distance = get_distance({'x': other_forward['x'], 'y': other_forward['y']}, {'x': ball['x'], 'y': ball['y']})
        return own_distance < other_distance

    def intercept_ball(self, ball,players):
        """Move towards the ball to intercept it."""
        direction_to_ball = get_direction({'x': self.x, 'y': self.y}, {'x': ball['x'], 'y': ball['y']})
        distance_to_ball = get_distance({'x': self.x, 'y': self.y}, {'x': ball['x'], 'y': ball['y']})
        if distance_to_ball > 10:
            if ball['owner_color'] == self.color:
                speed = 5
                destination = self.calculate_strategic_position(ball,players)
            else:
                speed = 10
                destination = {'x': ball['x'], 'y': ball['y']}
            return {
                'type': 'move',
                'player_number': self.number,
                'destination': destination,
                'direction': direction_to_ball,
                'speed': speed,  # This speed can be adjusted based on gameplay needs
                'has_ball':False
            }
        else:
            return self.grab_ball(ball)
    
    def grab_ball(self,ball):
        direction_to_ball = get_direction({'x': self.x, 'y': self.y}, {'x': ball['x'], 'y': ball['y']})
        return {
            'type': 'grab',
            'player_number': self.number,
            'direction': direction_to_ball,
        }
    
    def own_half(self,ball):
        x = ball['x']
        x1 = 0
        x2 = 450
        return x1 < x < x2