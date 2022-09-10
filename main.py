from G import Generation, initialPop
from colr import Colr as C
import random

time = True
size = 50
ContTime = 0
Population = initialPop(size)
Besouro = 0
Parada = 0.55
while (time):
#while (ContTime < time):
	print("\nGeração " + str(ContTime))
	Population = Generation(Population, size)
	contFit = 0

	for x in Population:
		if x.fit >= Parada:
			contFit += 1
		if contFit == size:
			time = False
	ContTime += 1

for x in Population:
				#print("\n",x.R,x.G,x.B,x.fit)
		if x.fit > Parada:
			print("\nBesouro " + str(Besouro) + " "+str(x.fit))
			print(C().rgb(x.R, x.G, x.B, "       ,_    /) (\    _,"))
			print(C().rgb(x.R, x.G, x.B, "        >>  <<,_,>>  <<"))
			print(C().rgb(x.R, x.G, x.B, "       //   _0.-.0_   \\"))
			print(C().rgb(random.randint(x.R, 255), random.randint(x.G, 255), random.randint(x.B, 255), "        \'._/░░░░░░░\_.'/"))
			print(C().rgb(x.R, x.G, x.B, "        '-.\.--.--./.-'"))
			print(C().rgb(x.R, x.G, x.B, "        __/ ░░░Y░░░ \ _"))
			print(C().rgb(x.R, x.G, x.B, "';,  .-(_| ░░░░|░░░░ |_)-.  ,:'"))
			print(C().rgb(x.R, x.G, x.B, "   \\/.'  |░░░░░|░░░░░|  `.\//"))			
			print(C().rgb(x.R, x.G, x.B, "   (/    |░░░░░|░░░░░|    \)"))
			print(C().rgb(x.R, x.G, x.B, "         |░░░░░|░░░░░;"))
			print(C().rgb(x.R, x.G, x.B, "        /░░░░░░|░░░░░░\."))
			print(C().rgb(x.R, x.G, x.B, "       (_/'.░ ░░░ ░.'\_)"))
			print(C().rgb(x.R, x.G, x.B, "        \\  `""`""`     //"))
			print(C().rgb(x.R, x.G, x.B, "         \\          //"))
			print(C().rgb(x.R, x.G, x.B, "           ':.     .:'\n"))
			Besouro += 1

print("\nGeração: " + str(ContTime))		
print(Population)


