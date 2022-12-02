#!/usr/bin/env python3
import rospy
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist
from turtlesim.srv import TeleportAbsolute
from turtlesim.srv import Spawn
from turtlesim.srv import Kill
from std_srvs.srv import Empty as EmptyServiceCall
from turtlesim.srv import SetPen 
import sys

pi=3.1415926535897
turtle_x=1
turtle_y=10.5
turtle_angle=0
desired_angle=0
spawn_theta=0
dist_travled=0
iterable=0

def set_position(turtle_name):
    global spawn_theta
    turtle_teleport=''.join(['/',turtle_name,'/teleport_absolute'])
    rospy.wait_for_service(turtle_teleport)
    Initial= rospy.ServiceProxy(turtle_teleport,TeleportAbsolute)
    Initial(1,10.5,spawn_theta)

def spawning(turtle_name):
    global spawn_theta
    rospy.wait_for_service('spawn')
    spawn_t2 = rospy.ServiceProxy('spawn', Spawn)
    spawn_t2(1,10.5,spawn_theta,turtle_name)

def call_set_pen_service(r,g,b,width,off,turtle_pen):
    try:
        set_pen = rospy.ServiceProxy(turtle_pen,SetPen)
        response = set_pen(r,g,b,width,off)
    except rospy.ServiceException as e:
        rospy.logwarn(e)

def path(points):
    global pi
    global spawn_theta
    global iterable
    x=[]
    y=[]
    x_distance_between=[]
    y_distance_between=[]
    dist=[]
    turn=[]

    for i in points:
        x.append(i[0])
        y.append(i[1])
    for i in range(2):
        if i==0:
            pass
        else:
            if x[i]>x[i-1] and y[i]==y[i-1]:
                theta=0
                spawn_theta=0
            elif x[i]<x[i-1] and y[i]==y[i-1]:
                theta=180
                spawn_theta=pi
            elif y[i]>y[i-1] and x[i]==x[i-1]:
                theta=90
                spawn_theta=pi/2
            elif y[i]<y[i-1] and x[i]==x[i-1]:
                theta=270
                spawn_theta=-pi/2
    for index in range(len(x)):
        if index>0:
            x_distance_between.append(x[index]-x[index-1])
            y_distance_between.append(y[index]-y[index-1])
    for i in range(len(points)):
        if i == 0:
            pass
        else:
            if theta == 0:
                if y[i]-y[i-1] == 0:
                    turn.append('None')
                elif x[i]-x[i-1] == 0:
                    if y[i]>y[i-1]:
                        turn.append('Left')
                        theta=90
                    elif y[i]<y[i-1]:
                        turn.append('Right')
                        theta=270
            elif theta == 90:
                if x[i]-x[i-1] == 0:
                    turn.append('None')
                else:
                    if x[i]>x[i-1]:
                        turn.append('Right')
                        theta=0
                    elif x[i]<x[i-1]:
                        turn.append('Left')
                        theta=180
            elif theta == 180:
                if y[i]-y[i-1] == 0:
                    turn.append('None')
                else:
                    if y[i]<y[i-1]:
                        turn.append('Left')
                        theta=270
                    elif y[i]>y[i-1]:
                        turn.append('Right')
                        theta=90
            elif theta == 270:
                if x[i]-x[i-1] == 0:
                    turn.append('None')
                else:
                    if x[i]>x[i-1]:
                        turn.append('Left')
                        theta=0
                    elif x[i]<x[i-1]:
                        turn.append('Right')
                        theta=180
    newlist=[]
    for i in range(len(x_distance_between)):
        newlist.append([turn[i],x_distance_between[i],y_distance_between[i]])
    return newlist

def pose_callback(pose: Pose):
    global turtle_x
    global turtle_y
    global turtle_angle
    turtle_x=pose.x
    turtle_y=pose.y
    turtle_angle=pose.theta

def rotate(turn,pub):
    global turtle_angle
    vel=Twist()
    speed=45
    angle=90
    if turn == 'None':
        pass
    elif turn == 'Left':
        angular_speed=speed*2*pi/360
        vel.angular.z=angular_speed
        if turtle_angle == 0:
            desired_angle=pi/2
        elif turtle_angle < 0.78 and turtle_angle > -0.78:
            desired_angle=pi/2
        elif turtle_angle < 2.35 and turtle_angle > 0.78:
            desired_angle=pi
        elif turtle_angle < -2.35 or turtle_angle > 2.35:
            desired_angle=-pi/2
        elif turtle_angle < 0 or turtle_angle > -2.35:
            desired_angle=0

        if desired_angle==pi/2:
            while turtle_angle<desired_angle:
                pub.publish(vel)
        elif desired_angle==pi:
            while turtle_angle<desired_angle:
                if turtle_angle<0:
                    break

                pub.publish(vel)
        elif desired_angle==-pi/2:
            while turtle_angle>0:
                pub.publish(vel)
            while turtle_angle<desired_angle:
                pub.publish(vel)
        elif desired_angle==0:
            while turtle_angle<desired_angle:
                pub.publish(vel)
    elif turn == 'Right':
        angular_speed=speed*2*pi/360
        vel.angular.z=-angular_speed
        if turtle_angle == 0:
            desired_angle=-pi/2
        elif turtle_angle < 0.78 and turtle_angle > -0.78:
            desired_angle=-pi/2
        elif turtle_angle > -2.35 and turtle_angle < -0.78:
            desired_angle=-pi
        elif turtle_angle < -2.35 or turtle_angle > 2.35:
            desired_angle=pi/2
        elif turtle_angle > 0 and turtle_angle < 2.35:
            desired_angle=0.0

        if desired_angle == -pi/2:
            while turtle_angle>desired_angle:
                pub.publish(vel)
        elif desired_angle == -pi:
            while turtle_angle>desired_angle:
                if turtle_angle>0:
                    break
                pub.publish(vel)
        elif desired_angle == pi/2:
            while turtle_angle<0:
                pub.publish(vel)
            while turtle_angle>desired_angle:
                pub.publish(vel)
        elif desired_angle == 0:
            while turtle_angle>desired_angle:
                pub.publish(vel)
    vel.angular.z=0
    pub.publish(vel)
    
