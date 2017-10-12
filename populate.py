from DyReTra.models.trafficCluster import TrafficCluster

if __name__ == "__main__":
    t = TrafficCluster()
    t.create({
    	'coordinates': {
    		'long': 12.979268, 'lat': 77.602457
    	},
    	'cluster_id': 123456,
    	'roads': [
    		{
    			"road_id": "r1",
            	"approach_fl": 1,
            	"slope": 1.2564997159795548,
            	"cv_coord": [],
            	"traffic_signal": {
            		"id": "tl1"
            	}
    		},
    		{
    			"road_id": "r2",
            	"approach_fl": 1,
            	"slope": -1.943558811423054,
            	"cv_coord": [],
            	"traffic_signal": {
            		"id": "tl2"
            	}
    		},
    		{
    			"road_id": "r3",
            	"approach_fl": 1,
            	"slope": 2.891439025559257,
            	"cv_coord": [],
            	"traffic_signal": {
            		"id": "tl3"
            	}
    		},
    		{
    			"road_id": "r4",
            	"approach_fl": 1,
            	"slope": -0.2788820981381136,
            	"cv_coord": [],
            	"traffic_signal": {
            		"id": "tl4"
            	}
    		},
    		{
    			"road_id": "r4",
            	"approach_fl":0,
            	"slope": None,
            	"cv_coord": [],
            	"traffic_signal": {
            		"id": "tl4"
            	}
    		}
    	]
    })
