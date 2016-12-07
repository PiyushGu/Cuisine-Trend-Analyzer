import json
from datetime import datetime
import numpy as np

def get_scores(businesses, reviews):
    if not businesses:
        return {'None':0}
    cuisine_score_map = {}
    CUISINES = ["American (New)", "American (Traditional)", "British", "Caribbean", "Chinese", \
            "French", "Greek", "Indian", "Italian", "Japanese", "Mediterranean", "Mexican", \
            "Moroccan", "Spanish", "Thai", "Turkish", "Vietnamese"]
    RATING_THRESHOLD = 5
    for cuisine in CUISINES:
        cuisine_score_map[cuisine] = None
        for business in businesses:
            if cuisine in business["categories"]:
                business_reviews = reviews[business["business_id"]]
                counter = 0
                score = 0
                if len(business_reviews) > RATING_THRESHOLD:
                    for review in business_reviews:
                        if review["text"].strip() != "":
                            score += review["sentiment"]
                            counter += 1
                        #cuisine_score_map[cuisine]+=review["stars"]
                    if counter != 0:
                        cuisine_score_map[cuisine] = float(score)/counter
    return cuisine_score_map

def get_data(filename):
	with open(filename) as f:
		return json.load(f)

def in_area_range(data, minlat,minlong,maxlat,maxlong):
	latitude = data['latitude']
	longitude = data['longitude']
	return latitude >= minlat and longitude >= minlong and latitude <= maxlat and longitude <= maxlong

def in_time_range(data,begin_year,end_year):
	year = datetime.strptime(data['date'], '%Y-%m-%d').year
	return year >= int(begin_year) and year<= int(end_year)

def get_latlong_steps(minlat,minlong,maxlat,maxlong):
	latdiff = (maxlat-minlat)/3.0
	longdiff = (maxlong-minlong)/3.0
	latranges = [(i,i+latdiff) for i in np.arange(minlat,maxlat,latdiff)]
	longranges = [(i,i+longdiff) for i in np.arange(minlong,maxlong,longdiff)]
	return [(lat[0],lon[0],lat[1],lon[1],(lat[0]+lat[1])/2,(lon[0]+lon[1])/2) for lat in latranges for lon in longranges]

def get_business_reviews_regionwise(minlat,minlong,maxlat,maxlong,centerlat,centerlong,begintime,endtime,business,reviews):
	business = filter(lambda data:in_area_range(data,minlat,minlong,maxlat,maxlong),business)
	business_ids = [data['business_id'] for data in business]
	print len(business_ids)
	reviews_map = dict([(k,filter(lambda data:in_time_range(data,begintime,endtime),reviews[k])) for k in business_ids])
	return business,reviews_map,centerlat,centerlong

def get_dict(maxkey,d):
	return [('cuisine',maxkey),('score',d[maxkey])]

def get_business(minlat,minlong,maxlat,maxlong,begintime,endtime,business,reviews_map):

	business = filter(lambda data:in_area_range(data,minlat,minlong,maxlat,maxlong),business)
	business_ids = [data['business_id'] for data in business]
	#reviews_map = get_data("data/reviews_map.json")
	reviews = dict([(bid,reviews_map[bid]) for bid in business_ids])
	print len(reviews)
	business_reviews = [get_business_reviews_regionwise(x[0],x[1],x[2],x[3],x[4],x[5],begintime,endtime,business,reviews) for x in get_latlong_steps(minlat,minlong,maxlat,maxlong)]
	scores = [(get_scores(b,r),[('center_lat',clat),('center_long',clong),('businesses',b)]) for b,r,clat,clong in business_reviews]
	result = [dict(get_dict(max(score_map,key=lambda x:score_map[x]),score_map)+center) for score_map,center in scores]
	print result
	return json.dumps(result)	

if __name__ == "__main__":
	#business = filter(lambda data:in_area_range(data,40,-80,50,-112),get_data("data/businesses.json"))
	#reviews = filter(lambda data:in_time_range(data,'2011-01-01','2012-01-01'),get_data("data/reviews.json"))
	#print reviews[0]
	'''
	minlat= 40
	maxlat=50
	minlong=-112
	maxlong=-80
	latdiff = (maxlat-minlat)/3.0
	longdiff = (maxlong-minlong)/3.0
	latranges = [(i,i+latdiff) for i in np.arange(minlat,maxlat,latdiff)]
	longranges = [(i,i+longdiff) for i in np.arange(minlong,maxlong,longdiff)]
	print [(lat[0],lon[0],lat[1],lon[1]) for lat in latranges for lon in longranges]
	'''
	get_business(32,-124,41,-114,'2000','2020',get_data("data/businesses.json"),get_data("data/reviews_map.json"))
