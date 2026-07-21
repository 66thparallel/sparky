# ROS 2 Build System

## Package Metadata

Every package needs `package.xml` to declare its name, version, license, maintainers, and dependencies. Declare dependencies accurately: build dependencies are needed to compile or generate interfaces, while execution dependencies are needed at runtime.

## Python Packages

Sparky's nodes are Python packages built through `ament_python`. Keep package metadata in `package.xml`, installation and entry points in `setup.py` or `setup.cfg`, and package resources in the standard `resource/` directory.

Use console-script entry points so ROS can invoke nodes by executable name:

```python
entry_points={'console_scripts': ['controller_node = controller.node:main']}
```

## CMake Packages

Use `ament_cmake` for C++, interface generation, and packages that install CMake targets. Export include directories and dependency information when other packages consume your library.

## Colcon Workflow

Build from the workspace root with `colcon build --symlink-install`, then source `install/setup.bash` in each shell. Build a single package with `--packages-select <package>`. Clean stale artifacts only when necessary because deleting `build/`, `install/`, and `log/` removes useful diagnostics.
