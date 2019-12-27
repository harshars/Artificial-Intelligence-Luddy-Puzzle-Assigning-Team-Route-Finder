#!/usr/local/bin/python3

# put your routing program here!

import pandas as pd
import sys
import heapq

def successors(start_city):
	next_city = final_data[final_data["city1"]==start_city]

	resultant_next_city = []
	for i in range(next_city.shape[0]):
		speed = int(next_city.iloc[i]["speed_limit"])
		resultant_next_city.append((next_city.iloc[i]["city2"], next_city.iloc[i]["distance"],\
			int(next_city.iloc[i]["distance"])/int(next_city.iloc[i]["speed_limit"]), int(next_city.iloc[i]["distance"])/(400*speed/150*pow((1- (speed/150)),4))))

	next_city_opp = final_data[final_data["city2"]==start_city]
	for i in range(next_city_opp.shape[0]):
		speed = int(next_city_opp.iloc[i]["speed_limit"])
		resultant_next_city.append((next_city_opp.iloc[i]["city1"], next_city_opp.iloc[i]["distance"],\
			int(next_city_opp.iloc[i]["distance"])/int(next_city_opp.iloc[i]["speed_limit"]), int(next_city_opp.iloc[i]["distance"])/(400*speed/150*pow((1- (speed/150)),4))))

	return list(set(resultant_next_city))



def parse_data(filename):
    with open(filename, "r") as f:
        return([line for line in f.read().split("\n")])

data = parse_data("road-segments.txt")

city1 = []
city2 = []
distance = []
speed_limit = []

for i in range(0, len(data)-1):
	temp = data[i].split()
	city1.append(temp[0])
	city2.append(temp[1])
	distance.append(temp[2])
	speed_limit.append(temp[3])


final_data = pd.DataFrame({"city1" : city1, "city2" : city2, "distance" : distance, "speed_limit" : speed_limit})

def mpg(velocity):
	return 400*velocity*pow(1-(velocity/150), 4)/150

def solve():

	start_city = sys.argv[1]
	end_city = sys.argv[2]
	cost_function = sys.argv[3]
	heap = []

	if (cost_function == "segment"):
		heapq.heappush(heap, (0, start_city, start_city, 0, 0, 0))

		while (len(heap) > 0):
			print(heap)
			(segment, start_city, path, distance, time, mpg) = heapq.heappop(heap)

			for (cities, distance1, time1, mpg1) in successors(start_city):
				if cities == end_city:
					result = (segment+1, cities, path + " " + cities, distance+int(distance1) , round(time+float(time1), 4), round(mpg+mpg1,4))
					return result
				else:
					heapq.heappush(heap, (segment+1, cities, path + " " + cities, distance+int(distance1) , round(time+float(time1),4), mpg+mpg1))

	elif (cost_function == "distance"):
		heapq.heappush(heap, (0, start_city, start_city, 0, 0, 0))

		while (len(heap) > 0):
			(distance, start_city, path, segment, time, mpg) = heapq.heappop(heap)

			for (cities, distance1, time1, mpg1) in successors(start_city):
				if cities == end_city:
					result = (segment+1, cities, path + " " + cities, distance+int(distance1) , round(time+float(time1), 4), round(mpg+mpg1,4))
					return result
				else:
					heapq.heappush(heap, (distance+int(distance1), cities, path + " " + cities, segment+1 , round(time+float(time1),4), mpg+mpg1))

	elif (cost_function == "time"):
		heapq.heappush(heap, (0, start_city, start_city, 0, 0, 0))

		while (len(heap) > 0):
			(time, start_city, path, segment, distance, mpg) = heapq.heappop(heap)

			for (cities, distance1, time1, mpg1) in successors(start_city):
				if cities == end_city:
					result = (segment+1, cities, path + " " + cities, distance+int(distance1) , round(time+float(time1), 4), round(mpg+mpg1,4))
					return result
				else:
					heapq.heappush(heap, (round(time+float(time1),4), cities, path + " " + cities, segment+1 , distance+int(distance1), mpg+mpg1))

	elif (cost_function == "mpg"):
		heapq.heappush(heap, (0, start_city, start_city, 0, 0, 0))

		while (len(heap) > 0):
			(mpg, start_city, path, segment, distance, time) = heapq.heappop(heap)

			for (cities, distance1, time1, mpg1) in successors(start_city):
				if cities == end_city:
					result = (segment+1, cities, path + " " + cities, distance+int(distance1) , round(time+float(time1), 4), round(mpg+mpg1,4))
					return result
				else:
					heapq.heappush(heap, (mpg+mpg1, cities, path + " " + cities, segment+1 , distance+int(distance1), round(time+float(time1),4)))



if __name__ == "__main__":
	final = solve()
	print(final[0], " ", final[3], " ", final[4], " ", final[5], " ", final[2])

	

	


