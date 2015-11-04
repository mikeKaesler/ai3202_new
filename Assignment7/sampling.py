#mike kaesler
#assignment 7, sampling


samples = [0.82,	0.56,	0.08,	0.81,	0.34,	0.22,	0.37,	0.99,	0.55,	0.61,	0.31,	0.66,	0.28,	1.0,	0.95,	
0.71,	0.14,	0.1,	1.0,	0.71,	0.1,	0.6,	0.64,	0.73,	0.39,	0.03,	0.99,	1.0,	0.97,	0.54,	0.8,	0.97,	
0.07,	0.69,	0.43,	0.29,	0.61,	0.03,	0.13,	0.14,	0.13,	0.4,	0.94,	0.19, 0.6,	0.68,	0.36,	0.67,	
0.12,	0.38,	0.42,	0.81,	0.0,	0.2,	0.85,	0.01,	0.55,	0.3,	0.3,	0.11,	0.83,	0.96,	0.41,	0.65,	
0.29,	0.4,	0.54,	0.23,	0.74,	0.65,	0.38,	0.41,	0.82,	0.08,	0.39,	0.97,	0.95,	0.01,	0.62,	0.32,	
0.56,	0.68,	0.32,	0.27,	0.77,	0.74,	0.79,	0.11,	0.29,	0.69,	0.99,	0.79,	0.21,	0.2,	0.43,	0.81,	
0.9,	0.0,	0.91,	0.01]


#splice every 4th element starting at 
cloudy = samples[::4] #index 0    all the samples used to determine if cloudy
sprinkler = samples[1::4] #index1  " " sprinkler on
rain = samples[2::4] #index 2  " " its raining
wet_grass = samples[3::4] #index 3   " " if the grass is wet
# index 0 of each list is the first sample, index 1 of each list is the second sample, etc. 

#check, correct
#print cloudy
#checking can spetrate samples like this, okay
#for i in xrange(len(cloudy)):
#	print "Sample", i, "'s probabilites are :", cloudy[i]," ", sprinkler[i]," ", rain[i], " ", wet_grass[i]

#create seperate, empty lists for each variable. With each sample denoted by index,
#a 0 at that particular index indicates - or not and a 1 indicates a + or positive
cloudy_bin = []
sprinkler_bin = []
rain_bin = []
wet_grass_bin = []


for i in xrange(len(cloudy)):
	if (cloudy[i] < 0.5): #cloudy is true
		cloudy_bin.append(1)
		if (sprinkler[i] < 0.1 and rain[i] < 0.8): #cloudy is true and sprinkler is true and rain is true
			sprinkler_bin.append(1)
			rain_bin.append(1)
			if (wet_grass[i] < 0.99): #s=t r=t w=t
				wet_grass_bin.append(1)
			else: #w=f
				wet_grass_bin.append(0)
		elif (sprinkler[i] < 0.1 and rain[i] >= 0.8): #cloudy is true and sprinkler is true and rain is false
			sprinkler_bin.append(1)
			rain_bin.append(0)
			if (wet_grass[i] < 0.9): #s=t r=f w=t
				wet_grass_bin.append(1)
			else: #s=t r=f w=f
				wet_grass_bin.append(0)
		elif (sprinkler[i] >= 0.1 and rain[i] < 0.8): #cloudy is true and sprinkler is false and rain is true
			sprinkler_bin.append(0)
			rain_bin.append(1)
			if (wet_grass[i] < 0.9): #s=f r=t w=t
				wet_grass_bin.append(1)
			else: #s=f r=t w=f
				wet_grass_bin.append(0)
		else: #cloudy is true and sprinkler is false and rain is false
			sprinkler_bin.append(0)
			rain_bin.append(0)
			if (wet_grass[i] < 0): #s=f r=f w=t
				wet_grass_bin.append(1)
			else: #s=f r=f w=f
				wet_grass_bin.append(0)
	else: #cloudy is false
		cloudy_bin.append(0)
		if (sprinkler[i] < 0.5 and rain[i] < 0.2): #cloudy is false and sprinkler is true and rain is true
			sprinkler_bin.append(1)
			rain_bin.append(1)
			if (wet_grass[i] < 0.99): #s=t r=t w=t
				wet_grass_bin.append(1)
			else: #w=f
				wet_grass_bin.append(0)
		elif (sprinkler[i] < 0.5 and rain[i] >= 0.2): #cloudy is false and sprinkler is true and rain is false
			sprinkler_bin.append(1)
			rain_bin.append(0)
			if (wet_grass[i] < 0.9): #s=t r=f w=t
				wet_grass_bin.append(1)
			else: #s=t r=f w=f
				wet_grass_bin.append(0)
		elif (sprinkler[i] >= 0.5 and rain[i] < 0.2): #cloudy is false and sprinkler is false and rain is true
			sprinkler_bin.append(0)
			rain_bin.append(1)
			if (wet_grass[i] < 0.9): #s=f r=t w=t
				wet_grass_bin.append(1)
			else: #s=f r=t w=f
				wet_grass_bin.append(0)
		else: #cloudy is false and sprinkler is false and rain is false
			sprinkler_bin.append(0)
			rain_bin.append(0)
			if (wet_grass[i] < 0): #s=f r=f w=t
				wet_grass_bin.append(1)
			else: #s=f r=f w=f
				wet_grass_bin.append(0)
		
print "cloudy bin is :", cloudy_bin
print "sprinkler bin is :", sprinkler_bin
print "rain bin is :", rain_bin
print "wet grass bin is :", wet_grass_bin
	
denominator = 0
numerator = 0
for i in xrange(len(cloudy_bin)):
	if (rain_bin[i] == 1):
		denominator += 1
	if (rain_bin[i] ==1 and cloudy_bin[i] ==1):
		numerator += 1

print "prob cloudy is true given rain is true"		
print numerator
print denominator

denominator1 = 0
numerator1 = 0
for i in xrange(len(cloudy_bin)):
	if (wet_grass_bin[i] == 1):
		denominator1 += 1
	if (wet_grass_bin[i] ==1 and sprinkler_bin[i] ==1):
		numerator1 += 1
	
print "sprinkler is true given wet grass is true"
print numerator1
print denominator1

denominator2 = 0
numerator2 = 0
for i in xrange(len(cloudy_bin)):
	if (wet_grass_bin[i] == 1 and cloudy_bin[i] == 1):
		denominator2 += 1
	if (wet_grass_bin[i] ==1 and sprinkler_bin[i] ==1 and cloudy_bin[i] == 1):
		numerator2 += 1

print "sprinkler is true given cloudy is true and wet grass is true"
print numerator2
print denominator2
	

