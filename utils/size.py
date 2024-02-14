def make_even_number(n):
    if n % 2 == 0:
        return n
    else:
        return n+1


main_size = 10
# # 既然它一直搞偶数，那我也这么搞，所有数据都按偶数来
# # 这里按厘米级别，完整场地长1100 cm，宽800 cm

# Physical entity data
FOOTBALL_SITE_LENGTH =  1100
FOOTBALL_SITE_WIDTH =  800
# 比赛区域是900cm长，600cm宽
FOOTBALL_PITCH_LENGTH =  900
FOOTBALL_PITCH_WIDTH =  600
PLAYER_RADIUS = 16 #574x 311x 275 mm 应该是高，左右，前后，取300mm,即30cm,半径取16
PLAYER_NUMBER_FONT_SIZE = 20 #几号
PLAYER_NAME_FONT_SIZE =  16 #字体几号
BALL_RADIUS = 8#球直径14.3，取半径为8

# Football pitch
GOAL_DEPTH = 60 # 0.6m in cm
GOAL_WIDTH = 260 # 2.6m in cm
GOAL_HEIGHT = 120 # 1.2m in cm
GOAL_AREA_LENGTH = 100 # 1m in cm
GOAL_AREA_WIDTH = 300 # 3m in cm
PENALTY_MARK_DISTANCE = 150 # 1.5m in cm
CENTER_CIRCLE_RADIUS = 76 # 1.5m in cm 除2再取偶数
BORDER_STRIP_WIDTH = 100 # 1m in cm
PENALTY_AREA_LENGTH = 200 # 2m in cm
PENALTY_AREA_WIDTH = 500 # 5m in cm

CENTER_POINT_RADIUS = 6
LINE_THICKNESS = 4


VERTICAL_MARGIN = make_even_number(int((PLAYER_RADIUS + BALL_RADIUS) * 2.5)) # 46
HORIZONTAL_MARGIN = make_even_number(int((PLAYER_RADIUS + BALL_RADIUS) * 2.5)) # 46
#
SCREEN_LENGTH = 1100 #这个是用来画图的，根据这个多长把自己画在某处
SCREEN_WIDTH = 742

GOALKEEPER_WIDTRH = make_even_number(main_size * 16) #160
GOALKEEPER_DEPTH = make_even_number(main_size * 21) #210


# SCOREBOARD
SCOREBOARD_FONT_SIZE = make_even_number(main_size * 3) # 40
