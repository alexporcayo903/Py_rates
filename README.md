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

1. Follw the instruction in the wiki to get started coding with ros: http://wiki.ros.org/ROS/Tutorials/InstallingandConfiguringROSEnvironment. This also shows how to create a catkin workspace.

2. After creating the catkin workspace, please download the " app_prog_project " folder from our github. This folder contains all the nodes that we created to run our simulation. Please run the command below to create the packadge. 


3. Go to your catinkin work space source folder and create a packadge 


```bash
cd ~/catkin_ws/src
catkin_create_pkg my_pkg rospy std_msgs
cd ..
catkin_make
```

4. From the downloaded " app_prog_project" folder copy  the contentes listed below and put it inside the my_pkg folder
      maze1.txt
      maze2.txt
      maze_fixed.py
      turtlesim_maze_node.py
      ourgazebonode.py
      


5. Run the following command in the bash terminal to run the code 

first open new  tab of the terminal, run the roscore


```bash
roscore
```

second tab : open the new tab in the terminal, run turtlesim node

```bash
rosrun turtlesim turtlesim_node
```

third tab:  open the new tab in the terminal, run turtlesim maze node


```bash
rosrun my_pkg turtlesim_maze_node.py
```

There are two seed file maze1.txt and maze2.txt in the folder " app_prog_prohject ". To run 
different maze go inside turtlesim_maze_node.py and edit line 


  
### How to save and run source folder in ros:
1)

2)

3)
### How to seed the maze:
1) make a text file with 

2) open that text file 

3) change lines of code

### How to use gazebo and turtlebot3:
1)

2)

3)
### How to use maze to gazebo:
1)

2)

3)

## Notes

All of the mazes in the files above are seeded except for "Graphing Points". These files will work with or without a seed, we used a seed so the files will line up with the examples. If you would like to unseed the mazes just follow the instructions above. The seeded and unseeded versions of the code are found the in the maze generator folder. If you have trouble installing pygame on linux this code can still function by giving the function points as shown in "Turtlesim Without Pygame".

