#Mike Kaesler
#Assignment 6
import networkx as nx
import matplotlib.pyplot as plt
import getopt
import sys

#create bayes net as graph using networkx (directed graph)
#then create all 5 nodes 
Bayes = nx.DiGraph()
#global Bayes                           maybe not
Bayes.add_node("P")  #Pollution node
Bayes.add_node("S")  #Smoker node
Bayes.add_node("C")  #Cancer node
Bayes.add_node("X")  #Xray node
Bayes.add_node("D")  #Dyspnoa node

#create edges in graph according to handout we were given
Bayes.add_edges_from([("P", "C"), ("S", "C"), 
						("C", "X"), ("C", "D")])

#definging starting probablities below. Updated from last version,
#making names more intutitive, if statements will work the control from the cline in the functions 
 
Bayes.node["P"]["p"] = .9 #prior probablity for pollution, LOW
Bayes.node["S"]["s"] = 0.3 #prior hard coded prob Smoker is TRUE


#probability priors are high or false
Bayes.node["P"]["~p"] = 1 - Bayes.node["P"]["p"] #prob pollution is HIGH
Bayes.node["S"]["~s"] = 1 - Bayes.node["S"]["s"] #prob somker is FALSE

#conditional probablities for having Cancer
Bayes.node["C"]["ps"] = 0.03 #pollution low, smoker true
Bayes.node["C"]["p~s"] = 0.001 #pollution low, smoker false
Bayes.node["C"]["~ps"] = 0.05 #pollution high, smoker true
Bayes.node["C"]["~p~s"] = 0.02 #pollution high, smoker false

Bayes.node["X"]["xc"] = 0.9 #xray is true given cancer is true
Bayes.node["X"]["x~c"] = 0.2 #xray is true given cancer is false

Bayes.node["D"]["dc"] = 0.65 #dys is true given cancer is true
Bayes.node["D"]["d~c"] = 0.3 #dis is true given cancer is false


#calculate priors
def setPrior(a, f):
	if (a == "P"):
		Bayes.node["P"]["p"] = f
		Bayes.node["P"]["~p"] = 1 - f
		print "probability pollution is low set at", Bayes.node["P"]["p"]
		
	elif (a == "S"):
		Bayes.node["S"]["s"] = f
		Bayes.node["S"]["~s"] = 1 - f
		print "probablility smoker is true is set at", Bayes.node["S"]["s"]
		 
	else:
		print "not valid argument"

#calculate marginal probabilities
def calcMarginal(a):
	if (a == "S"):
		marginal = Bayes.node["S"]["s"]
		return marginal
	if (a == "~s"):
		marginal = Bayes.node["S"]["~s"] 
		return marginal
	if (a == "P"):
		marginal = Bayes.node["P"]["p"]
		return marginal
	if (a == "~p"):
		marginal = Bayes.node["P"]["~p"]
		return marginal
	if (a == "C"):
		marginal = ((Bayes.node["C"]["ps"]*Bayes.node["S"]["s"] * Bayes.node["P"]["p"]) + (Bayes.node["C"]["p~s"]*Bayes.node["P"]["p"]*
		Bayes.node["S"]["~s"]) + (Bayes.node["C"]["~p~s"] * Bayes.node["P"]["~p"] * Bayes.node["S"]["~s"]) + (Bayes.node["C"]["~ps"] *
		Bayes.node["P"]["~p"]*Bayes.node["S"]["s"]))
		return marginal
	if (a == "~c"):
		marginal = 1 - calcMarginal("C") 
		return marginal
	if (a == "X"):
		marginal = (Bayes.node["X"]["xc"]*calcMarginal("C")) + (Bayes.node["X"]["x~c"]* (1 - calcMarginal("C")))
		return marginal
	if (a == "~x"):
		marginal = 1 - calcMarginal("X")
		return marginal
	if (a == "D"):
		marginal = (Bayes.node["D"]["dc"]*calcMarginal("C")) + (Bayes.node["D"]["d~c"]*(1 - calcMarginal("C")))
		return marginal
	if (a == "~d"):
		marginal = 1 - calcMarginal("D")


