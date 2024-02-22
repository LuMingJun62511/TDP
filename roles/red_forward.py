# forward.py
from utils import get_direction, get_distance,how_to_grab
from utils import FOOTBALL_PITCH_LENGTH,FOOTBALL_PITCH_WIDTH
import numpy as np
from itertools import combinations
from models import player
import random
import heapq
class RedForward(player.Player):
    
    def __init__(self, x,y,name, number, color,radius,img=None, ban_cycles=0,role=None,direction=0):
        super().__init__(x,y,name, number, color,radius,img, ban_cycles,role,direction)
        self.historic_centers = []
        self.cost_map = [[1] * (FOOTBALL_PITCH_LENGTH // 50) for _ in range(FOOTBALL_PITCH_WIDTH // 50)]  # Default cost value


    def decide_action(self, ball, players,opponent_players):
        decisions = []
        #strategic_position = self.calculate_strategic_position(ball, players,opponent_players)
        self.update_cost_map(ball,players,opponent_players)
        #test = self.calculate_a_star_defensive_position(ball,players,opponent_players)
        if not self.own_half(ball):
            if self.is_closest_to_ball(players, ball):
                if self.owns_ball(ball):
                    pass_decision = self.pass_to_teammates(players,ball)
                    if pass_decision:
                        decisions.append(pass_decision)
                    elif self.opponent_in_randius(opponent_players):
                        decisions.append(self.random_kick_out(opponent_players))
                    else:
                        decisions.append(self.attempt_to_score(ball))
                else:
                    print(f"Forward {self.color} {self.number} is closet")
                    decisions.append(self.intercept_ball(ball,players,opponent_players))
            elif self.in_strategic_position(ball,players,opponent_players):
                decisions.append(self.face_ball_direction(ball))
            else:
                decisions.append(self.move_to_strategic_position(self.calculate_strategic_position(ball, players,opponent_players)))

        elif self.owns_ball(ball):
            if self.opponent_in_randius(opponent_players):
                decisions.append(self.random_kick_out(opponent_players))
            else:
                decisions.append(self.attempt_to_score(ball))
        elif self.in_strategic_position(ball,players,opponent_players):
            if self.is_closest_to_ball(players,ball):
                decisions.append(self.intercept_ball(ball,players,opponent_players))
            else:
                decisions.append(self.face_ball_direction(ball))        
        else:
            decisions.append(self.move_to_strategic_position(self.calculate_strategic_position(ball, players,opponent_players)))
         
        return decisions

    def move_towards_ball(self,ball):
        # Example action to move towards the ball
        #print(f"Forward {self.number} moving towards the ball at {ball['x']}, {ball['y']}")
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
            goal_position = {'x': 450, 'y': 0}
        else:
            goal_position = {'x': -450, 'y': 0}
            goal_position = {'x': -450, 'y': 0}
        direction = get_direction({'x': self.x, 'y': self.y}, goal_position)
        if self.in_shoot_area():
            #print(f"Forward {self.number} attempting to score")
            return {
                'type': 'kick',
                'player_number': self.number,
                'direction': direction,
                'power': 60,  # Power might be adjusted based on distance to goal
            }
        else:
            return self.move_towards_goal(ball)
    
    def in_shoot_area(self):
        if (self.color == 'red' and self.x > 300) or (self.color == 'blue' and self.x < -300):
            return True  #需要定义射门区域
        return False

    def calculate_strategic_position(self, ball, players,opponent_players):
        if not self.own_half(ball):
            # Scenario 1: Ball on our attacking half
            if ball['owner_color'] != self.color and not self.is_closest_to_ball(players, ball):
                # Move to a position that covers the farthest goal from the ball
                return self.calculate_offensive_strategic_position(ball, players,opponent_players)
            elif ball['owner_color'] == self.color and ball['owner_number'] != self.number:
                # Scenario when we own the ball or are closest to it
                return self.calculate_offensive_strategic_position(ball, players,opponent_players)
        elif self.owns_ball(ball):
            return self.calculate_offensive_strategic_position(ball,players,opponent_players)
        else:
            return self.calculate_defensive_strategic_position(ball,players,opponent_players)

    def default_strategic_position(self,ball):
        # Return a default strategic position based on the side of the field
        return {'x': (self.x + ball['x'])/2, 'y': (self.y + ball['y'])/2}  # Example value

    def calculate_defensive_strategic_position(self, ball, players,opponent_players):
        # Calculate defensive position based on ball and goal locations
        # Implement logic from documentation
        #return self.cal_sparse_area(ball,opponent_players)  # Placeholder logic
        return self.calculate_a_star_defensive_position(ball,players,opponent_players)

    def calculate_offensive_strategic_position(self, ball, players,opponent_players):
        # Calculate offensive position when in possession but not holding the ball
        # Implement logic from documentation
        #return self.cal_sparse_area(ball,players)  # Placeholder logic  
        return self.calculate_a_star_offensive_position(ball,players,opponent_players)
    def in_strategic_position(self,ball,players,opponent_players):
        # Check if the defender is in a strategic position
        strategic_pos = self.calculate_strategic_position(ball,players,opponent_players)
        if not strategic_pos:
            return True
        strategic_x = strategic_pos['x']
        strategic_y = strategic_pos['y']
        strategic_x_min, strategic_x_max = strategic_x - 10, strategic_x + 10
        strategic_y_min, strategic_y_max = strategic_y - 10, strategic_y + 10  
        return strategic_x_min <= self.x <= strategic_x_max and strategic_y_min <= self.y <= strategic_y_max


    def get_triangles(self,points):
        triangles = []
        for combo in combinations(points, 3):
            triangles.append(np.array(combo))
        return triangles

    def is_point_in_triangle(self,point, triangle):
        A, B, C = triangle
        return (np.cross(B - A, point - A) > 0) & (np.cross(C - B, point - B) > 0) & (np.cross(A - C, point - C) > 0)

    def cal_sparse_area(self,ball,players):
        all_players = players
        points = np.array([(player['x'], player['y']) for player in all_players])
        triangles = self.get_triangles(points)
        centers = []
        # 计算历史空旷点的平均值作为参考点
        if hasattr(self, 'historic_centers') and self.historic_centers:
            # 提取字典中的 x 和 y 值，并存储在数组中
            points = np.array([[point['x'], point['y']] for point in self.historic_centers[0]])

            # 计算数组的平均值
            reference_point = np.mean(points, axis=0)
        else:
            reference_point = np.array([0, 0])  # 默认参考点

        for triangle in triangles:
            triangle_center = np.mean(triangle, axis=0)
            # 如果新计算的空旷点与历史空旷点的距离小于阈值，则将其添加到有效空旷点列表中
            if np.linalg.norm(triangle_center - reference_point) < 50:
                if all(not self.is_point_in_triangle((player['x'], player['y']), triangle) for player in all_players):
                    centers.append({'x': triangle_center[0], 'y': triangle_center[1]})
        # 如果空旷区域列表为空，则返回默认位置或者不执行任何操作
        if not centers:
            return self.default_strategic_position(ball)

        # 更新历史空旷点数据
        if hasattr(self, 'historic_centers'):
            self.historic_centers.append(centers)
            if len(self.historic_centers) > 10:
                self.historic_centers.pop(0)
        else:
            self.historic_centers = [centers]
        
        if centers:
            choice = random.choice(centers)
        return choice


    def is_closest_to_ball(self, players, ball):
        """Check if this player is the closest to the ball among all forwards."""
        own_distance = get_distance({'x': self.x, 'y': self.y}, {'x': ball['x'], 'y': ball['y']})
        forwards = [player for player in players if player['role'] == 'forwards']
        for player in forwards:
            if player['number'] != self.number:
                if get_distance({'x': player['x'], 'y': player['y']}, {'x': ball['x'], 'y': ball['y']}) < own_distance:
                    return False
        return True

    def owns_ball(self, ball):
        return ball['owner_number'] == self.number and ball['owner_color'] == self.color
    
    def opponent_in_randius(self,opponent_players):
        for player in opponent_players:
            if get_distance(player,{'x':self.x,'y':self.y}) <= 100 and player['role'] != 'goalkeeper':
                return player['number']
        return None
    
    def random_kick_out(self,opponent_players):
        print(f"{self.color}Forward {self.number}检测到拦截风险大，随机踢出")
        angle = how_to_grab({'x': self.x, 'y': self.y},opponent_players)
        return{      
            'type': 'kick',
            'player_number': self.number,
            'direction': angle,
            'power': 60,  
        }

    
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
                'power': 60  # Adjust power as necessary
            }
        else:
            return None
        
    def find_best_receiver(self,players, opponent_players):
        best_receiver = None
        min_opponent_distance = 50
        min_goal_distance = 100
        min_pass_distance = 200

        for player in players:
            if player['role'] != 'goalkeeper':
                
                opponent_distance= min([get_distance(player, opponent) for opponent in opponent_players])
                #print(opponent_distance,"distance")
                goal_distance = get_distance(player, {'x': 450 if self.color == 'red' else -450, 'y': 0})
                team_distance = get_distance(player,{'x':self.x,'y':self.y})
                if opponent_distance > min_opponent_distance or (opponent_distance == min_opponent_distance and goal_distance < min_goal_distance and team_distance > min_pass_distance):
                    best_receiver = player
                    min_opponent_distance = opponent_distance
                    min_goal_distance = goal_distance
        
        if best_receiver is not None and best_receiver['number'] != self.number:
            direction_to_receiver = get_direction({'x': self.x, 'y': self.y}, {'x': best_receiver['x'], 'y': best_receiver['y']})
            print(f"Forward {self.color}{self.number}有适合传球的队员，传球")
            return {
                'type': 'kick',
                'player_number': self.number,
                'direction': direction_to_receiver,
                'power': 60  # Adjust power as necessary
            }
        else:
            return None

    
    def move_towards_goal(self, ball):
        if self.color == 'red':
            goal_position = {'x': 350, 'y': 0}
        else:
            goal_position = {'x': -350, 'y': 0}
        direction_to_goal = get_direction({'x': self.x, 'y': self.y}, goal_position)
        print(f"{self.color}Forward {self.number}尝试接近射门区域")
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
        #print(f"{self.color}Forward {self.number}跑向战略点",strategic_pos)
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
        forwards = [player for player in players if player['role'] == 'forward']
        for player in forwards:
            if player['number'] != self.number:
                if get_distance({'x': player['x'], 'y': player['y']}, {'x': ball['x'], 'y': ball['y']}) < own_distance:
                    return False
        return True
    
    def intercept_ball(self, ball,players,opponent_players):
        """Move towards the ball to intercept it."""
        direction_to_ball = get_direction({'x': self.x, 'y': self.y}, {'x': ball['x'], 'y': ball['y']})
        distance_to_ball = get_distance({'x': self.x, 'y': self.y}, {'x': ball['x'], 'y': ball['y']})
        if distance_to_ball > 18:

            return {
                'type': 'move',
                'player_number': self.number,
                'destination': ball,
                'direction': direction_to_ball,
                'speed': 10,  # This speed can be adjusted based on gameplay needs
                'has_ball':False
            }
        else:
            print(f"Forward {self.color} {self.number} try to grab")
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
    



    def calculate_a_star_defensive_position(self, ball, players, opponent_players):
        # Implement A* algorithm for defensive position calculation
        #self.update_cost_map(players,opponent_players)
        start_node = (self.x,self.y)
        goal_node = (ball['x'], ball['y'])
        visited = set()
        if len(self.cost_map) > 0 and len(self.cost_map[0]) > 0:
            open_set = []
            heapq.heappush(open_set, (0, start_node))

        while open_set:
            _, current = heapq.heappop(open_set)
            #print("Current node:", current)  # 打印当前节点
            if current in visited:
                continue
            visited.add(current)
            tolerance = 5  # 容忍范围
            if abs(current[0] - goal_node[0]) <= tolerance and abs(current[1] - goal_node[1]) <= tolerance:
                # 到达目标节点
                print(f"Forward {self.color} {self.number} reached",current[0],current[1])
                return {'x': current[0], 'y': current[1]}  # Defensive position found

            for neighbor in self.get_neighbors(current):
                if 0 <= abs(neighbor[0] // 50) < len(self.cost_map[0]) and 0 <= abs(neighbor[1] // 50) < len(self.cost_map):
                    new_cost = self.cost_map[int(abs(neighbor[1] // 50))][int(abs(neighbor[0] // 50))]
                    heapq.heappush(open_set, (new_cost, neighbor))
        # Defensive position not found, return default position
        #print("Defensive position not found, returning default position")
        return self.default_strategic_position(ball)


    def calculate_a_star_offensive_position(self, ball, players,opponent_players):
        # Implement A* algorithm for offensive position calculation
        #self.update_cost_map(players,opponent_players)
        defenders = [player for player in opponent_players if player['role'] == 'goalkeeper']
        if self.owns_ball(ball):
            goal_node = (-400 if self.color == 'red' else 400, 0)
        elif ball['owner_color'] == self.color:
            defenders_x = [player['x'] for player in defenders]
            defenders_y = [player['y'] for player in defenders]

            midpoint_x = sum(defenders_x) / len(defenders_x)
            midpoint_y = sum(defenders_y) / len(defenders_y)

            midpoint = (midpoint_x, midpoint_y)
           
            goal_node = midpoint
        else:
            goal_node = (ball['x'], ball['y'])
        
        start_node = (self.x, self.y)
        visited = set()
        if self.cost_map and len(self.cost_map) > 0 and len(self.cost_map[0]) > 0:
            open_set = []
            heapq.heappush(open_set, (0, start_node))

        while open_set:
            _, current = heapq.heappop(open_set)
            if current in visited:
                continue
            visited.add(current)
            tolerance = 20  # 容忍范围
            if abs(current[0] - goal_node[0]) <= tolerance and abs(current[1] - goal_node[1]) <= tolerance:
                # 到达目标节点
                print(f"Forward {self.color} {self.number} reached",current[0],current[1])
                return {'x': current[0], 'y': current[1]}  # Offensive position found

            for neighbor in self.get_neighbors(current):
                if 0 <= abs(neighbor[0] // 50) < len(self.cost_map[0]) and 0 <= abs(neighbor[1] // 50) < len(self.cost_map):
                    new_cost = self.cost_map[int(abs(neighbor[1] // 50))][int(abs(neighbor[0] // 50))]
                    heapq.heappush(open_set, (new_cost, neighbor))

        # Offensive position not found, return default position
        return self.default_strategic_position(ball)
    
    def get_neighbors(self, node):
        x, y = node
        neighbors = []

        # 添加当前节点周围的四个相邻节点，同时检查边界
        if (x + 10) // 50 * 50 <= 450:
            neighbors.append(((x + 10) // 50 * 50, y))  # 右边节点
        if (x - 10) // 50 * 50 >= -450:
            neighbors.append(((x - 10) // 50 * 50, y))  # 左边节点
        if (y + 10) // 50 * 50 <= 450:
            neighbors.append((x, (y + 10) // 50 * 50))  # 下方节点
        if (y - 10) // 50 * 50 >= -450:
            neighbors.append((x, (y - 10) // 50 * 50))  # 上方节点

        return neighbors


    def update_cost_map(self,ball,player_positions, opponent_positions):
        grid_size = 50
        grid_cols = len(self.cost_map[0])
        grid_rows = len(self.cost_map)

        for row in range(grid_rows):
            for col in range(grid_cols):
                row_start, row_end = row - 2, row + 2  # 子矩阵的行索引范围
                col_start, col_end = col - 2, col + 2  # 子矩阵的列索引范围

                # 确保行索引范围有效
                if row_start < 0:
                    row_start = 0
                if row_end > len(self.cost_map):
                    row_end = len(self.cost_map)

                # 确保列索引范围有效
                if col_start < 0:
                    col_start = 0
                if col_end > len(self.cost_map[0]):
                    col_end = len(self.cost_map[0])

                # 计算网格单元格左上角的坐标
                grid_top_left_x = col * grid_size - 450
                grid_top_left_y = 300 - row * grid_size

                # 计算网格单元格右下角的坐标
                grid_bottom_right_x = (col + 1) * grid_size - 450
                grid_bottom_right_y = 300 - (row + 1) * grid_size

                # 检查每个球员的位置是否在当前网格单元格内
                for player_pos in player_positions:
                    if (grid_top_left_x <= player_pos['x'] < grid_bottom_right_x and
                        grid_bottom_right_y <= player_pos['y'] < grid_top_left_y):

                        # 如果球员在网格单元格内，则减少代价
                        if player_pos['number'] == self.number:
                            self.cost_map[row][col] +=  0
                        elif player_pos['number'] == ball['owner_number'] and self.color == ball['owner_color']:
                            #self.cost_map[row][col] +=  200
                            for i in range(row_start, row_end):
                                for j in range(col_start, col_end):
                                    self.cost_map[i][j] += 150
                        else:
                            self.cost_map[row][col] -=  50

                # 检查每个对手的位置是否在当前网格单元格内
                for opponent_pos in opponent_positions:
                    if (grid_top_left_x <= opponent_pos['x'] < grid_bottom_right_x and
                        grid_bottom_right_y <= opponent_pos['y'] < grid_top_left_y):
                        # 如果对手在网格单元格内，则增加代价
                            for i in range(row_start, row_end):
                                for j in range(col_start, col_end):
                                    self.cost_map[i][j] += 100
        #print(self.cost_map)