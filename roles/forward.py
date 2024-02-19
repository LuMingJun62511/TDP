# forward.py
from utils import get_direction, get_distance
from .role import Role
from models import player

class Forward(player.Player):
    def __init__(self, x,y,name, number, color,radius,img=None, ban_cycles=0,role=None,direction=0):
        super().__init__(x,y,name, number, color,radius,img, ban_cycles,role,direction)

    def decide_action(self, ball, players,opponent_players):
        decisions = []
        strategic_position = self.calculate_strategic_position(ball, players)
        if not self.own_half(ball):
            if self.is_closest_to_ball(players, ball):
                if self.owns_ball(ball): #这个时候得知道躲避人了
                    #pass_decision = self.pass_to_teammates(players, ball)
                    pass_decision = self.find_best_receiver(players,opponent_players)
                    decisions.append(pass_decision if pass_decision else self.attempt_to_score(ball))
                else:
                    decisions.append(self.intercept_ball(ball,players))
            elif self.in_strategic_position():
                decisions.append(self.face_ball_direction(ball))
            else:
                decisions.append(self.move_to_strategic_position(strategic_position))
        elif self.in_strategic_position():
            decisions.append(self.face_ball_direction(ball))
        elif self.owns_ball(ball):
            decisions.append(self.attempt_to_score(ball))
        else:
            decisions.append(self.move_to_strategic_position(strategic_position))
         
        return decisions

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
            'has_ball':False
        }

    def attempt_to_score(self, ball):
        # Example action to attempt scoring
        
        if self.color == 'red':
            goal_position = {'x': 450, 'y': 0}
        else:
            goal_position = {'x': -450, 'y': 0}
        direction = get_direction({'x': self.x, 'y': self.y}, goal_position)
        if self.in_shoot_area():
            print(f"Forward {self.number} attempting to score")
            return {
                'type': 'kick',
                'player_number': self.number,
                'direction': direction,
                'power': 50,  # Power might be adjusted based on distance to goal
            }
        else:
            return self.move_towards_goal(ball)
    
    def in_shoot_area(self):
        if (self.color == 'red' and self.x > 300) or (self.color == 'blue' and self.x < -300):
            return True  #需要定义射门区域
        return False

    def calculate_strategic_position(self, ball, players):
        if not self.own_half(ball):
            # Scenario 1: Ball on our attacking half
            if ball['owner_color'] != self.color and not self.is_closest_to_ball(players, ball):
                # Move to a position that covers the farthest goal from the ball
                return self.calculate_defensive_strategic_position(ball, players)
            elif ball['owner_color'] == self.color and ball['owner_number'] != self.number:
                # Scenario when we own the ball or are closest to it
                return self.calculate_offensive_strategic_position(ball, players)
        else:
            return self.calculate_defensive_strategic_position(ball,players)

    def default_strategic_position(self):
        # Return a default strategic position based on the side of the field
        return {'x': 300, 'y': 100}  # Example value

    def calculate_defensive_strategic_position(self, ball, players):
        # Calculate defensive position based on ball and goal locations
        # Implement logic from documentation
        return {'x': 350, 'y': 100}  # Placeholder logic

    def calculate_offensive_strategic_position(self, ball, players):
        # Calculate offensive position when in possession but not holding the ball
        # Implement logic from documentation
        return {'x': 200, 'y': 100}  # Placeholder logic  
    
    def in_strategic_position(self):
        # Check if the defender is in a strategic position
        strategic_x_min, strategic_x_max = 400, 0
        strategic_y_min, strategic_y_max = 100, 100
        return strategic_x_min <= self.x <= strategic_x_max and strategic_y_min <= self.y <= strategic_y_max


    def is_closest_to_ball(self, players, ball):
        """Check if this defender is the closest to the ball among all forwards."""
        own_distance = get_distance({'x': self.x, 'y': self.y}, {'x': ball['x'], 'y': ball['y']})
        forwards = [player for player in players if player['role'] == 'forwards']
        for player in forwards:
            if player['number'] != self.number:
                if get_distance({'x': player['x'], 'y': player['y']}, {'x': ball['x'], 'y': ball['y']}) < own_distance:
                    return False
        return True

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
        
    def find_best_receiver(self,players, opponent_players):
        best_receiver = None
        min_opponent_distance = float('inf')
        min_goal_distance = float('inf')

        for player in players:
            if player['role'] != 'goalkeeper':
                opponent_distance = min([get_distance(player, opponent) for opponent in opponent_players])
                goal_distance = get_distance(player, {'x': 450 if self.color == 'red' else -450, 'y': 0})
                if opponent_distance > min_opponent_distance or (opponent_distance == min_opponent_distance and goal_distance < min_goal_distance):
                    best_receiver = player
                    min_opponent_distance = opponent_distance
                    min_goal_distance = goal_distance

        if best_receiver:
            direction_to_receiver = get_direction({'x': self.x, 'y': self.y}, {'x': best_receiver['x'], 'y': best_receiver['y']})
            return {
                'type': 'kick',
                'player_number': self.number,
                'direction': direction_to_receiver,
                'power': 50  # Adjust power as necessary
            }
        else:
            return None

    
    def move_towards_goal(self, ball):
        if self.color == 'red':
            goal_position = {'x': 350, 'y': 0}
        else:
            goal_position = {'x': -350, 'y': 0}
        direction_to_goal = get_direction({'x': self.x, 'y': self.y}, goal_position)
        return {
            'type': 'move', 
            'player_number': self.number,
            'destination': goal_position, 
            'direction': direction_to_goal, 
            'speed': 7,
            'has_ball':True
        }

    def move_to_strategic_position(self, strategic_pos):
        # Move to a predefined strategic position
        direction_to_strategic_pos = get_direction({'x': self.x, 'y': self.y}, strategic_pos)
        return {
            'type': 'move',
            'player_number': self.number,
            'destination': strategic_pos,
            'direction': direction_to_strategic_pos,
            'speed': 7,
            'has_ball':False
        }
    
    def face_ball_direction(self, ball):
        direction_to_ball = get_direction({'x': self.x, 'y': self.y}, {'x': ball['x'], 'y': ball['y']})
        return {
            'type': 'move', 
            'player_number': self.number, 
            'destination': {'x': self.x, 'y': self.y}, 
            'direction': direction_to_ball, 
            'speed': 0,
            'has_ball':False
        }

    
    def distance_to_ball(self,ball):
        return get_distance({'x': self.x, 'y': self.y}, {'x': ball['x'], 'y': ball['y']})


    def is_closest_to_ball(self, players, ball):
        """Check if this defender is the closest to the ball among all defenders."""
        own_distance = get_distance({'x': self.x, 'y': self.y}, {'x': ball['x'], 'y': ball['y']})
        #defenders = [players[1],players[2]]
        defenders = [player for player in players if player['role'] == 'defender']
        for player in defenders:
            if player['number'] != self.number:
                if get_distance({'x': player['x'], 'y': player['y']}, {'x': ball['x'], 'y': ball['y']}) < own_distance:
                    return False
        return True
    
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

    def is_in_goal_area(self,ball):
        if self.color == 'red':
            x = ball['x']
            y = ball['y']
            x1 = -450
            x2 = -350
            y1 = -150
            y2 = 150
        elif self.color == 'blue':
            x = ball['x']
            y = ball['y']
            x1 = 350
            x2 = 450
            y1 = -150
            y2 = 150
        else:
            print("错误的前锋属性")
        return x1 < x < x2 and y1 < y < y2
    
    def own_half(self,ball):
        if self.color == 'red':
            x = ball['x']
            x1 = -450
            x2 = 0
        elif self.color == 'blue':
            x = ball['x']
            x1 = 0
            x2 = 450
        else:
            print("错误的前锋属性")
        return x1 < x < x2