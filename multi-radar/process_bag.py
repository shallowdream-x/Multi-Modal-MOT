import rospy
import json

from radar_msgs.msg import RadarObjectsArray

json_filename1 = "/mnt/d/Nutstore/Nutstore/try/MOT/Multi-Modal-MOT/multi-radar/detection1.json"
json_filename2 = "/mnt/d/Nutstore/Nutstore/try/MOT/Multi-Modal-MOT/multi-radar/detection2.json"
json_filename3 = "/mnt/d/Nutstore/Nutstore/try/MOT/Multi-Modal-MOT/multi-radar/detection3.json"
json_filename4 = "/mnt/d/Nutstore/Nutstore/try/MOT/Multi-Modal-MOT/multi-radar/detection4.json"

class process_bag(object):
    
    def __init__(self):
        radar1_sub = rospy.Subscriber("/radar_wjj_test/sondit__001", RadarObjectsArray, self.radar1callback)
        radar2_sub = rospy.Subscriber("/radar_wjj_test/sondit__002", RadarObjectsArray, self.radar2callback)
        radar3_sub = rospy.Subscriber("/radar_wjj_test/sondit__003", RadarObjectsArray, self.radar3callback)
        radar4_sub = rospy.Subscriber("/radar_wjj_test/sondit__004", RadarObjectsArray, self.radar4callback)
        self.radar1_frame = 0
        self.radar2_frame = 0
        self.radar3_frame = 0
        self.radar4_frame = 0
        self.data1 = {}
        self.data2 = {}
        self.data3 = {}
        self.data4 = {}

    def radar1callback(self, msg):
        sample = {}
        for i in range(msg.object_num):
            detection = {}
            detection['pose'] = [msg.objects_general[i].pos_x, msg.objects_general[i].pos_y, msg.objects_general[i].OrientationAngle]
            detection['type'] = msg.objects_general[i].type
            detection['gps'] = [msg.objects_general[i].lat, msg.objects_general[i].lon]
            detection['velocity'] = [msg.objects_general[i].Vx, msg.objects_general[i].Vy]
            detection['status'] = [msg.objects_general[i].DynProp, msg.objects_general[i].RCS, msg.objects_general[i].ProbOfExist, msg.objects_general[i].MeasState, msg.objects_general[i].valid]
            sample[str(i)] = detection
        self.data1["sample" + str(self.radar1_frame)] = sample
        self.radar1_frame += 1

    
    def radar2callback(self, msg):
        sample = {}
        for i in range(msg.object_num):
            detection = {}
            detection['pose'] = [msg.objects_general[i].pos_x, msg.objects_general[i].pos_y, msg.objects_general[i].OrientationAngle]
            detection['type'] = msg.objects_general[i].type
            detection['gps'] = [msg.objects_general[i].lat, msg.objects_general[i].lon]
            detection['velocity'] = [msg.objects_general[i].Vx, msg.objects_general[i].Vy]
            detection['status'] = [msg.objects_general[i].DynProp, msg.objects_general[i].RCS, msg.objects_general[i].ProbOfExist, msg.objects_general[i].MeasState, msg.objects_general[i].valid]
            sample[str(i)] = detection
        self.data2["sample" + str(self.radar2_frame)] = sample
        self.radar2_frame += 1

    
    def radar3callback(self, msg):
        sample = {}
        for i in range(msg.object_num):
            detection = {}
            detection['pose'] = [msg.objects_general[i].pos_x, msg.objects_general[i].pos_y, msg.objects_general[i].OrientationAngle]
            detection['type'] = msg.objects_general[i].type
            detection['gps'] = [msg.objects_general[i].lat, msg.objects_general[i].lon]
            detection['velocity'] = [msg.objects_general[i].Vx, msg.objects_general[i].Vy]
            detection['status'] = [msg.objects_general[i].DynProp, msg.objects_general[i].RCS, msg.objects_general[i].ProbOfExist, msg.objects_general[i].MeasState, msg.objects_general[i].valid]
            sample[str(i)] = detection
        self.data3["sample" + str(self.radar3_frame)] = sample
        self.radar3_frame += 1

    
    def radar4callback(self, msg):
        sample = {}
        for i in range(msg.object_num):
            detection = {}
            detection['pose'] = [msg.objects_general[i].pos_x, msg.objects_general[i].pos_y, msg.objects_general[i].OrientationAngle]
            detection['type'] = msg.objects_general[i].type
            detection['gps'] = [msg.objects_general[i].lat, msg.objects_general[i].lon]
            detection['velocity'] = [msg.objects_general[i].Vx, msg.objects_general[i].Vy]
            detection['status'] = [msg.objects_general[i].DynProp, msg.objects_general[i].RCS, msg.objects_general[i].ProbOfExist, msg.objects_general[i].MeasState, msg.objects_general[i].valid]
            sample[str(i)] = detection
        self.data4["sample" + str(self.radar4_frame)] = sample
        self.radar4_frame += 1
    
    def __del__(self):
        for i in range(155, 185):
            del self.data1["sample"+str(i)]
        for i in range(155, 185):
            del self.data2["sample"+str(i)]
        for i in range(155, 187):
            del self.data3["sample"+str(i)]
        for i in range(155, 186):
            del self.data4["sample"+str(i)]
        with open(json_filename1, 'w') as f:
            json.dump(self.data1, f)
        with open(json_filename2, 'w') as f:
            json.dump(self.data2, f)
        with open(json_filename3, 'w') as f:
            json.dump(self.data3, f)
        with open(json_filename4, 'w') as f:
            json.dump(self.data4, f)
        print("json file is written!")

if __name__ == '__main__':
    rospy.init_node('process_bag', anonymous=True)
    process_bag()
    rospy.spin()
    
    