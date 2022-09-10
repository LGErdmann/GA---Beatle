import math
import random



class Beatle:

	def __init__(self, R, G, B, fit):
        #Genomas
		self.R = R
		self.G = G
		self.B = B
		self.fit = fit

	def __repr__(self):
		return str(self.fit)


#######Primeiro Bloco######
def creatBeatle():
	R = random.randint(0, 255)
	G = random.randint(0, 255)
	B = random.randint(0, 255)
	BeatleJuice = Beatle(R, G, B, (R + G + B) / 765)

	return BeatleJuice


def initialPop(size):																																																						
	population = []

	for i in range(size):
		population.append(creatBeatle())
	print("População Inicial")
	print(population)
	print("\n")
	
	return population


########Segundo Bloco######


def fit(BeatleJuice):
	fitness = 1 - (BeatleJuice.R + BeatleJuice.G + BeatleJuice.B) / 765 
	return fitness


def GemRullet(population):
	#print("\nGem Parte 1")
	Roll = []
	Porcent = []
	aux = 0
	sum = 0
	cont = 0
	equal = True
	for Beatle in population:
		sum += fit(Beatle)
		Roll.append(fit(Beatle))
	#print(Roll)
	for x in range(len(Roll)):
		Roll[x] = math.floor( (Roll[x] * 100) / sum)
	#print(Roll)
	while aux <= len(Roll) - 1:
		cont = 0
		while cont <= Roll[aux]:
			Porcent.append(aux)
			cont += 1
		aux += 1


        #	while cont ==	Roll[x]:
    #		Porcent.append(x)
    #		cont += cont

	select = random.randint(0, 99)
	Dad = population[Porcent[select]]

	while (equal):
		select = random.randint(0, 99)
		Mom = population[Porcent[select]]
		if Mom != Dad:
			equal = False
		#print("Mãe "+ str(Mom))
		#print("Pai "+ str(Dad))
		breed = Breed(Dad, Mom)
		#print("(Rullet)Filho " + str(breed))
		
		return breed


def Breed(Mom, Dad):
	Son = creatBeatle()
	Son.R = Mom.R
	Son.G = Dad.G
	Son.B = Mom.B
	son = mutation(Son)
	#print("\n" +str(Son.R)+ " " +str(Mom.R))
	#print("" +str(Son.G)+ " " +str(Dad.G))
	#print("" +str(Son.B)+ " " +str(Mom.B))
	Son.fit = fit(Son)
	#print("########################")
	#print("(Breed)Filho " + str(son))
	#print("########################")
	return	son


def Generation(population, size):
	#print("\n(Generation)Parte 1")
	NewPopulation = []

	for i in range(size):
		x = GemRullet(population)
		#print("Adicionado filho"+ str(x))
		NewPopulation.append(x)
	#print("\n")
	#print("Nova população")
	#print(NewPopulation)
	#print("\n")
	return NewPopulation


def mutation(son):
	evolve = random.randint(-255, 255)
	if random.randint(0, 100) > 90:
		#print("Mutação")
		x = random.randint(0, 2)
		if x == 0:
			son.R = son.R + evolve
			if son.R < 0:
				son.R = 0
				return	son
			if son.R > 255:
				son.R = 255
				return	son
			else:
				return	son
		
		if x == 1:
			son.G = son.G + evolve
			if son.G < 0:
				son.G = 0
				return	son
			if son.G > 255:
				son.G = 255
				return	son				
			else:
				return	son
		
		if x == 2:
			son.B = son.B + evolve
			if son.B < 0:
				son.B = 0
				return	son
			if son.B > 255:
				son.B = 255
				return	son
			else:
				return son
	else:
		return son
			

#def mutation(son):
#    evolve = random.randint(150, 255)
#		
#   if random.uniform(0.01, 1) > 0.89:
#        son.R = son.R + evolve
#    if son.R > 255:
#        son.R = 255
#
#    else:
#        return son
#    return son

#def elitism(population):
#	cont = 0
#	while cont < len(population):
#		if Population[cont].fit > 0.80:
#			Elite = Population[cont]
#			return Elite
#		cont += 1

#time = True
#size = 50
#ContTime = 0
#Population = initialPop(size)
#Besouro = 0
#Parada = 0.55
#while (time):
#while (ContTime < time):
#	print("\nGeração " + str(ContTime))
#	Population = Generation(Population, size)
#	contFit = 0
#
#	for x in Population:
#		if x.fit >= Parada:
#			contFit += 1
#		if contFit == size:
#			time = False
#	ContTime += 1
#
#for x in Population:
#				#print("\n",x.R,x.G,x.B,x.fit)
#		if x.fit > Parada:
#			print("\nBesouro " + str(Besouro) + " "+str(x.fit))
#			print(C().rgb(x.R, x.G, x.B, "       ,_    /) (\    _,"))
#			print(C().rgb(x.R, x.G, x.B, "        >>  <<,_,>>  <<"))
#			print(C().rgb(x.R, x.G, x.B, "       //   _0.-.0_   \\"))
#			print(C().rgb(random.randint(x.R, 255), random.randint(x.G, 255), random.randint(x.B, 255), "        \'._/░░░░░░░\_.'/"))
#			print(C().rgb(x.R, x.G, x.B, "        '-.\.--.--./.-'"))
#			print(C().rgb(x.R, x.G, x.B, "        __/ ░░░Y░░░ \ _"))
#			print(C().rgb(x.R, x.G, x.B, "';,  .-(_| ░░░░|░░░░ |_)-.  ,:'"))
#			print(C().rgb(x.R, x.G, x.B, "   \\/.'  |░░░░░|░░░░░|  `.\//"))			
#			print(C().rgb(x.R, x.G, x.B, "   (/    |░░░░░|░░░░░|    \)"))
#			print(C().rgb(x.R, x.G, x.B, "         |░░░░░|░░░░░;"))
#			print(C().rgb(x.R, x.G, x.B, "        /░░░░░░|░░░░░░\."))
#			print(C().rgb(x.R, x.G, x.B, "       (_/'.░ ░░░ ░.'\_)"))
#			print(C().rgb(x.R, x.G, x.B, "        \\  `""`""`     //"))
#			print(C().rgb(x.R, x.G, x.B, "         \\          //"))
#			print(C().rgb(x.R, x.G, x.B, "           ':.     .:'\n"))
#			Besouro += 1
#
#print("\nGeração: " + str(ContTime))		
#print(Population)


