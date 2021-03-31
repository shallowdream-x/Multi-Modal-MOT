import json
import numpy as np

np.set_printoptions(threshold=np.inf)

def valid_gps():
    detection_file = '/mnt/d/Nutstore/Nutstore/try/MOT/Multi-Modal-MOT/multi-radar/detection.json'
    track_file = '/mnt/d/Nutstore/Nutstore/try/MOT/Multi-Modal-MOT/multi-radar/track.json'
    unlat_num = 0
    unlon_num = 0
    with open(detection_file) as f:
        data = json.load(f)
    for i in range(len(data)):
        for j in range(len(data["sample"+str(i)])):
            if int(data["sample"+str(i)][str(j)]["gps"][0] * 100) != 3054:
                unlat_num += 1
                print(int(data["sample"+str(i)][str(j)]["gps"][0] * 1000))
            if int(data["sample"+str(i)][str(j)]["gps"][1] * 100) != 11998:
                unlon_num += 1
    print("unlat_num", unlat_num)
    print("unlon_num", unlon_num)
    return (unlat_num, unlon_num)


def merge_multi_radar():
    data = {}
    detection1_file = '/mnt/d/Nutstore/Nutstore/try/MOT/Multi-Modal-MOT/multi-radar/detection1.json'
    detection2_file = '/mnt/d/Nutstore/Nutstore/try/MOT/Multi-Modal-MOT/multi-radar/detection2.json'
    detection3_file = '/mnt/d/Nutstore/Nutstore/try/MOT/Multi-Modal-MOT/multi-radar/detection3.json'
    detection4_file = '/mnt/d/Nutstore/Nutstore/try/MOT/Multi-Modal-MOT/multi-radar/detection4.json'
    detection_all_file = '/mnt/d/Nutstore/Nutstore/try/MOT/Multi-Modal-MOT/multi-radar/detection_all.json'
    with open(detection1_file) as f1:
        data1 = json.load(f1)
    with open(detection2_file) as f2:
        data2 = json.load(f2)
    with open(detection3_file) as f3:
        data3 = json.load(f3)
    with open(detection4_file) as f4:
        data4 = json.load(f4)
    for i in range(len(data1)):
        sample = {}
        for a in range(len(data1["sample"+str(i)])):
            sample[str(a)] = data1["sample"+str(i)][str(a)]
            sample[str(a)]["sensor_source"] = "radar1"
        for b in range(len(data2["sample"+str(i)])):
            sample[str(a+b+1)] = data2["sample"+str(i)][str(b)]
            sample[str(a+b+1)]["sensor_source"] = "radar2"
        for c in range(len(data3["sample"+str(i)])):
            sample[str(a+b+c+2)] = data3["sample"+str(i)][str(c)]
            sample[str(a+b+c+2)]["sensor_source"] = "radar3"
        for d in range(len(data4["sample"+str(i)])):
            sample[str(a+b+c+d+3)] = data4["sample"+str(i)][str(d)]
            sample[str(a+b+c+d+3)]["sensor_source"] = "radar4"
        data["sample"+str(i)] = sample
    with open(detection_all_file, 'w') as f5:
            json.dump(data, f5)
    print("write json finished!")


def cluster(output=True):
    detection_all_file = '/mnt/d/Nutstore/Nutstore/try/MOT/Multi-Modal-MOT/multi-radar/detection_all.json'
    output_file = '/mnt/d/Nutstore/Nutstore/try/MOT/Multi-Modal-MOT/multi-radar/detection_all_cluster.json'
    unuse_detection_all = []
    thre = 4
    with open(detection_all_file) as f:
        data = json.load(f)
    for i in range(len(data)):
        unuse_detection = []
        cost = np.zeros((len(data["sample"+str(i)]), len(data["sample"+str(i)])))
        for j in range(len(data["sample"+str(i)])):
            unuse_detection_tmp = []
            for k in range(j):
                lat_j = (data["sample"+str(i)][str(j)]['gps'][0] * 100 - 3054) * 1000 - 200
                lon_j = (data["sample"+str(i)][str(j)]['gps'][1] * 100 - 11998) * 1000 - 900
                lat_k = (data["sample"+str(i)][str(k)]['gps'][0] * 100 - 3054) * 1000 - 200
                lon_k = (data["sample"+str(i)][str(k)]['gps'][1] * 100 - 11998) * 1000 - 900
                cost[j][k] = np.sqrt(np.square(lat_j - lat_k) + np.square(lon_j - lon_k))
                if cost[j][k] < thre:
                    unuse_detection_tmp.append((j, k))
            if len(unuse_detection_tmp) > 1:
                unuse_detection.append(unuse_detection_tmp[0][0])
                for m in range(len(unuse_detection_tmp)-1):
                    unuse_detection.append(unuse_detection_tmp[m][1])
            elif len(unuse_detection_tmp) == 1:
                unuse_detection.append(unuse_detection_tmp[0][0])
            else:
                continue
        unuse_detection_all.append(unuse_detection)
    if (output):
        data_cluster = {}
        for i in range(len(data)):
            sample = {}
            detection_cluster = [x for x in range(len(data["sample"+str(i)])) if x not in unuse_detection_all[i]]
            for j in range(len(data["sample"+str(i)])-len(unuse_detection_all[i])):
                sample[str(j)] = data["sample"+str(i)][str(detection_cluster[j])]
            data_cluster["sample"+str(i)] = sample
            # if i == 0:
            #     print(len(detection_cluster))
            #     print(len(data["sample"+str(i)])-len(unuse_detection_all[i]))
            #     print(range(len(data["sample"+str(i)])))
            #     print(unuse_detection_all[i])
            #     print(detection_cluster)
        with open(output_file, 'w') as f:
            json.dump(data_cluster, f)

    return unuse_detection_all

    

if __name__ == '__main__':
    merge_multi_radar()  
    

            