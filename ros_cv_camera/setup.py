from setuptools import find_packages, setup

package_name = 'ros_cv_camera'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='hem',
    maintainer_email='hem@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            "img_sub = ros_cv_camera.image_subscriber:main",
            "img_pub = ros_cv_camera.image_publisher:main"
        ],
    },
)
