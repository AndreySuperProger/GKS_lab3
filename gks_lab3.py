#	Задача Джонсона о 2 станках
#	Вариант с 3 станками
#	Автор: Зволикевич А.В. ІК-51

import numpy as np

class Component():
	#класс Деталь
	def __init__(self, number, time_arr):
		self.number = number
		self.time = time_arr	#time[i] -- время обработки на і-той операции
		self.route = [1, 2, 3]	#технологический маршрут
		self.operation = 0		#Поточная операция
		self.engaged = False	#Обрабатываеться ли деталь на данный момент
		
class Portfolio():
	def __init__(self, time):
		self.time = time
		self.Components_list = []
	def Append_Component(self, comp):
		self.Components_list.append(comp)
		
class CompOperation():
	#класс объеденяет операцию, время начала и конца обработки
	def __init__(self, c, sT):
		self.comp = c
		self.startTime = sT
		self.endTime = sT + c.time[c.operation]
		
class GVM():
	def __init__(self, number):
		self.number = number
		self.engaged = False				#Выполняет ли станок работу на данный момент
		self.Comp = Component(0, [0, 0, 0])	#Деталь над которой проводиться обработка
		self.Portf = []						#Портфель работ
		self.WorkList = []					#Очередь обработок(массив CompOperation)
	
	def refresh(self, time):
		if (any(self.WorkList)):
			co = self.WorkList[len(self.WorkList) - 1]
			print("refreshing: gvm = " + str(self.number) + " t_e = " + str(co.endTime) + \
				" comp = " + str(co.comp.number) + ", comp engaged = " + str(co.comp.engaged))
			if co.endTime == time and co.comp.engaged == True:
				co.comp.engaged = False
				self.engaged = False
	

#T[j][i] -- время обработки j-той детали на і-той операции(гвм)
	
#Детали:
C = [
	Component(1, [2, 3, 3]),
	Component(2, [5, 2, 4]),
	Component(3, [3, 4, 3]),
	Component(4, [4, 1, 5])
	]
#Станки:
Q = [
	GVM(1),
	GVM(2),
	GVM(3)
	]

	
#########################debug##########################################
def printPortfolio():
	print("Portfolio:")
	for gvm in Q:
		print("gvm = " + str(gvm.number), end = ':')
		for p in gvm.Portf:
			print("t" + str(p.time), end = ':')
			for comp in p.Components_list:
				print(comp.number, end = " ")
			print(" ", end = '')
		print('')
		
def printWorkList():
	print("WorkList:")
	for gvm in Q:
		print("gvm = " + str(gvm.number))
		for w in gvm.WorkList:
			print("	comp = " + str(w.comp.number), end = ' ')
			print("t_start = " + str(w.startTime), end = ' ')
			print("t_end = " + str(w.endTime))
		print('')
#########################debug##########################################

#Разбить детали на 2 группы:
Comp_Group1 = [C[j] for j in range(0, 4) if C[j].time[0] < C[j].time[2]]
Comp_Group2 = [C[j] for j in range(0, 4) if C[j].time[0] >= C[j].time[2]]

#Отсортировать:
Comp_Group1.sort(key = lambda component: component.time[0] + component.time[1])
Comp_Group2.sort(key = lambda component: component.time[1] + component.time[2], reverse = True)

#Выводим расчитанные группы:
for j in range(0, len(Comp_Group1)):
	print(str(Comp_Group1[j].number) + " : " + str(Comp_Group1[j].time))
print("\n")
for j in range(0, len(Comp_Group2)):
	print(str(Comp_Group2[j].number) + " : " + str(Comp_Group2[j].time))

#Об́ъеденяем 2 массива в С
for j in range(0, len(Comp_Group1)):
	C[j] = Comp_Group1[j]
for j in range(0, len(Comp_Group2)):
	C[j + len(Comp_Group1)] = Comp_Group2[j]
del Comp_Group1, Comp_Group2
	
#Выводим последовательность обработки деталей:
for j in range(0, len(C)):
	if j != 0:
		print("-", end = '')
	print(str(C[j].number), end = '')
print('')

##########################test##########################################
"""C = [
	Component(1, [1, 4, 6]),
	Component(2, [1, 1, 5]),
	Component(3, [2, 2, 5]),
	Component(4, [3, 4, 4])
	]
	
C[0].route = [1, 3, 2]
C[1].route = [3, 1, 2]
C[2].route = [1, 3, 2]
C[3].route = [3, 2, 1]

#Станки:
Q = [
	GVM(1),
	GVM(2),
	GVM(3)
	]"""
##########################test##########################################

#Алгоритм формирования диаграммы Ганта:
time = 0
while any(comp for comp in C if comp.operation < 3):
	print("time = " + str(time))
	for gvm in Q:
		gvm.refresh(time)
	#ранжировка:
	Q1 = [q for q in Q if any(q.WorkList) and (not q.engaged)]
	print("Q1 before range:")
	for q in Q1:
		print("q = " + str(q.number))
	Q1.sort(key = lambda gvm: gvm.WorkList[len(gvm.WorkList) - 1].endTime)
	print("Q1 after range:")
	for q in Q1:
		print("q = " + str(q.number))
	Q2 = [q for q in Q if any(q.WorkList) == False or q.engaged]
	print("Q2:")
	for q in Q2:
		print("q = " + str(q.number))
	Q = Q2 + Q1
	for gvm in Q:
		print("	gvm = " + str(gvm.number))
		if gvm.engaged == False:		#Если станок завершил обработку
			print("	gvm not engaged")
			for comp in C:
				print("		comp = " + str(comp.number))
				if comp.engaged == False and comp.operation < 3:
					print("		comp not engaged")
					if comp.route[comp.operation] == gvm.number:	#Если следущая операция на этой gvm, то занести в портфель
						if any(pf.time == time for pf in gvm.Portf) == False:
							gvm.Portf.append(Portfolio(time))
						gvm.Portf[len(gvm.Portf) - 1].Components_list.append(comp)
						print("		Занесено в порфель")
					
			#Здесь нужно выбрать деталь из портфеля согласно правилу
			if (any(pf.time == time for pf in gvm.Portf)):
				chosenComp = min((comp for comp in gvm.Portf[len(gvm.Portf) - 1].Components_list), \
					key = lambda x: x.time[x.operation])
				print("	chosen = " + str(chosenComp.number))
				#######debug:
				for comp in gvm.Portf[len(gvm.Portf) - 1].Components_list:
					print("	comp = " + str(comp.number) + " time = " + str(comp.time[comp.operation]))
				#######debug
				gvm.Portf[len(gvm.Portf) - 1].Components_list.remove(chosenComp)	#Удалить деталь из порфеля
				gvm.WorkList.append(CompOperation(chosenComp, time))				#добавить в обработку
				chosenComp.operation += 1
				gvm.Comp = chosenComp
				gvm.engaged = True
				chosenComp.engaged = True
	time += 1		
			
		
	
printPortfolio()
printWorkList()
#criterion 1.1:

#criterion 2.1:
#criterion 2.3:
#criterion 2.6:
#criterion 3.1:
#criterion 3.4:
#criterion 3.6:


