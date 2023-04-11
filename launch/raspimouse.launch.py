import launch
import launch.actions
import launch.substitutions
import launch_ros.actions

def generate_launch_description():
    rtbuzzer = launch_ros.actions.Node(
        package='raspimouse_tiny',
        executable='buzzer',
        )
    rtlightsensors = launch_ros.actions.Node(
        package='raspimouse_tiny',
        executable='lightsensors',
        output='screen',
        )

    return launch.LaunchDescription([rtbuzzer, rtlightsensors])