def calcConditional(n):
	p = n.find("/")
	#print "left side", n[:p]
	#print "right side", n[p+1:]
	
	#left side of "/", can only ever be one argument
	left = n[:p]
	#right side of "/", can either be one or two arguments
	right = n[p+1:]
	
	if len(right) == 1:
		#getting the conditonal given that particular case is itself
		if (left == right):
			conditional = 1.0
			return conditional
		
		#predictive cases    
		if (left == "x"): # x = pos 
			if (right[0] == "s"): # given smoker = true     P(X=POS|S=TRUE)
				conditional = ((Bayes.node["X"]["xc"]*Bayes.node["C"]["ps"]*calcMarginal("S")*
				calcMarginal("P"))+(Bayes.node["X"]["xc"]*Bayes.node["C"]["~ps"]*calcMarginal("S")
				*calcMarginal("~p")) + (Bayes.node["X"]["x~c"]*(1 - Bayes.node["C"]["~ps"])*calcMarginal("~p")
				*calcMarginal("S")) + (Bayes.node["X"]["x~c"]*(1- Bayes.node["C"]["ps"])*calcMarginal("P")*
				calcMarginal("S")))/((Bayes.node["C"]["ps"]*calcMarginal("P")*calcMarginal("S")) + (Bayes.node["C"]["~ps"]*calcMarginal("S")
				*calcMarginal("~p")) + ((1- Bayes.node["C"]["ps"])*calcMarginal("P")*
				calcMarginal("S")) + ((1 - Bayes.node["C"]["~ps"])*calcMarginal("~p")
				*calcMarginal("S")))
				return conditional
		if (left == "~p"): #pol is high given smoker
			if (right[0] == "s"):
				conditional = Bayes.node["P"]["~p"]
				return conditional
		if (left == "c"): #cancer true given somker
			if (right[0] == "s"):
				conditional = ((Bayes.node["C"]["ps"]*calcMarginal("P")*calcMarginal("S"))+(Bayes.node["C"]["~ps"]
				*calcMarginal("~p")*calcMarginal("S")))/calcMarginal("S")
				return conditional
		if (left == "d"): #dys true given smoker
			if (right[0] == "s"):
				conditional = ((Bayes.node["D"]["dc"]*Bayes.node["C"]["ps"]*calcMarginal("S")*
				calcMarginal("P"))+(Bayes.node["D"]["dc"]*Bayes.node["C"]["~ps"]*calcMarginal("S")
				*calcMarginal("~p")) + (Bayes.node["D"]["d~c"]*(1 - Bayes.node["C"]["~ps"])*calcMarginal("~p")
				*calcMarginal("S")) + (Bayes.node["D"]["d~c"]*(1- Bayes.node["C"]["ps"])*calcMarginal("P")*
				calcMarginal("S")))/((Bayes.node["C"]["ps"]*calcMarginal("P")*calcMarginal("S")) + (Bayes.node["C"]["~ps"]*calcMarginal("S")
				*calcMarginal("~p")) + ((1- Bayes.node["C"]["ps"])*calcMarginal("P")*
				calcMarginal("S")) + ((1 - Bayes.node["C"]["~ps"])*calcMarginal("~p")
				*calcMarginal("S")))
				return conditional
		
		#diagnostic case    DONE
		if (left == "~p"): #pollution is high given dys
			if (right[0] == "d"):
				conditional = ((((Bayes.node["D"]["dc"]*Bayes.node["C"]["~ps"]*calcMarginal("~p") *
				calcMarginal("S"))+(Bayes.node["D"]["dc"]*Bayes.node["C"]["~p~s"]*calcMarginal("~p")
				*calcMarginal("~s")) + (Bayes.node["D"]["d~c"]*(1-Bayes.node["C"]["~ps"])*calcMarginal("~p")*
				calcMarginal("S"))+(Bayes.node["D"]["d~c"]*(1-Bayes.node["C"]["~p~s"])*calcMarginal("~p")*calcMarginal("~s"))
				)/((Bayes.node["C"]["~p~s"]*calcMarginal("~p")*calcMarginal("~s"))+ (
				Bayes.node["C"]["~ps"]*calcMarginal("~p") *calcMarginal("S"))+((1-Bayes.node["C"]["~ps"])*calcMarginal("~p")
				*calcMarginal("S"))+((1-Bayes.node["C"]["~p~s"])*calcMarginal("~p")*calcMarginal("~s"))))*(calcMarginal("~p")/calcMarginal("D")))
				return conditional
		if (left == "s"):
			if (right[0] == "d"): #smoker is true given dys is true
				conditional = ((((Bayes.node["D"]["dc"]*Bayes.node["C"]["ps"]*calcMarginal("P") *
				calcMarginal("S"))+(Bayes.node["D"]["dc"]*Bayes.node["C"]["~ps"]*calcMarginal("~p")
				*calcMarginal("S")) + (Bayes.node["D"]["d~c"]*(1-Bayes.node["C"]["ps"])*calcMarginal("P")*
				calcMarginal("S"))+(Bayes.node["D"]["d~c"]*(1-Bayes.node["C"]["~ps"])*calcMarginal("~p")*calcMarginal("S"))
				)/((Bayes.node["C"]["ps"]*calcMarginal("P")*calcMarginal("S"))+ (
				Bayes.node["C"]["~ps"]*calcMarginal("~p") *calcMarginal("S"))+((1-Bayes.node["C"]["~ps"])*calcMarginal("~p")
				*calcMarginal("S"))+((1-Bayes.node["C"]["ps"])*calcMarginal("P")*calcMarginal("S"))))*(calcMarginal("S")/calcMarginal("D")))
				return conditional
		if (left == "c"):
			if (right[0] == "d"): #cancer is true given dys is true
				conditional = (Bayes.node["D"]["dc"]*calcMarginal("C"))/calcMarginal("D")
				return conditional
		if (left == "x"):  #xray is pos given dys
			if (right[0] == "d"):
				conditional = ((Bayes.node["X"]["xc"]*calcMarginal("C")*Bayes.node["D"]["dc"])
				+ (Bayes.node["X"]["x~c"]*calcMarginal("~c")*Bayes.node["D"]["d~c"]))/calcMarginal("D")
				return conditional
		
		#intercausal C=T
		if (left == "~p"):
			if (right[0] == "c"):
				conditional = ((Bayes.node["C"]["~ps"]*calcMarginal("~p")*calcMarginal("S") +
				(Bayes.node["C"]["~p~s"]*calcMarginal("~p")*calcMarginal("~s")))/calcMarginal("~p"))*(calcMarginal("~p")/calcMarginal("C"))
				return conditional
		
		if (left == "s"):
			if (right[0] == "c"):
				conditional = ((Bayes.node["C"]["ps"]*calcMarginal("P")*calcMarginal("S") +
				(Bayes.node["C"]["~ps"]*calcMarginal("~p")*calcMarginal("S")))/calcMarginal("S"))*(calcMarginal("S")/calcMarginal("C"))
				return conditional
		if (left == "x"):
			if (right[0] == "c"):
				conditional = Bayes.node["X"]["xc"]
				return conditional
		if (left == "d"):
			if (right[0] == "c"):
				conditional = Bayes.node["D"]["dc"]
				return conditional
	
	if len(right) == 2:
		if (left == right[0] or left == right[1]):
			conditional = 1.0
			return conditional
		
		#intercausal cases
		if (left == "x"):   #prob of x/c=t and s=t 
			if (right[0] == "c" and right[1]== "s"):
				conditional = Bayes.node["X"]["xc"] ## same as, x=t/c=t because c "explains away" s=t
				return conditional
		if (left == "d"): #prob of dys given cancer and smoke are true
			if (right[0] == "c" and right[1] == "s"):
				conditional = Bayes.node["D"]["dc"]
				return conditional
		if (left == "~p"): #prob pol is high given cancser and smoke are true
			if (right[0] == "c" and right[1] == "s"):
				conditional = ((Bayes.node["C"]["~ps"]*calcMarginal("~p")*calcMarginal("S"))/
				((Bayes.node["C"]["~ps"]*calcMarginal("S")*calcMarginal("~p")) + (Bayes.node["C"]["ps"]*
				calcMarginal("S")*calcMarginal("P"))))
				return conditional
		#combined cases   DONE
		if (left == "~p"):
			if (right[0] == "d" and right[1] == "s"): #pollution is high and dys and smoke are true
				conditional = (((Bayes.node["D"]["dc"]*Bayes.node["C"]["~ps"]*calcMarginal("~p")*
				calcMarginal("S"))+(Bayes.node["D"]["d~c"]*(1-Bayes.node["C"]["~ps"])*calcMarginal("~p")*
				calcMarginal("S")))/((Bayes.node["D"]["dc"]*Bayes.node["C"]["~ps"]*calcMarginal("~p")*
				calcMarginal("S"))+(Bayes.node["D"]["dc"]*Bayes.node["C"]["ps"]*calcMarginal("P")*
				calcMarginal("S"))+(Bayes.node["D"]["d~c"]*(1-Bayes.node["C"]["~ps"])*calcMarginal("~p")*
				calcMarginal("S"))+(Bayes.node["D"]["d~c"]*(1-Bayes.node["C"]["ps"])*calcMarginal("P")*
				calcMarginal("S"))))
				return conditional
		
		if (left == "c"):
			if (right[0] == "d" and right[1] == "s"):#cancer is true given dys and smoking is true
				conditional = (((Bayes.node["D"]["dc"]*Bayes.node["C"]["~ps"]*calcMarginal("~p")*
				calcMarginal("S"))+(Bayes.node["D"]["dc"]*Bayes.node["C"]["ps"]*calcMarginal("P")*
				calcMarginal("S")))/((Bayes.node["D"]["dc"]*Bayes.node["C"]["~ps"]*calcMarginal("~p")*
				calcMarginal("S"))+(Bayes.node["D"]["dc"]*Bayes.node["C"]["ps"]*calcMarginal("P")*
				calcMarginal("S"))+(Bayes.node["D"]["d~c"]*(1-Bayes.node["C"]["~ps"])*calcMarginal("~p")*
				calcMarginal("S"))+(Bayes.node["D"]["d~c"]*(1-Bayes.node["C"]["ps"])*calcMarginal("P")*
				calcMarginal("S"))))
				return conditional
		if (left == "x"):
			if (right[0] == "d" and right[1] == "s"): #xray is true given dys and smoker are true
				conditional = (((Bayes.node["X"]["xc"]*Bayes.node["D"]["dc"]*Bayes.node["C"]["~ps"]*
				calcMarginal("~p")*calcMarginal("S")) + (Bayes.node["X"]["x~c"]*Bayes.node["D"]["d~c"]*
				(1-Bayes.node["C"]["~ps"])*calcMarginal("~p")*calcMarginal("S")) + (Bayes.node["X"]["xc"]*
				Bayes.node["D"]["dc"]*Bayes.node["C"]["ps"]*calcMarginal("P")*calcMarginal("S")) + 
				(Bayes.node["X"]["x~c"]*Bayes.node["D"]["d~c"]*(1-Bayes.node["C"]["ps"])*calcMarginal("P")*
				calcMarginal("S")))/((Bayes.node["D"]["dc"]*Bayes.node["C"]["~ps"]*
				calcMarginal("~p")*calcMarginal("S")) + (Bayes.node["D"]["d~c"]*
				(1-Bayes.node["C"]["~ps"])*calcMarginal("~p")*calcMarginal("S")) + (Bayes.node["D"]["dc"]*
				Bayes.node["C"]["ps"]*calcMarginal("P")*calcMarginal("S")) + (Bayes.node["D"]["d~c"]*(1-Bayes.node["C"]["ps"])
				*calcMarginal("P")*calcMarginal("S"))))
				return conditional
	
	
