# -*- coding: UTF-8 -*-

import rospy
import json
import sys
import signal
import keyboard
import numpy as np

from visualization_msgs.msg import MarkerArray
from visualization_msgs.msg import Marker

type = ['point', 'car', 'truck', 'pedstrain', 'motorcycle', 'bicycle', 'wide', 'tbd']
# detection_file = '/home/jingxin/Nutstore Files/Nutstore/try/MOT/Multi-Modal-MOT/multi-radar/detection.json'
# track_file = '/home/jingxin/Nutstore Files/Nutstore/try/MOT/Multi-Modal-MOT/multi-radar/track.json'
detection1_file = '/mnt/d/Nutstore/Nutstore/try/MOT/Multi-Modal-MOT/multi-radar/detection1.json'
detection2_file = '/mnt/d/Nutstore/Nutstore/try/MOT/Multi-Modal-MOT/multi-radar/detection2.json'
detection3_file = '/mnt/d/Nutstore/Nutstore/try/MOT/Multi-Modal-MOT/multi-radar/detection3.json'
detection4_file = '/mnt/d/Nutstore/Nutstore/try/MOT/Multi-Modal-MOT/multi-radar/detection4.json'
detection_all_file = '/mnt/d/Nutstore/Nutstore/try/MOT/Multi-Modal-MOT/multi-radar/detection_all.json'
detection_cluster_file = '/mnt/d/Nutstore/Nutstore/try/MOT/Multi-Modal-MOT/multi-radar/detection_all_cluster.json'
track_file = '/mnt/d/Nutstore/Nutstore/try/MOT/Multi-Modal-MOT/multi-radar/track.json'

isGPS = False

def signal_handling(signum, frame):
    global terminate                         
    terminate = True  

def yaw_to_quaternion(yaw):
    qx = 0
    qy = 0
    qz = np.sin(yaw / 2)
    qw = np.cos(yaw / 2)
    
    return [qx, qy, qz, qw]

