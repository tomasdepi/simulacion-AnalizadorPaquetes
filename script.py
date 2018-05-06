import random
import sys
import math

# CONDICIONES INICIALES

CT = int(sys.argv[1])

T = 0 # tiempo
HighValue = 10000000000
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

print ("Cantidad de Threads " + str(CT))
print ("Simulacion para " + str(TF) + " Microsegundos")

def getIndexMinValueOfList(list):
	return list.index(min(list))

def getIntervaloArribo():
	rand = random.uniform(0,1)
	return (1573.3 - 2853.8 * math.log(-1*math.log(rand)))

def getTiempoEvaluacion():
	return random.randint(3000,5000)

def atenderPaquete(threadMenorCarga):
	global TPS
	global ITO
	global STO
	global STE
	global TPT
	TE = getTiempoEvaluacion()
	TPS[threadMenorCarga] = T + TE
	STO[threadMenorCarga] += T - ITO[threadMenorCarga]
	STE[threadMenorCarga] += TE
	TPT[threadMenorCarga] += 1

while T <= TF:
	print(T)
	threadProximaSalida = getIndexMinValueOfList(TPS)

	if TPLL <= TPS[threadProximaSalida]: # llegada

		T = TPLL
		IA = getIntervaloArribo()
		TPLL = T + IA

		threadMenorCarga = getIndexMinValueOfList(PT)
		STPS[threadMenorCarga] += (TPLL - T)*PT[threadMenorCarga]
		
		R = random.randint(0,99)

		if(R <= 9): # paquete de prioridad

			PARP +=1

			if(PARP == 1 and PT[threadMenorCarga] == 0):
				PARP -= 1
				PT[threadMenorCarga] += 1
				atenderPaquete(threadMenorCarga)

		else: # paquete baja prioridad

			PT[threadMenorCarga] += 1

			if(PT[threadMenorCarga] == 1):
				atenderPaquete(threadMenorCarga)

	else: # salida
		print(T)
		T = TPS[threadProximaSalida]
		PT[threadProximaSalida] -= 1
		STPS[threadProximaSalida] += (TPS[threadProximaSalida] - T)*PT[threadProximaSalida]

		if PARP > 0 or (PARP == 0 and PT[threadProximaSalida] > 0):

			if(PARP > 0):
				PARP -= 1
				PT[threadProximaSalida] += 1

			TE = getTiempoEvaluacion()
			TPS[threadProximaSalida] = T + TE
			STE[threadProximaSalida] += TE

		else: # el thread pasa a estar oscioso

			ITO[threadProximaSalida] = T
			TPS[threadProximaSalida] = HighValue


for thread in range(0, CT):
	print("Informacion Thread " + str(thread+1))
	print("TPT " + str(TPT[thread]))
	print("STE " + str(STE[thread]))
	print("STPS " + str(STPS[thread]))
	print("PPS " + str(STPS[thread] / TPT[thread]))
	print("PEC " + str((STPS[thread] - STE[thread]) / TPT[thread]))
	print("PTO " + str((STO[thread] * 100 / T)))
