import rclpy
from rclpy.node import Node 
from geometry_msgs.msg import Twist ,TwistStamped
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
        super().__init__('Movment_node')
        self.declare_parameter('vel_topic','/turtle1/cmd_vel') # topic and its value
        self.declare_parameter('stamped_vel',False) #no time info by defualt

        topic_name= self.get_parameter('vel_topic').value #take the value from prameter and store it 
        
        self.stamped=bool(self.get_parameter('stamped_vel').value) #check bool value and store it
        self.get_logger().info(f"stamped is{self.stamped}")

        self.linear_vel= 2.0 
        self.angular_vel=2.0 

        if self.stamped:
            self.pub=self.create_publisher(TwistStamped,topic_name,10)# PUBLISH WITJ TIME AND ID FRAME
            self.get_logger().info("TwistStamped pub...")

        else:
            self.pub=self.create_publisher(Twist,topic_name,10) # without tim and id info
            self.get_logger().info("Twist pub...")


    def pub_vel(self,linear,angular):
        if self.stamped:
            msg=TwistStamped()
            msg.header.stamp=self.get_clock().now().to_msg() #get the current time
            msg.header.frame_id='turtle' # to refer angle and vel to turtle
            msg.twist.linear.x=float(linear) ##store vel in twist object and made it float
            msg.twist.angular.z=float(angular)
        else:
            msg=Twist()
            msg.linear.x=float(linear)
            msg.angular.z=float(angular)
        self.pub.publish(msg)

        self.get_logger().info("use W, A, S, D to control the turtle")


    def run_loop(self):

        while rclpy.ok():
            key= read_key().lower()
            twist=Twist()
            if key =='w': ## forward
               self.pub_vel(self.linear_vel, 0.0)
            elif key == 's': ##backward
                self.pub_vel(-self.linear_vel, 0.0)
            elif key=='a': ## turn left
                self.pub_vel(0.0 , self.angular_vel)
            elif key == 'd' : ## turn right
               self.pub_vel(0.0 , - self.angular_vel)
            elif key == ' ':
                self.pub_vel(0.0, 0.0)
            elif key == 'q':
                break
        


def main():
    rclpy.init() # start ros communication 
    node=MovmentNode()
    try:
        node.run_loop()
    except KeyboardInterrupt:
        pass
    finally:
       stop_twist= Twist()
       node.pub.publish(stop_twist)
       node.destroy_node()
       rclpy.shutdown()

if __name__ == '__main__':
    main()

