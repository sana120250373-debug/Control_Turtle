import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/sana/colcon1_ws/src/control_turtle/install/control_turtle'
