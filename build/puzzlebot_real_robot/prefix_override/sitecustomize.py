import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/itzelh/puzzlebot_JuanMa_ws/install/puzzlebot_real_robot'