def forward(dist_x,dist_y,pub):
    global turtle_x
    global turtle_y
    global turtle_angle
    global dist_travled
    global iterable

    lin_vel=Twist()
    lin_vel.linear.x=2.0 
    destiation_x=dist_x+turtle_x
    destiation_y=dist_y+turtle_y
    dist_travled+=abs(dist_x)
    dist_travled+=abs(dist_y)

    if (turtle_angle < 0.78 and turtle_angle > -0.78) or (turtle_angle>2.35 or turtle_angle<-2.35):
        if dist_x>0:
            while turtle_x<destiation_x:
                pub.publish(lin_vel)
            lin_vel.linear.x=0
            pub.publish(lin_vel)
        elif dist_x<0:
            while turtle_x>destiation_x:
                pub.publish(lin_vel)
            lin_vel.linear.x=0
            pub.publish(lin_vel)
    elif (turtle_angle>0.78 and turtle_angle<2.35) or (turtle_angle<-0.78 and turtle_angle>-2.35):
        if dist_y>0:
            while turtle_y<destiation_y:
                pub.publish(lin_vel)
            lin_vel.linear.x=0
            pub.publish(lin_vel)
        elif dist_y<0:
            while turtle_y>destiation_y:
                pub.publish(lin_vel)
            lin_vel.linear.x=0
            pub.publish(lin_vel)

def move(turn,dist_x,dist_y,pub):
    rotate(turn,pub)
    forward(dist_x,dist_y,pub)

## The exact lines I used for my package and file
# rosrun my_robot_controller turtle_controller.py turtle1
# rosrun my_robot_controller turtle_controller.py turtle2
  
