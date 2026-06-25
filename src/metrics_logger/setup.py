from setuptools import setup


package_name = 'metrics_logger'


setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='janeikeliu',
    maintainer_email='janeikeliu@gmail.com',
    description='CSV metrics logger for the Sparky simulation stack.',
    license='MIT',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'metrics_logger_node = metrics_logger.metrics_logger_node:main',
        ],
    },
)