def calcJoint(n):
	args = n[:]
	if (args == "PSC" or "PCS" and not "psc" or "pcs" or "ps~c"):
		array = []
		array.append(Bayes.node["C"]["ps"]*calcMarginal("P")*calcMarginal("S"))
		array.append((1-Bayes.node["C"]["ps"])*calcMarginal("P")*calcMarginal("S"))
		array.append(Bayes.node["C"]["~ps"]*calcMarginal("~p")*calcMarginal("S"))
		array.append((1-Bayes.node["C"]["~ps"])*calcMarginal("~p")*calcMarginal("S"))
		array.append(Bayes.node["C"]["p~s"]*calcMarginal("P")*calcMarginal("S"))
		array.append((1-Bayes.node["C"]["p~s"])*calcMarginal("P")*calcMarginal("~s"))
		array.append(Bayes.node["C"]["~p~s"]*calcMarginal("~p")*calcMarginal("~s"))
		array.append((1-Bayes.node["C"]["~p~s"])*calcMarginal("~p")*calcMarginal("~s"))
		return array
	elif (args == "psc" or "pcs"):
		prob = (Bayes.node["C"]["ps"]*calcMarginal("P")*calcMarginal("S"))
		return prob 
	elif (args == "ps~c"):
		prob = ((1-Bayes.node["C"]["ps"])*calcMarginal("P")*calcMarginal("S"))
		return prob
	elif (args == "p~sc"):
		prob = (Bayes.node["C"]["p~s"]*calcMarginal("P")*calcMarginal("~s"))
		return prob 
	elif (args == "~psc"):
		prob = (Bayes.node["C"]["~ps"]*calcMarginal("~p")*calcMarginal("S"))
		return prob 
	elif (args == "~p~s~c"):
		prob = ((1-Bayes.node["C"]["~p~s"])*calcMarginal("~p")*calcMarginal("~s"))
		return prob
	elif (args == "~ps~c"):
		prob = ((1-Bayes.node["C"]["~ps"])*calcMarginal("~p")*calcMarginal("S"))
		return prob
	elif (args == "~p~sc"):
		prob = (Bayes.node["C"]["~p~s"]*calcMarginal("~p")*calcMarginal("~s"))
		return prob
	elif (args == "p~s~c"):
		prob = ((1-Bayes.node["C"]["p~s"])*calcMarginal("P")*calcMarginal("~s"))
		return prob
		

#-jpsc 


def main():
	try:
		opts, args = getopt.getopt(sys.argv[1:], "m:g:j:p:")
	except getopt.GetoptError as err:
		#print help info and exit
		print(err)
		sys.exit(2)
	for o, a in opts:
		if o in ("-p"):
			setPrior(a[0], float(a[1:]))
		elif o in ("-m"):
			marginal = calcMarginal(a)
			print(marginal)
		elif o in ("-g"):
			#p = a.find("/")
			#conditional = 
			conditional = calcConditional(a[:])
			print(conditional)
		elif o in ("-j"):
			joint = calcJoint(a[:])
			print(joint) 
			#do joint 
        #else:             for some reason, still triggers this else anyway, so dont mess up input
			#assert False, "unhandled option"
	
if __name__ == "__main__":
	main()
