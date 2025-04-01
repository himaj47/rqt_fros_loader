from setuptools import find_packages, setup

package_name = 'rqt_fros_loader'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name, ['plugin.xml']),
        ('share/' + package_name + '/resource', ['resource/fros_loader_widget.ui']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='himaj',
    maintainer_email='himajjoshi932@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'rqt_fros_loader = ' + package_name + '.main:main',
        ],
    },
)
