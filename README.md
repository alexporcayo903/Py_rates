# Maze Follower with Turtlebot and Gazebo
## Summary

To have a simulated robot to solve a maze and convert the solution into a path to follow. Using ROS to simulate path following with Turtlesim and Gazebo. Starts with the Maze Generator to create a random maze with a solution path. The solution path is saved as a set of coordinates and the Maze itself is saved as a PNG file. To minimize ROS errors and crashes, the coordinates are reformatted to run more smoothly with Gazebo and Turtlebot. The reformations does not change the shape of the path. The PNG goes through Map2Gazebo to create a world with a 3D maze. The final output of this whole intergration is a robot, we chose Burger, to follow the solution path of the maze.

## Dependences
### Ros1, Pygame, Turtlebot3, PythonMazeGenerator, Ubuntu 20.04
## Installation
### Virtualbox
One of the virtual machines we used to run Ubuntu 20.04 was virtual box. This virtual machine can be downloaded by following the instructions in https://data-flair.training/blogs/install-virtualbox/.

### Ros1

Ros1 is the main package we use in this project. By dowlading this package you can use both Turtlesim and Gazebo. The best way to install Ros1 is to follow their wiki: http://wiki.ros.org/ROS/Installation.
### Maze Generator/Pygame

Stared from the [baseline maze code]( https://github.com/tonypdavis/PythonMazeGenerator) found in Github and credited to Davis MT. With modifications to intergrate with our project, the Maze Generator will be the first Python file to be called. The needed modules are : pygame, time , and random        

### Turtlebot3



ros stuff


gazebo stuff


## How To Use

### How to set up a ros file (After Installation): 

Follw the instruction in the wiki 

(http://wiki.ros.org/ROS/Tutorials/InstallingandConfiguringROSEnvironment)

### How to seed the maze with a text file:
1)

2)

3)
### How to use gazebo and turtlebot3:
1)

2)

3)
### How to use maze to gazebo:
1)

2)

3)
## Notes

All of the mazes in the files above are seeded except for "Graphing Points". These files will work with ot without a seed, we used a seed so the files will line up with the examples. If you have trouble installing pygame on linux Pygame this code can still function by giving the function points as shown in "Turtlesim Without Pygame".

