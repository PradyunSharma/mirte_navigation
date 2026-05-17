from setuptools import setup
import os
from glob import glob

package_name = 'grp29'

setup(
    name=package_name,
    version='0.0.1',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.launch.py')),
        (os.path.join('share', package_name, 'maps'), glob('maps/*')),
        (os.path.join('share', package_name, 'config'), glob('config/*')),
        (os.path.join('share', package_name, 'laser_config'), glob('laser_config/*')),
        (os.path.join('share', package_name, 'slam_config'), glob('slam_config/*')),
    ],
    install_requires=['setuptools', 'pyyaml'],
    entry_points={
        'console_scripts': [
            'waypoint_follower = grp29.waypoint_follower:main',
        ],
    },
)