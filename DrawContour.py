import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
def Draw_Contour(NumSats, SenAng, typeVar):
    #Loading Result File from runRTV.py
    Output = pd.read_csv('Output.csv')

    #Sorting and Filtering the results
    Output = Output.sort_values(by='Altitude',axis=0)
    condition_Satnum = (Output['NumberSats'] == NumSats)
    condition_SenAng = (Output['SenAng'] == SenAng)
    condition_Inc42 = (Output['Inclination'] == 52)
    condition_Inc80 = (Output['Inclination'] == 80)
    condition_IncSSO = (Output['Inclination'] >= 90)
    Output_all_condition42 = Output[condition_Satnum & condition_SenAng & condition_Inc42]
    Output_all_condition80 = Output[condition_Satnum & condition_SenAng & condition_Inc80]
    Output_all_conditionSSO = Output[condition_Satnum & condition_SenAng & condition_IncSSO]

    #Define X, Y coordinate for contour plot
    alt = Output_all_condition42['Altitude']
    alt_list = np.array(alt.values.tolist())
    #inc = [42, 80]
    inc = [52, 80, 98]
    X, Y = np.meshgrid(alt_list, inc)

    #Define Z coordinate for contour plot
    Var42 = Output_all_condition42[typeVar]
    Var80 = Output_all_condition80[typeVar]
    VarSSO = Output_all_conditionSSO[typeVar]
    Var42_list = Var42.values.tolist()
    Var80_list = Var80.values.tolist()
    VarSSO_list = VarSSO.values.tolist()
    #Var22 = np.array([Var42_list, Var80_list])
    Var22 = np.array([Var42_list, Var80_list, VarSSO_list])

    #Plot Contour & Labelling
    cp = plt.contourf(X, Y, Var22)
    plt.colorbar(cp)
    plt.xlabel('Altitude')
    plt.ylabel('Inclination')
    plt.title("{Pe_t} for Number of Sat = {Te_t} Sensor Angle = {n_t}"
              .format(Pe_t = typeVar, Te_t = NumSats, n_t = SenAng))

#Plotting Contour graphs in one page
a = [1, 4, 16, 32]
b = [10, 20, 30]
k = 1
fig = plt.figure()
for i in a:
    for j in b:
        fig.add_subplot(4,3, k)
        Draw_Contour(i, j, 'avgVar') #Put 'avgVar' or 'maxVar' or 'minVar' for Average/Maximum/Minimum revisit time
        k = k + 1

#fig.tight_layout()
plt.subplots_adjust(left=0.125,
                    bottom=0.1,
                    right=0.9,
                    top=0.9,
                    wspace=0.2,
                    hspace=0.5)
plt.show()
