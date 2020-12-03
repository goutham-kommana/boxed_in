rosservice call gazebo/delete_model my_robot
rosrun gazebo_ros spawn_model -file ~/catkin_ws/src/gazebo/models/my_robot/model.sdf -sdf -model my_robot

cd src
python move_forward.py