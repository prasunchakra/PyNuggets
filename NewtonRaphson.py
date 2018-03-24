# -*- coding: utf-8 -*-
"""
Created on Thu Mar 22 23:05:20 2018

@author: lordprasun
"""
import math

def NewtonsMethod(F,FP,x0,epsilon) : 
    x = x0
    while math.fabs(F(x)) >= epsilon:
        x = x - F(x)/FP(x)  
    return x
 
if __name__=="__main__":
    print ("epsilon? 1E-4")
    epsilon = 0.0001
    
    F= lambda x: x**3 -x -1
    FP=lambda x: 3*x**2 -1
    x0=2
    root = NewtonsMethod(F,FP,x0,epsilon)
    res = round(F(root),5)
    root = round(root,5)    
    print ("F(x) = x**3-x-1, x0 = 2.0, F(%0.5f) = %0.5f" %(root,res))
    
    F= lambda x: x**3 +x -1
    FP=lambda x: 3*x**2 +1
    x0=2
    root = NewtonsMethod(F,FP,x0,epsilon)
    res = round(F(root),5)
    root = round(root,5)    
    print ("F(x) = x**3 +x -1, x0 = 2.0, F(%0.5f) = %0.5f" %(root,res))
    
    F= lambda x: x**2 -2
    FP=lambda x: 2*x
    x0=2
    root = NewtonsMethod(F,FP,x0,epsilon)
    res = F(root)
    print ("F(x) = x**2 -2, x0 = 2.0, F(%0.5f) = %0.5f" %(root,res))
    
    F= lambda x: 6*x**5-5*x**4-4*x**3+3*x**2
    FP=lambda x: 30*x**4-20*x**3-12*x**2+6*x
    x0=-1.1
    root = NewtonsMethod(F,FP,x0,epsilon)
    res = round(F(root),5)
    root = round(root,5)    
    print ("F(x) = 6*x**5-5*x**4-4*x**3+3*x**2, x0 = -1.1, F(%0.5f) = %0.5f" %(root,res))
    
    F= lambda x: 6*x**5-5*x**4-4*x**3+3*x**2
    FP=lambda x: 30*x**4-20*x**3-12*x**2+6*x
    x0=0.1
    root = NewtonsMethod(F,FP,x0,epsilon)
    res = round(F(root),5)
    root = round(root,5)    
    print ("F(x) = 6*x**5-5*x**4-4*x**3+3*x**2, x0 = 0.1, F(%0.5f) = %0.5f" %(root,res))
    
    F= lambda x: 6*x**5-5*x**4-4*x**3+3*x**2
    FP=lambda x: 30*x**4-20*x**3-12*x**2+6*x
    x0=0.5
    root = NewtonsMethod(F,FP,x0,epsilon)
    res = round(F(root),5)
    root = round(root,5)    
    print ("F(x) = 6*x**5-5*x**4-4*x**3+3*x**2, x0 = 0.5, F(%0.5f) = %0.5f" %(root,res))
    
    F= lambda x: 6*x**5-5*x**4-4*x**3+3*x**2
    FP=lambda x: 30*x**4-20*x**3-12*x**2+6*x
    x0=1.1
    root = NewtonsMethod(F,FP,x0,epsilon)
    res = round(F(root),5)
    root = round(root,5)    
    print ("F(x) = 6*x**5-5*x**4-4*x**3+3*x**2, x0 = 1.1, F(%0.5f) = %0.5f" %(root,res))
    
    
    


