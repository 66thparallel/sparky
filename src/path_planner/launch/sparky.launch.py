from pathlib import Path

from ament_index_python.packages import get_package_share_directory
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    path_planner_dir = Path(get_package_share_directory('path_planner'))
    vehicle_description_dir = Path(get_package_share_directory('vehicle_description'))
    default_route_config = path_planner_dir / 'config' / 'default_route.yaml'
    urdf_path = vehicle_description_dir / 'urdf' / 'vehicle.urdf'
    robot_description = urdf_path.read_text()
    route_config = LaunchConfiguration('route_config')

    return LaunchDescription([
        DeclareLaunchArgument(
            'route_config',
            default_value=str(default_route_config),
            description='Path planner parameter file containing frame_id and waypoints.',
        ),
        Node(
            package='vehicle_sim',
            executable='vehicle_sim_node',
            output='screen',
        ),
        Node(
            package='controller',
            executable='controller_node',
            output='screen',
        ),
        Node(
            package='path_planner',
            executable='path_planner_node',
            parameters=[route_config],
            output='screen',
        ),
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            parameters=[{'robot_description': robot_description}],
            output='screen',
        ),
    ])