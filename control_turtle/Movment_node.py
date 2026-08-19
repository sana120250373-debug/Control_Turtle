import rclpy
from rclpy.node import Node 
from geometry_msgs.msg import Twist
import sys
import termios
import tty


## function to read the input from keyboad directly
def read_key():
    terminal_num = sys.stdin.fileno()  ## take the num of terminal screen 
    settings = termios.tcgetattr(terminal_num) ## store terminal settings 
    
    try:
      tty.setraw(sys.stdin.fileno()) ## convert terminal to "raw mode"
      read_key = sys.stdin.read(1)

    finally:
        termios.tcsetattr(terminal_num , termios.TCSADRAIN, settings) ## return terminal to its state  after reading key 
    
    return read_key


class MovmentNode(Node):
    def __init__(self):
        super().__init__('Movement_node')
        self.pub_vel=self.create_publisher(Twist,'/turtle1/cmd_vel',10) ## create publisher on vel topic

        self.linear_vel= 2.0 
        self.angular_vel=2.0 
        self.get_logger().info("use W, A, S, D OR arrows to control the turtle")


    def run_loop(self):

        while rclpy.ok():
            key= read_key().lower()
            twist=Twist()
            if key =='w': ## forward
                twist.linear.x=self.linear_vel
                twist.angular.z=0.0
            elif key == 's': ##backward
                twist.linear.x= -self.linear_vel
                twist.angular.z=0.0
            elif key=='a': ## turn left
                twist.linear.x= 0.0
                twist.angular.z=self.angular_vel

            elif key == 'd' : ## turn right
                twist.linear.x=0.0
                twist.angular.z = -self.angular_vel
            elif key == ' ':
                twist.linear.x=0.0
                twist.angular.z=0.0
            elif key == 'q':
                break
                
            self.pub_vel.publish(twist)


def main():
    rclpy.init() # start ros communication 
    node=MovmentNode()
    try:
        node.run_loop()
    except KeyboardInterrupt:
        pass
    finally:
       stop_twist= Twist()
       node.pub_vel.publish(stop_twist)
       node.destroy_node()
       rclpy.shutdown()

if __name__ == '__main__':
    main()

