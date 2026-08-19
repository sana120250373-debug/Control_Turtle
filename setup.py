from setuptools import find_packages, setup

package_name = 'control_turtle'

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
    maintainer='sana',
    maintainer_email='sana.120250373@ejust.edu.eg',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'Movment_node = control_turtle.Movment_node:main',
            'perception_node = control_turtle.perception_node:main',

        ],
    },
)
