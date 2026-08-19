import rclpy
from rclpy.node import Node
from turtlesim.msg import Color
from std_msgs.msg import String



class PerceptionNode(Node):
    def __init__(self):
        super().__init__('perception_node')
        
        self.color_sub = self.create_subscription( ##create subscriber to know color
            Color,
            '/turtle1/color_sensor',
            self.color_callback,
            10
        )
        
        self.dominant_color_pub = self.create_publisher(  ##publish el dominant color
            String,
            '/dominant_color',
            10
        )
        
        self.get_logger().info("Started Listening to /turtle1/color_sensor...")

    def color_callback(self, msg: Color):
        
        r = msg.r
        g = msg.g
        b = msg.b
        
        if r >= g and r >= b:
            major_color = "Red"

        elif g >= r and g >= b:
            major_color = "Green"

        else:
            major_color = "Blue"

        self.get_logger().info(f"Dominant Color: {major_color} (R: {r}, G: {g}, B: {b})")

        color_msg = String()
        color_msg.data = major_color
        self.dominant_color_pub.publish(color_msg) 

def main():
    rclpy.init()
    node = PerceptionNode()
    
    try:
        rclpy.spin(node) ##spin on the callback
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()