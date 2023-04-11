import launch
import launch.actions
import launch.substitutions
import launch_ros.actions

def generate_launch_description():
    buzzer = launch_ros.actions.Node(
        package='raspimouse_tiny',
        executable='buzzer',
        )
    lightsensors = launch_ros.actions.Node(
        package='raspimouse_tiny',
        executable='lightsensors',
        output='screen',
        )
    switches = launch_ros.actions.Node(
        package='raspimouse_tiny',
        executable='switches',
        output='screen',
        )
    motors = launch_ros.actions.Node(
        package='raspimouse_tiny',
        executable='motors',
        output='screen',
        )

    return launch.LaunchDescription([buzzer, lightsensors, switches])