def visualize_position(index, hz):
    bbox_pub = rospy.Publisher('radardet', MarkerArray, queue_size=5)
    text_pub = rospy.Publisher('radartext', MarkerArray, queue_size=5)
    arrow_pub = rospy.Publisher('radararrow', MarkerArray, queue_size=5)
    rate = rospy.Rate(hz)
    with open(track_file) as track_f:
        track_data = json.load(track_f)
    if index == 1:
        with open(detection1_file) as f:
            data = json.load(f)
    elif index == 2:
        with open(detection2_file) as f:
            data = json.load(f)
    elif index == 3:
        with open(detection3_file) as f:
            data = json.load(f)
    elif index == 4:
        with open(detection4_file) as f:
            data = json.load(f)
    max_marker_size = 0
    for i in range(len(data)):
        print("index is ", i)
        print("object num", len(data["sample"+str(i)]))
        if terminate:
            break
        radar1box = MarkerArray()
        radar1text = MarkerArray()
        radar1arrow = MarkerArray()
        marker_id = 0
        for j in range(len(data["sample"+str(i)])):
            bbox_marker = Marker()
            bbox_marker.header.frame_id = "radar1"
            bbox_marker.header.stamp = rospy.Time.now()
            bbox_marker.ns = ""
            bbox_marker.color.r = 1.0
            bbox_marker.color.g = 0.0
            bbox_marker.color.b = 0.0
            bbox_marker.color.a = 0.2
            bbox_marker.type = Marker.CUBE
            bbox_marker.action = Marker.ADD
            bbox_marker.frame_locked = True
            bbox_marker.id = marker_id
            bbox_marker.pose.position.x = data["sample"+str(i)][str(j)]['pose'][0]
            bbox_marker.pose.position.y = data["sample"+str(i)][str(j)]['pose'][1]
            bbox_marker.pose.position.z = 0
            orientation = yaw_to_quaternion(data["sample"+str(i)][str(j)]['pose'][2])
            bbox_marker.pose.orientation.w = orientation[3]
            bbox_marker.pose.orientation.x = orientation[0]
            bbox_marker.pose.orientation.y = orientation[1]
            bbox_marker.pose.orientation.z = orientation[2]
            bbox_marker.scale.x = 3
            bbox_marker.scale.y = 3
            bbox_marker.scale.z = 0
            radar1box.markers.append(bbox_marker)

            text_marker = Marker()
            text_marker.header.frame_id = "radar1"
            text_marker.header.stamp = rospy.Time.now()
            text_marker.ns = ""
            text_marker.color.r = 255
            text_marker.color.g = 255
            text_marker.color.b = 255
            text_marker.color.a = 1.0
            text_marker.type = Marker.TEXT_VIEW_FACING
            text_marker.action = Marker.ADD
            text_marker.frame_locked = True
            text_marker.id = marker_id
            text_marker.pose.position.x = data["sample"+str(i)][str(j)]['pose'][0]
            text_marker.pose.position.y = data["sample"+str(i)][str(j)]['pose'][1]
            text_marker.pose.position.z = 0
            text_marker.pose.orientation.w = 1
            text_marker.pose.orientation.x = 0
            text_marker.pose.orientation.y = 0
            text_marker.pose.orientation.z = 0
            text_marker.scale.x = 1
            text_marker.scale.y = 1
            text_marker.scale.z = 2
            # text_marker.text = type[data["sample"+str(i)][str(j)]['type']]
            # text_marker.text = "det" + str(j)
            text_marker.text = str(track_data["sample"+str(i)][str(j)]['id'])
            radar1text.markers.append(text_marker)

            arrow_marker = Marker()
            arrow_marker.header.frame_id = "radar1"
            arrow_marker.header.stamp = rospy.Time.now()
            arrow_marker.ns = ""
            arrow_marker.color.r = 1.0
            arrow_marker.color.g = 0.0
            arrow_marker.color.b = 0.0
            arrow_marker.color.a = 1.0
            arrow_marker.type = Marker.ARROW
            arrow_marker.action = Marker.ADD
            arrow_marker.frame_locked = True
            arrow_marker.id = marker_id
            arrow_marker.pose.position.x = data["sample"+str(i)][str(j)]['pose'][0]
            arrow_marker.pose.position.y = data["sample"+str(i)][str(j)]['pose'][1]
            arrow_marker.pose.position.z = 0
            arrow_marker.pose.orientation.w = orientation[3]
            arrow_marker.pose.orientation.x = orientation[0]
            arrow_marker.pose.orientation.y = orientation[1]
            arrow_marker.pose.orientation.z = orientation[2]
            arrow_marker.scale.x = 3
            arrow_marker.scale.y = 0.3
            arrow_marker.scale.z = 0.3
            radar1arrow.markers.append(arrow_marker)
            marker_id += 1

        if (len(data["sample"+str(i)]) > max_marker_size):
            max_marker_size = len(data["sample"+str(i)])
        for k in range(marker_id, max_marker_size):
            bbox_marker = Marker()
            bbox_marker.header.frame_id = "radar1"
            bbox_marker.header.stamp = rospy.Time.now()
            bbox_marker.ns = ""
            bbox_marker.color.r = 1.0
            bbox_marker.color.g = 0.0
            bbox_marker.color.b = 0.0
            bbox_marker.color.a = 0.0
            bbox_marker.type = Marker.CUBE
            bbox_marker.action = Marker.ADD
            bbox_marker.frame_locked = True
            bbox_marker.id = k
            bbox_marker.pose.position.x = 0
            bbox_marker.pose.position.y = 0
            bbox_marker.pose.position.z = 0
            bbox_marker.scale.x = 0
            bbox_marker.scale.y = 0
            bbox_marker.scale.z = 0
            radar1box.markers.append(bbox_marker)

            text_marker = Marker()
            text_marker.header.frame_id = "radar1"
            text_marker.header.stamp = rospy.Time.now()
            text_marker.ns = ""
            text_marker.color.r = 1.0
            text_marker.color.g = 0.0
            text_marker.color.b = 0.0
            text_marker.color.a = 0.0
            text_marker.type = Marker.TEXT_VIEW_FACING
            text_marker.action = Marker.ADD
            text_marker.frame_locked = True
            text_marker.id = k
            text_marker.pose.position.x = 0
            text_marker.pose.position.y = 0
            text_marker.pose.position.z = 0
            text_marker.scale.x = 0
            text_marker.scale.y = 0
            text_marker.scale.z = 0
            text_marker.text = "det" + str(j)
            radar1text.markers.append(text_marker)

            arrow_marker = Marker()
            arrow_marker.header.frame_id = "radar1"
            arrow_marker.header.stamp = rospy.Time.now()
            arrow_marker.ns = ""
            arrow_marker.color.r = 1.0
            arrow_marker.color.g = 0.0
            arrow_marker.color.b = 0.0
            arrow_marker.color.a = 0.0
            arrow_marker.type = Marker.ARROW
            arrow_marker.action = Marker.ADD
            arrow_marker.frame_locked = True
            arrow_marker.id = k
            arrow_marker.pose.position.x = 0
            arrow_marker.pose.position.y = 0
            arrow_marker.pose.position.z = 0
            arrow_marker.scale.x = 0
            arrow_marker.scale.y = 0
            arrow_marker.scale.z = 0
            radar1arrow.markers.append(arrow_marker)
            marker_id += 1
        
        bbox_pub.publish(radar1box)
        text_pub.publish(radar1text)
        arrow_pub.publish(radar1arrow)
        rate.sleep()


