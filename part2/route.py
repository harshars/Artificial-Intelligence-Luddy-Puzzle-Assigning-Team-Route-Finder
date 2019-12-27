#!/usr/local/bin/python3
#
# route.py : Road trip - Finding the route based on optimal distance, mpg, time or segment
#
# Code by: [Harsha Raja Shivakumar | Maithreyi Manur Narasimha Prabhu | Sunny Bhati]
#


import sys
import heapq

def successors(start_city):
	#next_city = final_data[final_data["city1"]==start_city]

	next_city = final_data[start_city]
	#print(next_city[0][0])
	#print(next_city)

	resultant_next_city = []
	for i in range(len(next_city)):
		speed = int(next_city[i][2])
		resultant_next_city.append((next_city[i][0], next_city[i][1],\
			int(next_city[i][1])/int(next_city[i][2]), int(next_city[i][1])/(400*speed/150*pow((1- (speed/150)),4))))

	return list(set(resultant_next_city))



def parse_data(filename):
    with open(filename, "r") as f:
        return([line for line in f.read().split("\n")])

data = parse_data("road-segments.txt")


#print(len(data))
final_data = {}
for i in range(0, len(data)-1):
	temp = data[i].split()
	# Key = start city, value1 = city2, value2 = distance, value3 = speed_limit
	if temp[0] in final_data:
		final_data[temp[0]].append([temp[1], temp[2], temp[3]])
	else:
		final_data[temp[0]] = [[temp[1], temp[2], temp[3]]]

	if temp[1] in final_data:
		final_data[temp[1]].append([temp[0], temp[2], temp[3]])
	else:
		final_data[temp[1]] = [[temp[0], temp[2], temp[3]]]

	#final_data.setdefault(temp[0], []).append([temp[1], temp[2], temp[3]])
	#final_data.update({temp[1] : [temp[0], temp[2], temp[3]]

#final_data = pd.DataFrame({"city1" : city1, "city2" : city2, "distance" : distance, "speed_limit" : speed_limit})

def mpg(velocity):
	return 400*velocity*pow(1-(velocity/150), 4)/150

def solve():

	start_city = sys.argv[1]
	end_city = sys.argv[2]
	cost_function = sys.argv[3]
	heap = []
	visited_cities = []
	visited_cities.append(start_city)

	if (cost_function == "segments"):
		heapq.heappush(heap, (0, start_city, start_city, 0, 0, 0))

		while (len(heap) > 0):
			(segment, start_city, path, distance, time, mpg) = heapq.heappop(heap)
			#print(start_city, "\n")

			for (cities, distance1, time1, mpg1) in successors(start_city):
				if cities == end_city:
					result = (segment+1, cities, path + " " + cities, distance+int(distance1) , round(time+float(time1), 4), round(mpg+mpg1,4))
					return result
				else:
					if cities not in visited_cities:
						heapq.heappush(heap, (segment+1, cities, path + " " + cities, distance+int(distance1) , round(time+float(time1),4), mpg+mpg1))
						visited_cities.append(cities)

	elif (cost_function == "distance"):
		heapq.heappush(heap, (0, start_city, start_city, 0, 0, 0))

		while (len(heap) > 0):
			(distance, start_city, path, segment, time, mpg) = heapq.heappop(heap)

			for (cities, distance1, time1, mpg1) in successors(start_city):
				if cities == end_city:
					result = (segment+1, cities, path + " " + cities, distance+int(distance1) , round(time+float(time1), 4), round(mpg+mpg1,4))
					return result
				else:
					if cities not in visited_cities:
						heapq.heappush(heap, (distance+int(distance1), cities, path + " " + cities, segment+1 , round(time+float(time1),4), mpg+mpg1))
						visited_cities.append(cities)

	elif (cost_function == "time"):
		heapq.heappush(heap, (0, start_city, start_city, 0, 0, 0))

		while (len(heap) > 0):
			(time, start_city, path, segment, distance, mpg) = heapq.heappop(heap)

			for (cities, distance1, time1, mpg1) in successors(start_city):
				if cities == end_city:
					result = (segment+1, cities, path + " " + cities, distance+int(distance1) , round(time+float(time1), 4), round(mpg+mpg1,4))
					return result
				else:
					if cities not in visited_cities:
						heapq.heappush(heap, (round(time+float(time1),4), cities, path + " " + cities, segment+1 , distance+int(distance1), mpg+mpg1))
						visited_cities.append(cities)

	elif (cost_function == "mpg"):
		heapq.heappush(heap, (0, start_city, start_city, 0, 0, 0))

		while (len(heap) > 0):
			(mpg, start_city, path, segment, distance, time) = heapq.heappop(heap)

			for (cities, distance1, time1, mpg1) in successors(start_city):
				if cities == end_city:
					result = (segment+1, cities, path + " " + cities, distance+int(distance1) , round(time+float(time1), 4), round(mpg+mpg1,4))
					return result
				else:
					if cities not in visited_cities:
						heapq.heappush(heap, (mpg+mpg1, cities, path + " " + cities, segment+1 , distance+int(distance1), round(time+float(time1),4)))
						visited_cities.append(cities)



if __name__ == "__main__":
	#tic = time.time()
	final = solve()
	#toc = time.time()
	if final:
		print('%d %d %f %f %s' % (final[0], final[3], final[4], final[5], final[2]))
		#print(final[0], " ", int(final[3]), " ", final[4], " ", final[5], " ", final[2])
	else:
		print("Inf")
	#print(toc - tic)

	

	


