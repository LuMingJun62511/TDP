import exception
from utils import utils,game,size
from .decision import Decision
import math
from models import Point


class MoveDecision(Decision):
    def __init__(self, runner, player_number, player_color, destination,direction, speed):
        super().__init__(runner, player_number, player_color)
        self.destination = destination
        self.direction = direction
        self.speed = speed

    def validate(self):
        super().validate()
        if not 0 <= self.speed <= game.MAX_PLAYER_SPEED:
            raise exception.DecisionException('Wrong move speed')
        if not -size.FOOTBALL_PITCH_LENGTH // 2 < self.destination.x < size.FOOTBALL_PITCH_LENGTH // 2 or \
                not -size.FOOTBALL_PITCH_WIDTH // 2 < self.destination.y < size.FOOTBALL_PITCH_WIDTH // 2:
            raise exception.DecisionException('Cannot move out of screen')
    

    def perform(self): # 原版
        distance = utils.distance(self.player, self.destination)
        print('——————————————————————',self.player)
        print('——————————————————————',self.destination.x)

        alpha = math.atan2((self.destination.y - self.player.y), (self.destination.x - self.player.x))
        
        if distance < self.speed: #一步到位
            self.player.x = int(self.destination.x)
            self.player.y = int(self.destination.y)
            self.player.direction = alpha
        
        else: #正常走一tick,pfa就是修改了speed和alpha,
            alpha = math.atan2((self.destination.y - self.player.y), (self.destination.x - self.player.x))
            #alpha = direction
            self.player.x += int(self.speed * math.cos(alpha))
            self.player.y += int(self.speed * math.sin(alpha))
            self.player.direction = alpha
            self.player.speed = self.speed
        
    # def perform(self):
    #     #self.player.move(self.destination,self.direction, self.speed) #计算与目的地的距离与角度差
    #     movement,alpha = self.pfa()
    #     if movement < self.speed: #一步到位
    #         self.player.x = int(self.destination.x)
    #         self.player.y = int(self.destination.y)
    #         self.player.direction = alpha
    #     else: #正常走一tick,pfa就是修改了speed和alpha,
    #         self.player.x += int(movement * math.cos(alpha))
    #         self.player.y += int(movement * math.sin(alpha))
    #         self.player.direction = alpha
    #         self.player.speed = movement
     
            
    # def get_enemy_team_position(self):
    #     # 根据当前球员的颜色决定敌方球队
    #     enemy_team = self.runner.blue_players if self.player.color == 'red' else self.runner.red_players
    #     enemy_team_position = [(player.x, player.y) for player in enemy_team]
    #     return enemy_team_position
    
    # # 其实，该函数可以进一步改进，改为对敌人要较早的避开，对队友可以较晚的避开，就达成了防重叠，现版本只有避敌
    # def pfa(self):
    #     enemy_team_position = self.get_enemy_team_position()
    #     attract_force = self.calculate_attract_force()
    #     repulse_forces = [self.calculate_repulse_force(enemy_pos_tuple) for enemy_pos_tuple in enemy_team_position]
    #     total_force = self.combine_forces(attract_force, repulse_forces)
    #     alpha = math.atan2(total_force[1], total_force[0])# 计算总力的方向
    #     speed = min(self.speed, math.sqrt(total_force[0]**2 + total_force[1]**2))# 计算移动距离，这里假设speed是一个基于力大小的动态值
    #     return speed, alpha

    # def calculate_attract_force(self):
    #     # 根据球员与目的地之间的距离计算吸引力
    #     distance_to_destination = utils.distance(self.player, self.destination)
    #     direction_to_destination = math.atan2((self.destination.y - self.player.y), (self.destination.x - self.player.x))
    #     attract_force = (math.cos(direction_to_destination) * distance_to_destination, math.sin(direction_to_destination) * distance_to_destination)
    #     return attract_force

    # def calculate_repulse_force(self, enemy_pos_tuple):
    #     enemy_pos = Point(enemy_pos_tuple[0], enemy_pos_tuple[1])
    #     # 计算当前球员与敌方球员之间的距离
    #     distance_to_enemy = utils.distance(self.player, enemy_pos)
    #     # 计算指向敌方球员的方向
    #     direction_to_enemy = math.atan2((enemy_pos.y - self.player.y), (enemy_pos.x - self.player.x))
    #     # 根据距离计算排斥力的强度（这里需要您根据实际情况调整计算方式）
    #     repulse_strength = max(0, 1 - (distance_to_enemy / self.player.radius*1.2))  # 假设有一个排斥距离阈值属性,self.repulse_distance_threshold,暂定为self.player.radius*1.2
    #     repulse_force = (-math.cos(direction_to_enemy) * repulse_strength, -math.sin(direction_to_enemy) * repulse_strength)
    #     return repulse_force

    # def combine_forces(self, attract_force, repulse_forces):
    #     # 合成吸引力和排斥力
    #     total_force_x = attract_force[0] + sum(force[0] for force in repulse_forces)
    #     total_force_y = attract_force[1] + sum(force[1] for force in repulse_forces)
    #     return (total_force_x, total_force_y)

    # def update_movement(self, total_force):
    #     # 根据合成力更新球员位置
    #     direction = math.atan2(total_force[1], total_force[0])
    #     self.player.x += int(self.speed * math.cos(direction))
    #     self.player.y += int(self.speed * math.sin(direction))
    #     self.player.direction = direction
    #     self.player.speed = self.speed
