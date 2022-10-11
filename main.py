import numpy as np
import matplotlib.pyplot as plt
import random
import math
from data_loader import *

frequency = 1/10
cycle_frequency = 2 * np.pi * frequency 

def arr_aligment(arr, elements_count):
    """Приведение массива к заданной длине"""
    len_diff = elements_count - len(arr)
    if len_diff > 0:
        arr = np.concatenate((arr, np.full(len_diff, arr[-1])))
    elif len_diff < 0:
        arr = arr[:elements_count]
    return arr

def get_ampl():
    """Расчёт амлитуды сигнала"""
    return 1.9 + (0.2 * random.random() - 0.1)                

def normal_mode(t):
    """Генерация ваттметрограммы для нормального режима работы"""
    #Амплитуда сигнала движения вверх
    #amplitude = 1.0 + 0.1 * random.random()
    #Количество отсчётов сигнала
    samples_count = len(t)
    #Движение вверх
    up_stroke = get_ampl() * np.sin(cycle_frequency * t[:(math.ceil(samples_count / 2))])
    #Движение вниз
    down_stroke = 0.9 * get_ampl() * np.sin(2 * np.pi * 1/10 * t[:(math.ceil(samples_count / 2))])
    
    return arr_aligment(np.concatenate((up_stroke, down_stroke)), samples_count)

def traveling_valve_leakage(t):
    """Генерация ваттметрограммы для утечки обратного клапана"""
    samples_count = len(t)

    #Движение вверх
    up_stroke = 0.5 * get_ampl() * np.sin(cycle_frequency * t[:(math.ceil(samples_count / 2))])
    #Движение вниз
    down_stroke = 0.9 *  get_ampl() * np.sin(cycle_frequency * t[:(math.ceil(samples_count / 2))])
    return arr_aligment(np.concatenate((up_stroke, down_stroke)), samples_count)

def insufficient_liquid_supply(t):
    """Генерация ваттметрограммы при недостататке жидкости в скважине"""

    #Движение вверх
    samples_count = len(t)
    up_stroke = get_ampl() * np.sin(cycle_frequency * t[:(math.ceil(samples_count / 2))])

    #Участок соответсвующий нормальному движению вниз, занимает 1/8 периода ваттметрограммы
    down_stroke = 0.5 * get_ampl() * np.sin(cycle_frequency * t[:(math.ceil(samples_count / 8))]) 

    start_point = down_stroke[-1] #Точка, на которой закончился предыдущий интервал 
    #Участок, состоящий из периода колебания с частотой в 4 раза большей, чем частота ваттметрограммы
    r1 = start_point + 0.06 * np.sin(2 * (np.pi / math.ceil(samples_count / 4)) * np.arange(0, math.ceil(samples_count / 4)))
    
    #Участок представляющий собой параболу
    p_amp = 0.3 * get_ampl() # амплитуда параболы
    a = -p_amp * 256 / (samples_count * samples_count) #расчёт коэффициента a, 256 так как парабола занимает 1/16 периода ваттметрограммы
    r2 = a * (np.power((np.arange(0, math.ceil(samples_count / 8)) - samples_count / 16), 2)) + p_amp + start_point
    
    down_stroke = np.concatenate((down_stroke, r1, r2))

    return arr_aligment(np.concatenate((up_stroke, down_stroke)), samples_count)

time = np.linspace(0, 10, 500)


#Создание обучающей выборки
file_handler = open("C:\\Users\makarovda\\Documents\\pythonProjects\\mpcs\\learn.csv", 'w')

for i in range(75):
    label = random.randint(0, 2)

    if label == 0:
        mpc = normal_mode(time)
    elif label == 1:
        mpc = traveling_valve_leakage(time)
    elif label == 2:
        mpc = insufficient_liquid_supply(time) 
    
    data_string = (np.array2string(mpc,separator=',',formatter={'float': lambda x: "%.8f" % x}))
    
    data_string = str(label) + 'lb' + str(len(mpc)) + 'cnt' + data_string.replace('\n','') + '\n' 
    
    file_handler.write(data_string)
    
file_handler.close()

#Создание тестовой выборки
file_handler = open("C:\\Users\makarovda\\Documents\\pythonProjects\\mpcs\\test.csv", 'w')

for i in range(75):
    label = random.randint(0, 2)

    if label == 0:
        mpc = normal_mode(time)
    elif label == 1:
        mpc = traveling_valve_leakage(time)
    elif label == 2:
        mpc = insufficient_liquid_supply(time) 
    
    data_string = (np.array2string(mpc,separator=',',formatter={'float': lambda x: "%.8f" % x} ))
    
    data_string = str(label) + 'lb' + str(len(mpc)) + 'cnt' + data_string.replace("\n","") + "\n" 
    
    file_handler.write(data_string)
    
file_handler.close()



(labels, mpcs) = data_loader("C:\\Users\makarovda\\Documents\\pythonProjects\\mpcs\\test.csv")
print(labels)




 

