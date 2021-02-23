import json

if __name__ == '__main__':
    # detection_file = '/home/jingxin/Nutstore Files/Nutstore/try/MOT/Multi-Modal-MOT/multi-radar/detection.json'
    # track_file = '/home/jingxin/Nutstore Files/Nutstore/try/MOT/Multi-Modal-MOT/multi-radar/track.json'
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

            