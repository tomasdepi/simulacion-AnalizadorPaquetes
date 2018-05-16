import random
import sys
import math

# CONDICIONES INICIALES

CT = int(sys.argv[1])

T = 0 # tiempo
HighValue = 10000000000000000
SS = [0] * CT # sumatoria tiempo de salida de cada thread
SLL = [0] * CT # sumatoria tiempo de llegada de cada thread
STE = [0] * CT # sumatoria tiempo de evaliacion de cada thread
ITO = [0] * CT # inicio tiempo oscioso de cada thread
STO = [0] * CT # sumatoria tiempo oscioso de cada thread
TPLL = 0 # tiempo de proxima llegada
TPS = [HighValue] * CT # tiempo de proxima salia de cada thread
PARP = 0 # cantidad de paquetes ARP encolados
PT = [0] * CT # cantidad de paquetes en cada thread
TF = int(sys.argv[2]) # tiempo final
TPT = [0] * CT # total paquetes que pasaron por el thread
STPS = [0] * CT
outputFile = sys.argv[3]


print ("Cantidad de Threads " + str(CT))
print ("Simulacion para " + str(TF) + " Microsegundos")

def getIndexMinValueOfList(list):
	return list.index(min(list))

def getIntervaloArribo():
	rand = random.uniform(0,1)
	resultado = 157.33 - 285.38 * math.log(-1*math.log(rand))

	if resultado < 0:
		return getIntervaloArribo()
	else:
		return resultado

def getTiempoEvaluacion():
	rand = random.uniform(0,1)
	resultado = 2505.6 - math.log((1/rand) - 1)*722.3

	if resultado < 0:
		return getTiempoEvaluacion()
	else:
		return resultado

def atenderPaquete(threadMenorCarga):
	global TPS
	global ITO
	global STO
	global STE
	global T
	TE = getTiempoEvaluacion()
	TPS[threadMenorCarga] = T + TE
	STO[threadMenorCarga] += T - ITO[threadMenorCarga]
	STE[threadMenorCarga] += TE
	

while T <= TF:
	threadProximaSalida = getIndexMinValueOfList(TPS)

	if TPLL <= TPS[threadProximaSalida]: # llegada

		threadMenorCarga = getIndexMinValueOfList(PT)
		for thread in range(0, CT):
			STPS[thread] += (TPLL - T)*PT[thread]	
		
		T = TPLL
		IA = getIntervaloArribo()
		TPLL = T + IA

		R = random.randint(0,99)

		if(R <= 9): # paquete de prioridad

			PARP +=1

			if(PARP == 1 and PT[threadMenorCarga] == 0):
				PARP -= 1
				PT[threadMenorCarga] += 1
				TPT[threadMenorCarga] += 1
				atenderPaquete(threadMenorCarga)

		else: # paquete baja prioridad

			PT[threadMenorCarga] += 1
			TPT[threadMenorCarga] += 1

			if(PT[threadMenorCarga] == 1):
				atenderPaquete(threadMenorCarga)

	else: # salida

		for thread in range(0, CT):
			STPS[thread] += (TPS[threadProximaSalida] - T)*PT[thread]

		T = TPS[threadProximaSalida]
		PT[threadProximaSalida] -= 1

		if PARP > 0 or (PARP == 0 and PT[threadProximaSalida] > 0):

			if(PARP > 0):
				PARP -= 1
				PT[threadProximaSalida] += 1
				TPT[threadProximaSalida] += 1

			TE = getTiempoEvaluacion()
			
			TPS[threadProximaSalida] = T + TE
			STE[threadProximaSalida] += TE

		else: # el thread pasa a estar oscioso

			ITO[threadProximaSalida] = T
			TPS[threadProximaSalida] = HighValue

file = open(outputFile, "w")

for thread in range(0, CT):
	print("Informacion Thread " + str(thread+1))
	file.write("Informacion Thread " + str(thread+1)+"\n")
	
	print("PPS " + str(STPS[thread] / TPT[thread]))
	file.write("PPS " + str(STPS[thread] / TPT[thread])+"\n")
	print("PEC " + str((STPS[thread] - STE[thread]) / TPT[thread]))
	file.write("PEC " + str((STPS[thread] - STE[thread]) / TPT[thread])+"\n")
	print("PTO " + str((STO[thread] * 100 / T)))
	file.write("PTO " + str((STO[thread] * 100 / T))+"\n")

