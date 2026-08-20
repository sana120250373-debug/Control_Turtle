import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def generate_launch_description():

    vel_topic_arg = DeclareLaunchArgument(
        'vel_topic',
        default_value='/turtle1/cmd_vel',
        description='vel topic'
    )

    stamped_vel_arg = DeclareLaunchArgument(
        'stamped_vel',
        default_value='false',
        description='set to true for twiststamped vel'
    )

    sub_topic_arg = DeclareLaunchArgument(
        'sub_topic',
        default_value='/turtle1/color_sensor',
        description='Topic to subscribe for turtle color sensor'
    )
    
    pub_topic_arg = DeclareLaunchArgument(
        'pub_topic',
        default_value='/dominant_color',
        description='Topic to publish the dominant color'
    )

    frame_id_arg = DeclareLaunchArgument(
        'frame_id',
        default_value='turtle1_frame',
        description='Frame ID for logger/messages'
    )

    turtlesim_node = Node(
        package='turtlesim',##pkg name 
        executable='turtlesim_node', #executable name in setup.py
        name='turtlesim'
    )

    Movment_node = Node(
        package='control_turtle',
        executable='Movment_node',
        name='Movment_node',
        output='screen',
        prefix='xterm -e',
        parameters=[{
            'vel_topic ': LaunchConfiguration('vel_topic'),
            'stamped_vel':LaunchConfiguration('stamped_vel')

        }]
    )
    perception_node = Node(
        package='control_turtle',      ##pkg name 
        executable='perception_node',   #executable name in setup.py
        name='perception_node',
        parameters=[{
            'sub_topic': LaunchConfiguration('sub_topic'),
            'pub_topic': LaunchConfiguration('pub_topic'),
            'frame_id': LaunchConfiguration('frame_id')
        }]
    )

    return LaunchDescription([
        vel_topic_arg,
        stamped_vel_arg,
        sub_topic_arg,
        pub_topic_arg,
        frame_id_arg,
        turtlesim_node,
        perception_node,
        Movment_node
    ])