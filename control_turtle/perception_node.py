import rclpy
from rclpy.node import Node
from turtlesim.msg import Color
from std_msgs.msg import String



class PerceptionNode(Node):
    def __init__(self):
        super().__init__('perception_node')

        self.declare_parameter ('sub_topic','/turtle1/color_sensor') #init topic parameter and store its default value
        self.declare_parameter ('pub_topic','/dominant_color')
        self.declare_parameter ('frame_id','turtle')
        
        sub_topic_val = self.get_parameter('sub_topic').value ## get topic store value
        pub_topic_val = self.get_parameter('pub_topic').value
        self.frame_id = self.get_parameter('frame_id').value

        

        self.color_sub = self.create_subscription( ##create subscriber to know color
            Color,
            sub_topic_val,
            self.color_callback,
            10
        )
        
        self.dominant_color_pub = self.create_publisher(  ##publish el dominant color
            String,
            pub_topic_val,
            10
        )
        
        self.get_logger().info(f"Started Listening to {sub_topic_val}...")

    def color_callback(self, msg: Color):
    
        r = msg.r
        b = msg.b
        g = msg.g
        
        if r >= g and r >= b:
            major_color = "Red"

        elif g >= r and g >= b:
            major_color = "Green"

        else:
            major_color = "Blue"

        current_time = self.get_clock().now().to_msg() ## get time and convert it to msg

        self.get_logger().info(f" Frame_id :{self.frame_id}, Time :{current_time.sec},Dominant Color: {major_color} (R: {r}, G: {g}, B: {b})")

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