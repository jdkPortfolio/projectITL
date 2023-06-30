import time
times = 1
# def display_data(delayAB, delayC, countAB, countC, times):
#     if times == 1:
#         print("Stats Collected : ")
#         print(96*"-")
#         print("| AB Delay   | C Delay | AB Vehicle Count | C Vehicle Count | Scaled AB Delay | Scaled C Delay |")
#         print(96*"-")
#         print("    "+str(round(delayAB, 1))+"         "+str(round(delayC))+"            "+str(countAB)+"                "+str(countC)+"                   "+str(round(delayAB/10, 1))+"                "+str(round(delayC/10, 1))+"  ")
#         print(96*"-")
#     else:
#         print("    "+str(round(delayAB, 1))+"         "+str(round(delayC))+"            "+str(countAB)+"                "+str(countC)+"                   "+str(round(delayAB/10, 1))+"                "+str(round(delayC/10, 1))+"  ")
#         print(96*"-")

#     times += 1
#     return times

def display_data(delayAB, delayC, countAB, countC, times):
    if times == 1:
        print('Stats Collected : ')
        print('DelayAB : '+str(delayAB))
        print('DelayC : '+str(delayC))
        print('CountAB : '+str(countAB))
        print('CountC : '+str(countC))
        print('Scaled AB Delay : '+str(round(delayAB/10, 1)))
        print('Scaled C Delay : '+str(round(delayC/10, 1)))
        print(20*'-')
    else:
        print('DelayAB : '+str(delayAB))
        print('DelayC : '+str(delayC))
        print('CountAB : '+str(countAB))
        print('CountC : '+str(countC))
        print('Scaled AB Delay : '+str(round(delayAB/10, 1)))
        print('Scaled C Delay : '+str(round(delayC/10, 1)))
        print(20*'-')

    times += 1
    return times
##while True:
##    times = display_data(1, 0, 0, 0, times)
##    time.sleep(3)
