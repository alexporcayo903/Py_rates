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

### How to set up a ros packadge and run our node (After Installation): 

1. Follw the instruction in the wiki to get started coding with ros: http://wiki.ros.org/ROS/Tutorials/InstallingandConfiguringROSEnvironment. This also shows how to create a catkin workspace.

2. After creating the catkin workspace, please download the " app_prog_project " folder from our github. This folder contains all the nodes that we created to run our simulation. Please run the command below to create the packadge. 


3. Go to your catinkin work space source folder and create a packadge 


```bash
cd ~/catkin_ws/src
catkin_create_pkg my_pkg rospy std_msgs
cd ..
catkin_make
```

4. From the downloaded " app_prog_project" folder copy  the contents listed below and put it inside the my_pkg folder


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
cd ~/catkin_ws/src/my_pkg/
rosrun my_pkg turtlesim_maze_node.py
```

There are two seed file maze1.txt and maze2.txt in the folder " app_prog_project ". To run 
different maze go inside turtlesim_maze_node.py and edit line 248 " XX=maze_fixed.mazf('maze2.txt') "


### How to seed the maze:

1) To save a specific maze from the Maze Generator, you'll need to save the cell list into a text file. The list contains directions {right,left,up,down} to carve out the grid into a maze. 


To save the list, start with a empty list and append the directions from the `carve_out_maze`, for our code the list is in a variable called `CELL_ORDER'



```python
....
if len(cell) > 0:                                                  # check to see if cell list is empty
           
            cell_chosen = (random.choice(cell))                    # select one of the cell randomly
            CELL_ORDER.append(cell_chosen)
....
```
Then the list is saved into text file

```python
with open('maze_saved.txt', 'w+') as f: 
    for items in CELL_ORDER:

        f.write('%s\n' %items)   
```
2) To use the saved maze, you'll need to do the following:
Import the file
```python
with open('maze3.txt') as f: # import a maze, list of direction of have pygame shape out the maze 
    CELL = f.read().splitlines()

```
Set `cell_chosen` equal to `CELL[n]` in the `carve_out_maze` function  

```python
n=0
if len(cell) > 0:                                          # check to see if cell list is empty
           
            #cell_chosen = (random.choice(cell))           # comment out or delete
            
            cell_chosen = CELL[n]                          # select seeded cell
          
            n=n+1                 
            #CELL_ORDER.append(cell_chosen)                 # comment out or delete, not saving directions of seeded maze
```

Then from there you should see the seeded maze.

### How to run turtle race:
1) To run two turtles at the same time open up 4 terminal windows. In the two teminals which will run the turtles change the current directory to the source file directory by:

```bash
cd catkin_ws/src/
```
2) Then start the roscore by:

```bash
roscore
```

3) In the next terminal start the turtlesim node by:

```bash
rosrun turtlesim turtlesim_node
```

4) In the first terminal you changed the directory in start the first turtle by:

```bash
rosrun my_package_name my_node.py turtle1
```

5) In the last terminal start the second turtle by:

```bash
rosrun my_package_name my_node.py turtle2
```

After you start the second turtle there will be a two second delay from rospy.sleep(2) and then the two turtles start simultaneously. Be careful to note the names of the turtles. These names need to be exatly set to run the two turtles at the same time (currently 'turtle1' and 'turtle2'). If you would like to change the turtle names you can go to everywhere that each turtle is named and change it to the desired name in those case statments. The names of your package and node can be whatever you choose. This works by using a roswait command and waiting for the final turtle to be created. The command expects the exact name of the final turtle specified in the code to be inputed as the turtle name(in this case 'turtle2'). This code is designed to run 2-3 turtles at once using given points from the maze generator. These points are hard set in the file due to ros1 timming constraints and our limitations using a virtual machine. 

### How to use map to gazebo:

### Installation ( This was copied from the github link: https://github.com/Adlink-ROS/map2gazebo)

NOTE:

trimesh needs the following soft dependencies to export Collada (.dae) files.

Theoretically you can install these with `pip install trimesh[soft]` but this
failed for me, so I installed the needed ones myself.

1. Install the python dependencies with pip:

```bash
pip3 install --user trimesh
pip3 install --user numpy
pip3 install --user pycollada
pip3 install --user scipy
pip3 install --user networkx
pip3 install --user opencv-contrib-python 

```

2. Git clone map2gazebo and build package

```bash
mkdir -p ~/map2gz_ros2_ws/src
cd ~/map2gz_ros2_ws/src
git clone https://github.com/Adlink-ROS/map2gazebo.git -b foxy-devel
```

### Offline conversion

* Create your map 

```bash
cd ~/map2gz_ros2_ws
```
after that download our maze2.png and maze2.yaml from our github folder app_prog_project and put it in the folder map2gz_ros2_ws


* Convert the map to STL model
  - Note the output directory: Gazebo world will use the model here

```bash
python3 src/map2gazebo/map2gazebo/map2gazebo_offline.py --map_dir maze2.png --export_dir src/map2gazebo/models/map/meshes
```

if this does not work then you may have to go inside map2gazebo_offline.py file and replace all pgm to png

* Modify the model file: `src/map2gazebo/models/map/model.sdf`
  - Replace `map.stl` to `maze2.stl` (or your stl name)

* Run Gazebo

```bash
export GAZEBO_MODEL_PATH=$HOME/map2gz_ros2_ws/src/map2gazebo/models/
gazebo src/map2gazebo/worlds/map.sdf
```


### How to use gazebo and turtlebot3:
1) follow this link to install turtlebot3 gazebo simulation packadge

https://emanual.robotis.com/docs/en/platform/turtlebot3/simulation/

2) Enter the following command in the bash terminal to run the gazebo

```bash
export TURTLEBOT3_MODEL=burger
roslaunch turtlebot3_gazebo turtlebot3_empty_world.launch 
```

3) ope a new tab from the terminal 

```bash
cd ~/catkin_ws/src/my_pkg/
rosrun my_pkg ourgazebonode.py
```



## Notes

All of the mazes in the files above are seeded except for "Graphing Points". These files will work with or without a seed, we used a seed so the files will line up with the examples. If you would like to unseed the mazes just follow the instructions above. The seeded and unseeded versions of the code are found the in the maze generator folder. If you have trouble installing pygame on linux this code can still function by giving the function points as shown in "Turtlesim Without Pygame".