def visualize_gps(index, hz):
    bbox_pub = rospy.Publisher('radardet', MarkerArray, queue_size=5)
    text_pub = rospy.Publisher('radartext', MarkerArray, queue_size=5)
    arrow_pub = rospy.Publisher('radararrow', MarkerArray, queue_size=5)
    rate = rospy.Rate(hz)
    if index == 0:
        with open(detection_all_file) as f:
            data = json.load(f)
    if index == 1:
        with open(detection1_file) as f:
            data = json.load(f)
    elif index == 2:
        with open(detection2_file) as f:
            data = json.load(f)
    elif index == 3:
        with open(detection3_file) as f:
            data = json.load(f)
    elif index == 4:
        with open(detection4_file) as f:
            data = json.load(f)
    elif index == 5:
        with open(detection_cluster_file) as f:
            data = json.load(f)
    max_marker_size = 0
    for i in range(len(data)):
        print("index is ", i)
        print("object num", len(data["sample"+str(i)]))
        if terminate:
            break
        radar1box = MarkerArray()
        radar1text = MarkerArray()
        radar1arrow = MarkerArray()
        marker_id = 0
        for j in range(len(data["sample"+str(i)])):
            bbox_marker = Marker()
            bbox_marker.header.frame_id = "radar1"
            bbox_marker.header.stamp = rospy.Time.now()
            bbox_marker.ns = ""
            bbox_marker.color.r = 1.0
            bbox_marker.color.g = 0.0
            bbox_marker.color.b = 0.0
            bbox_marker.color.a = 0.2
            bbox_marker.type = Marker.CUBE
            bbox_marker.action = Marker.ADD
            bbox_marker.frame_locked = True
            bbox_marker.id = marker_id
            bbox_marker.pose.position.x = (data["sample"+str(i)][str(j)]['gps'][0] * 100 - 3054) * 1000 - 200
            bbox_marker.pose.position.y = (data["sample"+str(i)][str(j)]['gps'][1] * 100 - 11998) * 1000 - 900
            print("lat", bbox_marker.pose.position.x)
            print("lon", bbox_marker.pose.position.y)
            bbox_marker.pose.position.z = 0
            orientation = yaw_to_quaternion(data["sample"+str(i)][str(j)]['pose'][2])
            bbox_marker.pose.orientation.w = orientation[3]
            bbox_marker.pose.orientation.x = orientation[0]
            bbox_marker.pose.orientation.y = orientation[1]
            bbox_marker.pose.orientation.z = orientation[2]
            bbox_marker.scale.x = 3
            bbox_marker.scale.y = 3
            bbox_marker.scale.z = 0
            radar1box.markers.append(bbox_marker)

            text_marker = Marker()
            text_marker.header.frame_id = "radar1"
            text_marker.header.stamp = rospy.Time.now()
            text_marker.ns = ""
            text_marker.color.r = 255
            text_marker.color.g = 255
            text_marker.color.b = 255
            text_marker.color.a = 1.0
            text_marker.type = Marker.TEXT_VIEW_FACING
            text_marker.action = Marker.ADD
            text_marker.frame_locked = True
            text_marker.id = marker_id
            text_marker.pose.position.x = (data["sample"+str(i)][str(j)]['gps'][0] * 100 - 3054) * 10
            text_marker.pose.position.y = (data["sample"+str(i)][str(j)]['gps'][1] * 100 - 11998) * 10
            text_marker.pose.position.z = 0
            text_marker.pose.orientation.w = 1
            text_marker.pose.orientation.x = 0
            text_marker.pose.orientation.y = 0
            text_marker.pose.orientation.z = 0
            text_marker.scale.x = 1
            text_marker.scale.y = 1
            text_marker.scale.z = 2
            # text_marker.text = type[data["sample"+str(i)][str(j)]['type']]
            text_marker.text = "det" + str(j)
            # text_marker.text = str(track_data["sample"+str(i)][str(j)]['id'])
            radar1text.markers.append(text_marker)

            arrow_marker = Marker()
            arrow_marker.header.frame_id = "radar1"
            arrow_marker.header.stamp = rospy.Time.now()
            arrow_marker.ns = ""
            arrow_marker.color.r = 1.0
            arrow_marker.color.g = 0.0
            arrow_marker.color.b = 0.0
            arrow_marker.color.a = 1.0
            arrow_marker.type = Marker.ARROW
            arrow_marker.action = Marker.ADD
            arrow_marker.frame_locked = True
            arrow_marker.id = marker_id
            arrow_marker.pose.position.x = (data["sample"+str(i)][str(j)]['gps'][0] * 100 - 3054) * 10
            arrow_marker.pose.position.y = (data["sample"+str(i)][str(j)]['gps'][1] * 100 - 11998) * 10
            arrow_marker.pose.position.z = 0
            arrow_marker.pose.orientation.w = orientation[3]
            arrow_marker.pose.orientation.x = orientation[0]
            arrow_marker.pose.orientation.y = orientation[1]
            arrow_marker.pose.orientation.z = orientation[2]
            arrow_marker.scale.x = 3
            arrow_marker.scale.y = 0.3
            arrow_marker.scale.z = 0.3
            radar1arrow.markers.append(arrow_marker)
            marker_id += 1

        if (len(data["sample"+str(i)]) > max_marker_size):
            max_marker_size = len(data["sample"+str(i)])
        for k in range(marker_id, max_marker_size):
            bbox_marker = Marker()
            bbox_marker.header.frame_id = "radar1"
            bbox_marker.header.stamp = rospy.Time.now()
            bbox_marker.ns = ""
            bbox_marker.color.r = 1.0
            bbox_marker.color.g = 0.0
            bbox_marker.color.b = 0.0
            bbox_marker.color.a = 0.0
            bbox_marker.type = Marker.CUBE
            bbox_marker.action = Marker.ADD
            bbox_marker.frame_locked = True
            bbox_marker.id = k
            bbox_marker.pose.position.x = 0
            bbox_marker.pose.position.y = 0
            bbox_marker.pose.position.z = 0
            bbox_marker.scale.x = 0
            bbox_marker.scale.y = 0
            bbox_marker.scale.z = 0
            radar1box.markers.append(bbox_marker)

            text_marker = Marker()
            text_marker.header.frame_id = "radar1"
            text_marker.header.stamp = rospy.Time.now()
            text_marker.ns = ""
            text_marker.color.r = 1.0
            text_marker.color.g = 0.0
            text_marker.color.b = 0.0
            text_marker.color.a = 0.0
            text_marker.type = Marker.TEXT_VIEW_FACING
            text_marker.action = Marker.ADD
            text_marker.frame_locked = True
            text_marker.id = k
            text_marker.pose.position.x = 0
            text_marker.pose.position.y = 0
            text_marker.pose.position.z = 0
            text_marker.scale.x = 0
            text_marker.scale.y = 0
            text_marker.scale.z = 0
            text_marker.text = "det" + str(j)
            radar1text.markers.append(text_marker)

            arrow_marker = Marker()
            arrow_marker.header.frame_id = "radar1"
            arrow_marker.header.stamp = rospy.Time.now()
            arrow_marker.ns = ""
            arrow_marker.color.r = 1.0
            arrow_marker.color.g = 0.0
            arrow_marker.color.b = 0.0
            arrow_marker.color.a = 0.0
            arrow_marker.type = Marker.ARROW
            arrow_marker.action = Marker.ADD
            arrow_marker.frame_locked = True
            arrow_marker.id = k
            arrow_marker.pose.position.x = 0
            arrow_marker.pose.position.y = 0
            arrow_marker.pose.position.z = 0
            arrow_marker.scale.x = 0
            arrow_marker.scale.y = 0
            arrow_marker.scale.z = 0
            radar1arrow.markers.append(arrow_marker)
            marker_id += 1
        
        bbox_pub.publish(radar1box)
        #text_pub.publish(radar1text)
        #arrow_pub.publish(radar1arrow)
        rate.sleep()
    


if __name__ == '__main__':
    terminate = False       
    signal.signal(signal.SIGINT,signal_handling) 
    rospy.init_node('visulize', anonymous=True)

    if isGPS:
        visualize_gps(index=5, hz=9)
    else:
        visualize_position(index=1, hz=9)