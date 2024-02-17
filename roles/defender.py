import pygame as pg
from utils import get_direction, get_distance
from .role import Role

class Defender(Role):
    def __init__(self, color, number):
        super().__init__(color, number)
        # Assuming the player's initial position is set here or elsewhere
        self.x = 0
        self.y = 0

    def action_decision(self, ball, players, own_half, strategic_position):
        decisions = []

        if self.collision_detection(ball):
            if not self.owns_ball(ball):
                decisions.append(self.execute_bounce_action(ball))
        
        if own_half(ball):
            if self.owns_ball(ball):
                pass_decision = self.pass_to_teammates(players, ball)
                if pass_decision:
                    decisions.append(pass_decision)
                else:
                    decisions.append(self.move_towards_goal(ball))
            elif self.in_strategic_position(strategic_position, self):
                decisions.append(self.face_ball_direction(ball))
            else:
                decisions.append(self.move_to_strategic_position(strategic_position))
        else:
            if self.in_strategic_position(strategic_position, self):
                decisions.append(self.face_ball_direction(ball))
            else:
                decisions.append(self.move_to_strategic_position(strategic_position))

        return decisions

    def collision_detection(self, ball):
        # Adjusted to use 'x' and 'y' directly
        return get_distance({'x': self.x, 'y': self.y}, {'x': ball['x'], 'y': ball['y']}) <= 10

    def owns_ball(self, ball):
        return ball['owner_number'] == self.number

    def execute_bounce_action(self, ball):
        direction_away_from_ball = get_direction({'x': ball['x'], 'y': ball['y']}, {'x': self.x, 'y': self.y})
        return {'type': 'move', 'player_number': self.number, 'direction': direction_away_from_ball, 'speed': 0}

    def pass_to_teammates(self, players, ball):
        closest_teammate = None
        min_distance = float('inf')
        for player in players:
            if player['number'] != self.number:
                distance = get_distance({'x': self.x, 'y': self.y}, {'x': player['x'], 'y': player['y']})
                if distance < min_distance:
                    closest_teammate = player
                    min_distance = distance
        
        if closest_teammate:
            direction_to_teammate = get_direction({'x': self.x, 'y': self.y}, {'x': closest_teammate['x'], 'y': closest_teammate['y']})
            return {'type': 'kick', 'player_number': self.number, 'direction': direction_to_teammate, 'power': 50}
        else:
            return None

    def move_towards_goal(self, ball):
        goal_position = {'x': 500, 'y': 0}
        direction_to_goal = get_direction({'x': self.x, 'y': self.y}, goal_position)
        return {'type': 'move', 'player_number': self.number, 'destination': goal_position, 'direction': direction_to_goal, 'speed': 7}

    def in_strategic_position(self, strategic_position, player):
        return strategic_position(player)

    def face_ball_direction(self, ball):
        direction_to_ball = get_direction({'x': self.x, 'y': self.y}, {'x': ball['x'], 'y': ball['y']})
        return {'type': 'move', 'player_number': self.number, 'destination': {'x': self.x, 'y': self.y}, 'direction': direction_to_ball, 'speed': 0}

    def move_to_strategic_position(self, strategic_position):
        strategic_pos = strategic_position()
        direction_to_strategic_pos = get_direction({'x': self.x, 'y': self.y}, strategic_pos)
        return {'type': 'move', 'player_number': self.number, 'destination': strategic_pos, 'direction': direction_to_strategic_pos, 'speed': 7}


    # 当球不在我方半场时，后卫应该根据他们相对于球门的位置来选择球门。如果两名后卫都在同一侧，那么他们需要根据距离另一个球门的远近来选择谁去防守哪个球门。
    # 当球在我方半场，无论另一后卫是在追球还是持球，总之，当它不在正常防守，我就要补弱，否则，我们呢正常防守，且对手持球，最近的后卫追球，另一名后卫应选择远离球的球门来进行防守。这两个合并
    # 当球在我方半场，我方持球但本人不持球时，应考虑补弱侧的策略，即选择相对远离球的球门。

    def calculate_distances_in_strategy(defender_itself, defender_other, goalpost_1, goalpost_2,ball):
        defender_itself_to_goalpost_1 = get_distance({'x': defender_itself['x'], 'y': defender_itself['y']}, {'x': goalpost_1['x'], 'y': goalpost_1['y']})
        defender_itself_to_goalpost_2 = get_distance({'x': defender_itself['x'], 'y': defender_itself['y']}, {'x': goalpost_2['x'], 'y': goalpost_2['y']})
        defender_other_to_goalpost_1 = get_distance({'x': defender_other['x'], 'y': defender_other['y']}, {'x': goalpost_1['x'], 'y': goalpost_1['y']})
        defender_other_to_goalpost_2 = get_distance({'x': defender_other['x'], 'y': defender_other['y']}, {'x': goalpost_2['x'], 'y': goalpost_2['y']})
        
        defender_itself_to_ball = get_distance({'x': defender_other['x'], 'y': defender_other['y']}, {'x': ball['x'], 'y': ball['y']})
        defender_other_to_ball = get_distance({'x': defender_other['x'], 'y': defender_other['y']}, {'x': ball['x'], 'y': ball['y']})

        return defender_itself_to_goalpost_1,defender_itself_to_goalpost_2,defender_other_to_goalpost_1,defender_other_to_goalpost_2,defender_itself_to_ball,defender_other_to_ball


    def determine_goalpost_by_sidedness(defender_itself, defender_other, goalpost_1, goalpost_2,ball):
        defender_itself_to_goalpost_1,defender_itself_to_goalpost_2,defender_other_to_goalpost_1,defender_other_to_goalpost_2,defender_itself_to_ball,defender_other_to_ball = calculate_distances_in_strategy(defender_itself, defender_other, goalpost_1, goalpost_2,ball)
        goalpost = goalpost_1
        if not self.on_both_sides(ball):#如果两名后卫在异侧
            goalpost = goalpost_1 if defender_itself_to_goalpost_1 < defender_itself_to_goalpost_2 else goalpost_2
        else:   #如果两名后卫在同侧
            if defender_itself_to_goalpost_1 < defender_itself_to_goalpost_2: #在同侧，且都离门柱1近
                goalpost = goalpost_2 if defender_itself_to_goalpost_2 < defender_other_to_goalpost_2 else goalpost_1 #相对离门柱2近的过去
            else: #在同侧，且都离门柱2近
                goalpost = goalpost_1 if defender_itself_to_goalpost_1 < defender_other_to_goalpost_1 else goalpost_2 #相对离门柱2近的过去
        return goalpost

    def choose_goalpost(defender_itself, defender_other, goalpost_1, goalpost_2,ball):
        goalpost = goalpost_1
        defender_itself_to_goalpost_1,defender_itself_to_goalpost_2,defender_other_to_goalpost_1,defender_other_to_goalpost_2,defender_itself_to_ball,defender_other_to_ball = calculate_distances_in_strategy(defender_itself, defender_other, goalpost_1, goalpost_2,ball)

        if not self.own_half(ball):# 当球不在我方半场时
            goalpost = determine_goalpost_by_sidedness(defender_itself, defender_other, goalpost_1, goalpost_2,ball)
        else:#当球在我方半场
            if not self.red_team_owns_ball(ball):#我方还不持球，一旦另一个后卫在追球或持球，则我要补它另一侧，
                if defender_itself_to_ball > defender_other_to_ball:#我不追球，就要看另一人
                    goalpost = goalpost_2 if defender_other_to_goalpost_1 < defender_other_to_goalpost_2 else goalpost_1#如果追球人离1柱比较近，我就去守2柱
            elif not self.red_team_owns_ball(ball) :#我方持球但我不持球，
                if not self.owns_ball(defender_other,ball):#如果另一队员和我一样不持球，则考虑一般性的异侧正常，同侧补弱，
                    goalpost = determine_goalpost_by_sidedness(defender_itself, defender_other, goalpost_1, goalpost_2,ball)
                else: #如果另一人持球，则它离1柱比较近，我去守2柱
                    goalpost = goalpost_2 if defender_other_to_goalpost_1 < defender_other_to_goalpost_2 else goalpost_1
        return goalpost


    def on_both_sides(defender_itself, defender_other):
        # 都在中线或一个在中线就视为异侧
        return defender_itself['y']*defender_other['y'] > 0


    def red_team_owns_ball(ball):
        return ball['owner_color'] == 'red'