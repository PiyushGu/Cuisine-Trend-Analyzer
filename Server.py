from bottle import route, run, debug, template, request, static_file, error, response
from api import get_business,get_data

@route('/:filename#.*#')
def send_static(filename):
    return static_file(filename, root='resources/public')


@route('/area/<minlat>/<minlong>/<maxlat>/<maxlong>/<begintime>/<endtime>')
def area(minlat,minlong,maxlat,maxlong,begintime,endtime,business,reviews_map):
	return get_business(minlat,minlong,maxlat,maxlong,begintime,endtime,business,reviews_map)
	

@error(403)
def mistake403(code):
	return 'There is a mistake in your url!'

@error(404)
def mistake404(code):
	return 'Sorry, this page does not exist!'

def main_fn():
	run(host="10.123.80.87", port=8080)
	
if __name__ == "__main__":
	business = get_data("data/businesses.json")
	reviews_map = get_data("data/reviews_map.json")
	main_fn()
