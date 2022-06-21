import numpy as np


def divided_fitting_function(c,a,df,estia,zo):
    return a+np.multiply(((c-estia)/zo),4*df)/((np.power(((c-estia)/zo),2)+9)*(np.power((c-estia)/zo,2)+1))

def open_fitting_function(c,q,estia,zo,plato):
    return  plato-q*0.354/(1+np.power((c-estia),2)/zo**2)

def linear_fitting(c,a):
    return a*c