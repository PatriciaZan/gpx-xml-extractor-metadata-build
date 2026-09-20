
def get_activity_start(points):
    #print(points[0])
    return points[0]["time"]

def get_activity_end(points):
    return points[-1]["time"]