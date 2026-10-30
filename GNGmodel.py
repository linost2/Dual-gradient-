
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 10 20:19:43 2021

@author: Ivan
"""

# Exporting the coordination of seed for gradient nano-grains 
# Candicate d0 =50 layers = 6; g = 0.28/0; xy = 5&d0 
# x方向始终为梯度方向，冲击方向需要自己设置


import sys
import random
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D




def model_create(g,d0,layers):
    """
    Parameters
    ----------
    g : gradient parameters
    d0 : units_angstron

    Returns
    -------
    None.

    """

    def inter_x(x1):
        
        return (1+0.5*g)/(1-0.5*g)*x1+d0
    
    
    def inter_x_down(x1):
        
        return ((1-0.5*g)*x1+g*(g+2)*xlist1[-1]+(1+g)*(d0*(1-0.5*g)))/(1+0.5*g)
    
    
    def yz_pos(d,length):# 120这里+1对齐
        
        """
        The uniform distribution of nodes along y/z direction
        """
        
        # return [ (i+0.2)* d for i in range(0,int(round(length/d)))]
        return [ (i)* d for i in range(0,int(round(length/d)))]
        # return [0]
    def choose_to_draw(a,b):
        
        fig, ax2 = plt.subplots(dpi=200)
        ax2.scatter(eval(a+'list'),eval(b+'list'),s=10)
        ax2.vlines([0, eval(b+'_length')], 0,eval(a+'_length'), linestyles='-', colors='red')
        ax2.hlines([0, eval(a+'_length')], 0, eval(b+'_length'), linestyles='-', colors='red')
        
        ax2.vlines([0, x_length], 0,eval(a+'_length'), linestyles='-', colors='red')
        ax2.set_aspect('equal')
        return 

    global y_length, z_length
    
    layers = layers                        #layers 单边的层数                    #smallest grain size
    devia = 0.05                       #deviation in nodes  
    margin = 0                       #avoid periodic on GBs along X
    
    y_length = 900  #shock direction 900 对于垂直梯度的冲击 x为梯度方向，y为冲击方向
    z_length = 220

#迭代函数解析式

    script_list = []
    script_pore_list = []
    
    xold = 0.5*d0
    xlist1 = [xold,]



    for i in range(layers-1):
        
        xnew = inter_x(xold)
        xlist1.append(xnew)
        xold = xnew


    xold2 = (1+g)*xlist1[-1]+d0*(1-0.5*g)
    xlist2 = [xold2,]




    for i in range(layers,2*layers-1):
        xnew = inter_x_down(xold2)

        xlist2.append(xnew)
        xold2 = xnew
    
    x_center_list = xlist1 +xlist2
    d_list = [g*x_center_list[i]+d0*(1-0.5*g) for i in range(layers)]+[-g*x_center_list[i]+g*(g+2)*xlist1[-1]+(1+g)*(d0*(1-0.5*g)) for i in range(layers,2*layers)]
    x_length= xlist2[-1]+0.5*d0+margin

#创建位置队列
    
    global  xlist,ylist,zlist
    xlist,ylist,zlist = [],[],[]
    xlist_p,ylist_p,zlist_p = [],[],[]
    mark = 0
    for layer in range(2*layers):
        
        d = d_list[layer]
        print(0.2*d)
        for y in range(int(round(y_length/d))):#120 这里+1对齐
            
            
            # for z in range(int(round(z_length/d))):
            for z in range(int(round(z_length/d))):
                # add deviation  
                xpos = np.array(x_center_list[layer])+random.uniform(devia*d*(-1),devia*d)
                
                ypos = np.array(yz_pos(d,y_length)[y])+random.uniform(devia*d*(-1),devia*d)
                
                if g == 0.0:
                    xpos = np.array(x_center_list[layer])+random.uniform(devia*d*(-1),devia*d)+0.5*d*((y+1)%2) # 对于均匀多晶 加挪移0.5*d*((y+1)%2)
                    ypos = np.array(yz_pos(d,y_length)[y])+random.uniform(devia*d*(-1),devia*d)
                    
                zpos = np.array(yz_pos(d,z_length)[z])+random.uniform(devia*d*(-1),devia*d)
                # zpos = 0.5*z_length*(z-1)+0.25*z_length+0.125*z_length#random.uniform(devia*30*(-1),devia*30)#z向双层

                if g!= 0.0:
                    if layer>=layers:
                    
                        ypos += 0.1*d
                        
                ylist.append(xpos)#垂直梯度方向则颠倒
                xlist.append(ypos)
                zlist.append(zpos)
                
                
                
                
                mark += 1
                #print("节点{}坐标（{}，{}，{}）".format(mark,xpos,ypos,zpos))
                script = 'node '+str(ypos)+' '+str(xpos)+' '+str(zpos)+' '+'random'#节点坐标梯度要更改
                script_list.append(script)
                
                #开始挖空
                #梯度挖空
                # if y != 0 and g!= 0:
                #     script_p = 'select in sphere ' +str(ypos)+' '+str(xpos)+' '+str(zpos) + ' ' + str(0.2*d)
                #均匀挖孔对比    
                if y != 0 and g!=0:
                    
                    if layer == 0 or layer == 7:#对于第一行和最后一行：
                        
                        if y%4 ==2:
                            script_p = 'select in sphere ' +str(ypos)+' '+str(xpos)+' '+str(zpos) + ' 10' 
                            script_pore_list.append(script_p)
                           
                       
                        else :
                            continue
                       
                        
                        
                                
                    elif layer == 1 or layer == 6: # 对于中间两行
                        
                          
                        if y%3 ==0 :
                            continue
                        else:
                            script_p = 'select in sphere ' +str(ypos)+' '+str(xpos)+' '+str(zpos) + ' 10' 
                            script_pore_list.append(script_p)
                        
                       
                    elif layer == 2 or layer == 5: 
                        if y%3 ==1 :
                            
                            y1pos = ypos - 0.25*d 
                            y2pos = ypos + 0.25*d
      
                            
                            script_p1 = 'select in sphere ' +str(y1pos)+' '+str(xpos)+' '+str(zpos) + ' 10' 
                            script_p2 = 'select in sphere ' +str(y2pos)+' '+str(xpos)+' '+str(zpos) + ' 10' 
                
                            script_pore_list.append(script_p1)
                            script_pore_list.append(script_p2)
                       
                        else:
                            script_p = 'select in sphere ' +str(ypos)+' '+str(xpos)+' '+str(zpos) + ' 10' 
                            script_pore_list.append(script_p)
                        
                    elif layer == 3 or layer == 4: # 对于中间两行
                        y1pos = ypos - 0.3*d 
                        y2pos = ypos + 0.3*d
                        y3pos = ypos
                        
                        script_p1 = 'select in sphere ' +str(y1pos)+' '+str(xpos)+' '+str(zpos) + ' 10' 
                        script_p2 = 'select in sphere ' +str(y2pos)+' '+str(xpos)+' '+str(zpos) + ' 10' 
                        script_p3 = 'select in sphere ' +str(y3pos)+' '+str(xpos)+' '+str(zpos) + ' 10' 
                        script_pore_list.append(script_p1)
                        script_pore_list.append(script_p2)
                        script_pore_list.append(script_p3)
                            

#写入
    file = open('g'+str(g)+'d'+str(int(d0))+'.txt','w')
    # file.write('box '+str(x_length)+' '+str(y_length)+' '+str(z_length)+'\n') #平行冲击
    file.write('box '+str(y_length)+' '+str(x_length)+' '+str(z_length)+'\n') #垂直冲击
    
    for j in script_list:
        
        file.write(j+'\n')
    
    file.close()
    



    
    file_p = open('UNpore.ats','w')
    file_p.write('read Total.lmp'+'\n') #垂直冲击
    
    
    for j in script_pore_list:
        
        file_p.write(j+'\n')
        file_p.write('rmatom select\n')
        
    file_p.write('write final.lmp')
    file_p.close()
    
    
    
    print("\n 梯度多晶建模完成： 梯度方向长度为{:.2f},平面方向长度{:.2f},垂直方向长度{:.2f}，晶粒数为{},预估平均晶粒尺寸{}"\
          .format(x_length,y_length,z_length,len(xlist),np.mean(d_list)))
    
    print('尺寸列表{}'.format(d_list))
    print('中心坐标列表{}'.format(x_center_list))
    print('xyz方向尺寸{}，{}，{}，单边层数{}'.format(x_length,y_length,z_length,layers))
#种子点可视化

    choose_to_draw('x','y')#'y' or 'z'

    fig = plt.figure()
    ax1 = fig.add_subplot(111, projection='3d')
    ax1.scatter(xlist,ylist,zlist)
    
    
    return x_length,y_length,z_length,len(xlist),np.mean(d_list)


#%%
# model_create(0.12,20)#formal

# model_create(0,206,3)
# model_create(0.32,40,4)
model_create(0,70,4)
 # %%
"""创建模型到当前路径"""
# if __name__ =='__main__':
#     print(type(sys.argv[1]))
#     model_create(float(sys.argv[1]),float(sys.argv[2]))
    
#     print("act as itself\n")

