import launch
import launch.actions
import launch.substitutions
import launch_ros.actions

def generate_launch_description():
    rtbuzzer = launch_ros.actions.Node(
        package='raspimouse_tiny',
        executable='rtbuzzer',
        )
    rtlightsensors = launch_ros.actions.Node(
        package='raspimouse_tiny',
        executable='rtlightsensors',
        output='screen',
        )

    return launch.LaunchDescription([rtbuzzer, rtlightsensors])