if __name__ == '__main__':
    rospy.init_node("turtle_controller",anonymous= True)

    turtle_name=sys.argv[1]

    turtle_pubTopic=''.join(['/',turtle_name,'/cmd_vel'])
    turtle_subTopic=''.join(['/',turtle_name,'/pose'])

    while not rospy.is_shutdown():
        pub = rospy.Publisher(turtle_pubTopic,Twist,queue_size=10)
        sub = rospy.Subscriber(turtle_subTopic,Pose,callback=pose_callback)        

        if turtle_name == 'turtle1':
            x = [400,380,360,360,340,340,340,340,320,300,300,320,320,300,280,280,280,280,260,240,240,240,240,220,220,220,220,200,200,180,180,180,200,220,220,200,200,220,220,240,240,260,260,280,280,260,240,240,220,200,200,180,180,180,160,160,160,140,120,100,100,100,80,80,60,60,80,80,80,80,100,100,120,120,100,100,100,120,120,120,140,140,140,140,160,160,140,140,140,140,140,120,100,100,80,60,60,60,60,40,20,20,40,40,20,20,20,40,40,60,60,80,80,80,60,40,20,20,40,40,40,60,60,80,80,80,80,60,60,40,20,20,20,40,40,20] 
            y = [380,380,380,400,400,380,360,340,340,340,360,360,380,380,380,360,340,320,320,320,340,360,380,380,360,340,320,320,340,340,320,300,300,300,280,280,260,260,240,240,260,260,240,240,220,220,220,200,200,200,220,220,240,260,260,240,220,220,220,220,240,260,260,280,280,300,300,320,340,360,360,340,340,320,320,300,280,280,260,240,240,260,280,300,300,320,320,340,360,380,400,400,400,380,380,380,360,340,320,320,320,300,300,280,280,260,240,240,220,220,240,240,220,200,200,200,200,180,180,160,140,140,120,120,100,80,60,60,80,80,80,60,40,40,20,20]
        elif turtle_name == 'turtle2':
            x = [380,360,340,320,300,300,280,280,260,240,220,220,240,260,260,240,220,200,180,180,180,200,200,180,180,200,220,220,240,240,240,260,280,300,300,320,340,340,340,340,360,380,380,380,360,360,380,400,400,400,380,380,360,360,360,360,380,380,400,400,400,380,380,360,360,340,320,300,300,280,260,260,280,280,280,260,240,240,220,220,240,240,240,260,260,240,240,220,200,200,200,200,180,180,160,140,140,140,160,160,180,180,160,140,120,100,80,60,60,80,80,80,100,120,120,120,140,160,180,180,160,140,140,120,120,100,80,80,80,60,60,60,40,40,20,20] 
            y = [400,400,400,400,400,380,380,360,360,360,360,380,380,380,400,400,400,400,400,380,360,360,340,340,320,320,320,300,300,320,340,340,340,340,320,320,320,340,360,380,380,380,360,340,340,320,320,320,300,280,280,300,300,280,260,240,240,260,260,240,220,220,200,200,220,220,220,220,200,200,200,220,220,240,260,260,260,240,240,220,220,200,180,180,160,160,140,140,140,120,100,80,80,100,100,100,80,60,60,40,40,20,20,20,20,20,20,20,40,40,60,80,80,80,100,120,120,120,120,140,140,140,160,160,140,140,140,120,100,100,80,60,60,40,40,20]
        elif turtle_name == 'turtle3':
            x = [400, 380, 380, 380, 400, 400, 400, 380, 380, 360, 360, 360, 360, 360, 360, 340, 340, 320, 300, 300, 280, 260, 260, 240, 220, 200, 180, 180, 200, 200, 180, 180, 200, 220, 220, 220, 240, 240, 260, 280, 280, 280, 260, 240, 220, 200, 180, 160, 160, 180, 200, 220, 220, 220, 220, 220, 220, 240, 240, 220, 220, 200, 200, 180, 180, 160, 160, 140, 120, 120, 100, 100, 80, 60, 40, 40, 60, 60, 80, 80, 100, 120, 120, 120, 100, 80, 80, 60, 40, 20]
            y = [380, 380, 360, 340, 340, 320, 300, 300, 280, 280, 300, 320, 340, 360, 380, 380, 400, 400, 400, 380, 380, 380, 400, 400, 400, 400, 400, 380, 380, 360, 360, 340, 340, 340, 360, 380, 380, 360, 360, 360, 340, 320, 320, 320, 320, 320, 320, 320, 300, 300, 300, 300, 280, 260, 240, 220, 200, 200, 180, 180, 160, 160, 180, 180, 160, 160, 140, 140, 140, 120, 120, 100, 100, 100, 100, 80, 80, 60, 60, 80, 80, 80, 60, 40, 40, 40, 20, 20, 20, 20]
            
        y_flipped=[]
        for i in y:
            y_flipped.append(abs(i-400))
        reversed_y=y_flipped[::-1]
        reversed_x=x[::-1]

        scaled_y=[]
        scaled_x=[]
        for index, value in enumerate(reversed_y):
            scaled_y.append(value/40+1)
            scaled_x.append(reversed_x[index]/40+0.5)

        z=10
        # z=len(scaled_x)
        
        points=[]
        for i in range(z):
            points.append([scaled_x[i],scaled_y[i]])

        path_list1 = path(points)

        if turtle_name == 'turtle1': 
            kill_turtle = rospy.ServiceProxy('kill', Kill)
            try:
                kill_turtle(turtle_name)
            except:
                pass
            spawning(turtle_name)
            turtle_pen=''.join(['/',turtle_name,'/set_pen'])
            rospy.wait_for_service(turtle_pen)
            call_set_pen_service(255,255,255,3,0,turtle_pen)
            rospy.wait_for_service('/turtle2/set_pen') ## switch to the last name of your turtle you intend to use 

        elif turtle_name == 'turtle2':            
            kill_turtle = rospy.ServiceProxy('kill', Kill)
            try:
                kill_turtle(turtle_name)
            except:
                pass
            spawning(turtle_name)
            turtle_pen=''.join(['/',turtle_name,'/set_pen'])
            rospy.wait_for_service(turtle_pen)
            call_set_pen_service(255,0,0,3,0,turtle_pen)
            rospy.wait_for_service('/turtle2/set_pen') ## switch to the last name of your turtle you intend to use 

    ## if you would like to run all three turtle change the turtle2 -> turtle3 in lines: 301,313

        # elif turtle_name == 'turtle3':            
        #     kill_turtle = rospy.ServiceProxy('kill', Kill)
        #     try:
        #         kill_turtle(turtle_name)
        #     except:
        #         pass
        #     spawning(turtle_name)
        #     turtle_pen=''.join(['/',turtle_name,'/set_pen'])
        #     rospy.wait_for_service(turtle_pen)
        #     call_set_pen_service(0,0,0,3,0,turtle_pen)
        
        rospy.sleep(2)

        t0=rospy.Time.now().to_sec()
        
        for i in path_list1:
            move(i[0],i[1],i[2],pub)
        
        t1=rospy.Time.now().to_sec()
        duration = t1 - t0
        
        rospy.loginfo("Distance traveled: %s meters",dist_travled)
        rospy.loginfo("Time it took to travel: %s seconds",duration)
        break