# These commands rebuild the Sparky vehicle simulation project

rm -rf build install log
colcon build --symlink-install
source install/setup.bash