import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, ExecuteProcess, IncludeLaunchDescription
from launch.substitutions import Command, LaunchConfiguration
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
from ament_index_python.packages import get_package_prefix


def generate_launch_description():
    
    pkg_barista_bot_gazebo = get_package_share_directory('barista_robot_description')
    description_package_name = "barista_robot_description"
    install_dir = get_package_prefix(description_package_name)
   
    # This is to find the models inside the models folder in barista_robot_description package
    gazebo_models_path = os.path.join(pkg_barista_bot_gazebo, 'models')
    if 'GAZEBO_MODEL_PATH' in os.environ:
        os.environ['GAZEBO_MODEL_PATH'] = os.environ['GAZEBO_MODEL_PATH'] + \
            ':' + install_dir + '/share' + ':' + gazebo_models_path
    else:
        os.environ['GAZEBO_MODEL_PATH'] = install_dir + \
            "/share" + ':' + gazebo_models_path


    if 'GAZEBO_PLUGIN_PATH' in os.environ:
        os.environ['GAZEBO_PLUGIN_PATH'] = os.environ['GAZEBO_PLUGIN_PATH'] + \
            ':' + install_dir + '/lib'
    else:
        os.environ['GAZEBO_PLUGIN_PATH'] = install_dir + '/lib'


    print("GAZEBO MODELS PATH=="+str(os.environ["GAZEBO_MODEL_PATH"]))
    print("GAZEBO PLUGINS PATH=="+str(os.environ["GAZEBO_PLUGIN_PATH"]))


    use_sim_time = LaunchConfiguration('use_sim_time', default='true')
    # Declare a new launch argument for the world file
    world_file_arg = DeclareLaunchArgument(
        'world',
        default_value=[get_package_share_directory(
            'barista_robot_description'), '/worlds/barista_robot_empty.world'],
        description='Path to the Gazebo world file'
    )


    # Define the launch arguments for the Gazebo launch file
    gazebo_launch_args = {
        'verbose': 'false',
        'pause': 'false',
        'world': LaunchConfiguration('world')
    }


   # Include the Gazebo launch file with the modified launch arguments
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory('gazebo_ros'), 'launch'), '/gazebo.launch.py']),
        launch_arguments=gazebo_launch_args.items(),
    )


    # Define the robot model files to be used
    # robot_desc_file = "box_bot_final.urdf"
    robot_desc_file = "barista_robot_model.urdf.xacro"


    robot_desc_path = os.path.join(get_package_share_directory(
        "barista_robot_description"), "xacro", robot_desc_file)


    robot_name_1 = "rick"
    robot_name_2 = "morty"

    robot_color_1 = "Gazebo/Blue"
    robot_color_2 = "Gazebo/Red"


    rsp_robot1 = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        namespace=robot_name_1,
        parameters=[{'frame_prefix': robot_name_1+'/', 'use_sim_time': use_sim_time,
                     'robot_description': Command(['xacro ', robot_desc_path, ' robot_name:=', robot_name_1, ' robot_gazebo_material:=', robot_color_1])}],
        output="screen")


    rsp_robot2 = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        namespace=robot_name_2,
        parameters=[{'frame_prefix': robot_name_2+'/', 'use_sim_time': use_sim_time,
                     'robot_description': Command(['xacro ', robot_desc_path, ' robot_name:=', robot_name_2, ' robot_gazebo_material:=', robot_color_2])}],
        output="screen"
    )


    spawn_robot1 = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=['-entity', 'robot1', '-x', '0.0', '-y', '0.0', '-z', '0.0',
                   '-topic', robot_name_1+'/robot_description']
    )


    spawn_robot2 = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=['-entity', 'robot2', '-x', '1.0', '-y', '1.0', '-z', '0.0',
                   '-topic', robot_name_2+'/robot_description']
    )


    # RVIZ Configuration
    rviz_config_dir = os.path.join(get_package_share_directory(description_package_name), 'rviz', 'double_robot.rviz')

    rviz_node = Node(
            package='rviz2',
            executable='rviz2',
            output='screen',
            name='rviz_node',
            parameters=[{'use_sim_time': True}],
            arguments=['-d', rviz_config_dir])


    return LaunchDescription([
        world_file_arg,
        gazebo,
        rsp_robot1,
        rsp_robot2,
        spawn_robot1,
        spawn_robot2,
        rviz_node ])
