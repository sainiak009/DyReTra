def parseClusterData(data) :
    data = data["roads"]
    result = []

    for road in data :
        result.append(road["cv_coord"])

    return result
