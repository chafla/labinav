# labinav

Labyrinth navigation using ROS.
Some of the earlier work of this project can be found in `old/`, however the most up-to-date and actively developed stuff is in https://github.com/athenian-robotics/lidar_navigation.
This readme forms a general guide towards getting an environment configured to be able to start messing around with everything.

# Setting up.

## Installation on PC

Labinav is configured to run under Ubuntu 16.04, using ROS Kinetic. Other distributions may work, however ymmv.

You can install ROS with the following commands:

```sh
$ sudo apt-get update
$ sudo apt-get upgrade
$ wget https://raw.githubusercontent.com/ROBOTIS-GIT/robotis_tools/master/install_ros_kinetic.sh && chmod 755 ./install_ros_kinetic.sh && bash ./install_ros_kinetic.sh
```

This will download and run a script that will install and configure your ROS environment, even setting environment variables.


Optionally, ROS Kinetic can be installed as outlined [here](http://wiki.ros.org/kinetic/Installation/Ubuntu). Note that the Full Desktop Install is required to use Gazebo.
There are quite a few other steps (that won't be outlined in detail here) about how to configure the rest of your environment.

After ROS is installed, you need to download a bunch of dependent packages for Turtlebot3 control to work effectively.

```sh
sudo apt install ros-kinetic-joy ros-kinetic-teleop-twist-joy ros-kinetic-teleop-twist-leopard ros-kinetic-laser-proc ros-kinetic-rgbd-launch ros-kinetic-depthimage-to-laserscan ros-kinetic-rosserial-arduino ros-kinetic-rosserial-python ros-kinetic-rosserial-server ros-kinetic-rosserial-client ros-kinetic-rosserial-msgs ros-kinetic-amcl ros-kinetic-map-server ros-kinetic-move-base ros-kinetic-urdf ros-kinetic-xacro ros-kinetic-compressed-image-transport ros-kinetic-rqt-image-view ros-kinetic-gmapping ros-kinetic-navigation ros-kinetic-interactive-markers
cd ~/catkin_ws/src/
git clone https://github.com/ROBOTIS-GIT/turtlebot3_msgs.git
git clone https://github.com/ROBOTIS-GIT/turtlebot3.git
cd ~/catkin_ws && catkin_make
```

Once that is completed, clone and set up the lidar navigation repos.

```sh
cd ~/catkin_ws/src
git clone https://github.com/athenian-robotics/lidar_navigation.git
cd lidar_navigation
pip install -r requirements.txt
cd ~/catkin_ws
catkin_make
```
One last note is that the type of turtlebot being used needs to be set. Run:
```sh
echo "export TURTLEBOT3_MODEL=burger" >> ~/.bashrc
```
If you have a physical Waffle-model TB3, then replace `burger` with `waffle`. If you are just planning on using a simulated TB3, just use burger.


## Installation on Raspberry PI
Robotis has also provided a very good guide (as well as a pre-built image) for putting ROS onto a physical Turtlebot3: http://emanual.robotis.com/docs/en/platform/turtlebot3/raspberry_pi_3_setup/#install-linux-based-on-raspbian. 
This image already has ssh enabled and should be configured to be ready-to-go. Manual installation of ROS and all the dependent packages on the raspi is an exercise left to the reader.

**Make sure to also set the turtlebot model on the raspberry pi's `~/.bashrc`.**

# Experimenting

## Loading the robot into the maze

First of all, a maze must be loaded. Follow the steps [here](https://github.com/athenian-robotics/lidar_navigation/blob/master/gzmaze.md) to configure the maze plugin for gazebo.

**Note:** This is not always entirely consistent, and has been met with some issues from time to time. 
In the event that the plugin does not build and Gazebo refuses to find the mazes, a possible solution is to copy the maze files themselves to `/usr/share/gazebo-7/models/`.  
Another possible solution is to run ```sh
echo "export GAZEBO_MODEL_PATH=$HOME/catkin_ws/src/lidar_nagivation/models/:$GAZEBO_MODEL_PATH" >> ~/.bashrc
```

Once Gazebo is configured, follow the instructions [here](https://github.com/athenian-robotics/lidar_navigation#start-a-turtlebot3) to get your Turtlebot3 initialized. This creates a roscore, and so any other ROS nodes run will connect to it. After that, to start up some nodes, follow the rest of the instructions on that page.

The bare minimum that you need to run to get the robot to move (in sim) are, as outlined:

```
roslaunch turtlebot3_gazebo turtlebot3_empty_world.launch
rosrun lidar_navigation teleop_node.py
rosrun lidar_navigation geometry_node.py

# To stop it after killing geometry_node
rosrun lidar_navigation stop_node.py
```

The other parts outlined are for visual purposes to help with debugging, to help with understanding, and also for future possible pursuits.

# Bonus: SLAM

The Turtlebot3 also comes packaged with a very useful SLAM package, which allows it to map out its environment. It meshes very well with lidar_navigation code, and is included with the turtlebot3 packages.

If it isn't present, it can be installed with

```sh
sudo apt install ros-kinetic-turtlebot3-slam
```

Assuming that you have already run the steps for lidar navigation, all that needs to be done is:

```sh
# Start the SLAM node
roslaunch turtlebot3_slam turtlebot3_slam.launch
# Visualize the map, the points the lidar detects, and the robot's position within it
rosrun rviz rviz -d `rospack find turtlebot3_slam`/rviz/turtlebot3_slam.rviz
```

You can then save the map itself to a file with
```sh
rosrun map_server map_saver -f ~/map
```



# Reference
[Turtlebot3 E-manual](http://emanual.robotis.com/)

[Lidar Navigation repo](https://github.com/athenian-robotics/lidar_navigation)
