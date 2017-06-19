#NOTE - these calculations are using the entire 2017 crime collection and a user in the middle of Chicago - for our app's purposes, the crime input would be every crime within the user's screen - if you try to change the user inputs outside of the area of the map, it will not work properly


import json
import math
#Load up the JSON file containing the crime data
dataFile = open('data_sorted_by_type.json')
#Load the data from the JSON format
jsonData = json.load(dataFile)

types = ['HOMICIDE', 'BURGLARY', 'THEFT', 'DECEPTIVE PRACTICE', 'CRIMINAL DAMAGE', 'BATTERY', 'CRIMINAL TRESPASS', 'OTHER OFFENSE', 'ASSAULT', 'STALKING', 'OFFENSE INVOLVING CHILDREN', 'MOTOR VEHICLE THEFT', 'ROBBERY', 'CONCEALED CARRY LICENSE VIOLATION', 'NARCOTICS', 'SEX OFFENSE', 'WEAPONS VIOLATION', 'LIQUOR LAW VIOLATION', 'CRIM SEXUAL ASSAULT', 'PROSTITUTION', 'PUBLIC PEACE VIOLATION', 'INTERFERENCE WITH PUBLIC OFFICER', 'GAMBLING', 'ARSON', 'KIDNAPPING', 'INTIMIDATION', 'OBSCENITY',
			'NON-CRIMINAL', 'HUMAN TRAFFICKING', 'NON-CRIMINAL (SUBJECT SPECIFIED)', 'PUBLIC INDECENCY']

#4 dimensional euclidean distance function
def euclid_dist4d(user, average):
	answer = math.sqrt((user[0]-average[0])**2 + (user[1]-average[1])**2 + (user[2]-average[2])**2 + (user[3]-average[3])**2)
	return answer

allCounts = []
#create an array with all the counts of each type of crimes
for type_of_crime, crimes in jsonData.items():
	count = len(crimes)
	allCounts.append(count)

#set a scale for the count
minCount = min(allCounts)
maxCount = max(allCounts)
scaleCount = (maxCount-minCount)/100

collectiveAverages = []

typeIndex = 0
#iterating through each type of crime
for type_of_crime, crimes in jsonData.items():
	latitude = 0 #setting the initial variables to 0, but will later on find the average value by dividing it (after all of the variable values have been added) by the length of the crime count in each type
	longitude = 0
	clockStamp = 0

	avg = [] #creating a temporary array that holds the raw average values of lat, long, time, and count for each type of crime so that they can be referenced later

	for i in crimes:
		latitude += i['lat']
		longitude += i['long']
		clockStamp += i['clockStamp']
	avg.append(abs(latitude)/allCounts[typeIndex])
	avg.append(abs(longitude)/allCounts[typeIndex])
	avg.append(clockStamp/allCounts[typeIndex])
	avg.append((allCounts[typeIndex]-minCount)/scaleCount)
	typeIndex +=1 #incrementing the index so that the correct count is used in calculation
	collectiveAverages.append(avg) #this array holds the raw averages for every type of crime - next step is to scale them properly!

#work with average values here outside of the main loop - variables are set to extreme values so that they can be replaced with the real maximum and minimum
maxLat = 0
maxLong=0
maxClockStamp = 0
minLat = 100000000
minLong = 100000000
minClockStamp = 100000000

#finding the maximum and minimum
for i in collectiveAverages:
	if abs(i[0]) > maxLat:
		maxLat = abs(i[0])
	if abs(i[1]) > maxLong:
		maxLong = abs(i[1])
	if abs(i[2]) > maxClockStamp:
		maxClockStamp = abs(i[2])
	if abs(i[0]) < minLat:
		minLat = abs(i[0])
	if abs(i[1]) < minLong:
		minLong = abs(i[1])
	if abs(i[2]) < minClockStamp:
		minClockStamp = abs(i[2])

#determinining scale for each variable - basically, converting everything onto a scale from 0 to 100 (count has already been scaled)
scaleLat = (maxLat-minLat)/100
scaleLong = (maxLong - minLong)/100
scaleClockStamp = (maxClockStamp - minClockStamp)/100
for average in collectiveAverages:
	average[0] = ((average[0]-minLat)/scaleLat)
	average[1] = ((average[1]-minLong)/scaleLong)
	average[2] = ((average[2]-minClockStamp)/scaleClockStamp)

#IMPORTANT - when using the app, the crime list generated will be dependent on the location of the user and the area of map that the user is looking at - therefore, for testing purposes, the testuser latitude and longitude will always be within the maximum and minumum values of the crimes
testuser = []
testuser.append((maxLat+minLat)/2)
testuser.append((maxLong+minLong)/2)
testuser.append(40000)
testuser.append(100)

#adjust the user's inputs to the scales established earlier (count is equal too 100 because the larger counts for each type of crime will be 100, and therefore the closest to the user, whereas the smallest count is 0, and furthest from the user)
testuser[0] = (testuser[0]-minLat)/scaleLat
testuser[1] = (testuser[1]-minLong)/scaleLong
testuser[2] = (testuser[2]-minClockStamp)/scaleClockStamp

#creating an array for all of the distances from the user's point to the average,scaled point of each type of crime
euclidean_distance = []

#appending the euclidean distances to the array
for i in collectiveAverages:
	euclidean_distance.append(euclid_dist4d(testuser,i))

print (types[euclidean_distance.index(min(euclidean_distance))]) #printing the type of crime closest to the user's values using index values
