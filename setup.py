from setuptools import setup
import os
from glob import glob

package_name = 'raspimouse_tiny'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name), glob('launch/*.launch.py'))
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Ryuichi Ueda',
    maintainer_email='ryuichiueda@gmail.com',
    description='ROS2 version of raspimouse_ros',
    license='BSD-3-Clause',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'buzzer = raspimouse_tiny.buzzer:main',
            'lightsensors = raspimouse_tiny.lightsensors:main',
            'switches = raspimouse_tiny.switches:main',
        ],
    },
)
