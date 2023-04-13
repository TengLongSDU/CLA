#!/usr/bin/env python
# coding: utf-8

# In[1]:


import imageio

def read_image(img_path='binary.png'):
    im = imageio.imread(img_path)
    x_len,y_len=im.shape
    #print(x_len,y_len)
    
    return x_len,y_len,im


# In[2]:


import numpy as np

def generate_start_point(x_len,y_len):
    x_start=np.random.randint(1,x_len-1,size=2)
    y_start=np.random.randint(1,y_len-1,size=2)
    #print(x_start,y_start)
    return x_start,y_start


# In[3]:


def generate_k(x_start,y_start):
    if x_start[0]==x_start[1]:
        k='vertical'
    else:
        k=(y_start[0]-y_start[1])/(x_start[0]-x_start[1])
    #print('斜率为：',k)
    return k
    '''
    k_sign=np.random.random()-0.5
    if k_sign<=0:
        k1=-1
    else:
        k1=1

    k_order=6*np.random.random()-3
    k2=10**k_order

    k=k1*k2

    print('斜率为：',k)
    return k
    '''


# In[4]:


def generate_b(x_start,y_start,k):
    if k=='vertical':
        b=x_start[0]
    else:
        b=y_start[0]-k*x_start[0]
    #print('截距为：',b)
    return b


# In[5]:


def calculate_interception(x_len,y_len,k,b):

    if k=='vertical':
        y_x0=100000
        y_xlen=100000
        x_y0=b
        x_ylen=b
    else:
        y_x0=b+k*0
        y_xlen=b+k*(x_len-1)
        if k==0:
            x_y0=0
            x_ylen=x_len
        else:
            x_y0=(0-b)/k
            x_ylen=(y_len-1-b)/k
    
    return y_x0,y_xlen,x_y0,x_ylen

#print(y_x0,y_xlen,x_y0,x_ylen)


# In[6]:


def check_cross_points(x_len,y_len,y_x0,y_xlen,x_y0,x_ylen):

    x1=None
    y1=None
    x2=None
    y2=None
    x3=None
    y3=None
    x4=None
    y4=None
    
    check_up=0
    if y_x0<=y_len-1 and y_x0>0:
        x1=0
        y1=y_x0
        #print('与上边相交',x1,y1)
        check_up=1

    check_down=0
    if y_xlen<=y_len-1 and y_xlen>0:
        x2=x_len-1
        y2=y_xlen
        #print('与下边相交',x2,y2)
        check_down=1

    check_left=0
    if x_y0<=x_len-1 and x_y0>0:
        y3=0
        x3=x_y0
        #print('与左边相交',x3,y3)
        check_left=1

    check_right=0
    if x_ylen<=x_len-1 and x_ylen>0:
        y4=y_len-1
        x4=x_ylen
        #print('与右边相交',x4,y4)
        check_right=1

    #print(check_up,check_down,check_left,check_right,x1,y1,x2,y2,x3,y3,x4,y4)
    return check_up,check_down,check_left,check_right,x1,y1,x2,y2,x3,y3,x4,y4


# In[7]:


def get_points_list(x_len,y_len,k,b,check_up,check_down,check_left,check_right,x1,y1,x2,y2,x3,y3,x4,y4):

    P=[]

    if check_up==1 and check_down==1:
        for xi in range(x_len):
            yi=int(np.around(k*xi+b))
            Pi=[xi,yi]
            P.append(Pi)
        #print('上下','像素个数：',len(P))

    if check_up==1 and check_left==1:
        if k>=-1:
            for xi in range(int(np.around(x3))):
                yi=int(np.around(k*xi+b))
                Pi=[xi,yi]
                P.append(Pi)
        else:
            for yi in range(int(np.around(y1))):
                xi=int(np.around((yi-b)/k))
                Pi=[xi,yi]
                P.append(Pi)
        #print('上左','像素个数：',len(P))

    if check_up==1 and check_right==1:
        if k<=1:
            for xi in range(int(np.around(x4))):
                yi=int(np.around(k*xi+b))
                Pi=[xi,yi]
                P.append(Pi)
        else:
            for yi in range(int(np.around(y1)),y_len):
                xi=int(np.around((yi-b)/k))
                Pi=[xi,yi]
                P.append(Pi)
        #print('上右','像素个数：',len(P))

    if check_down==1 and check_left==1:
        if k<=1:
            for xi in range(int(np.around(x3)),x_len):
                yi=int(np.around(k*xi+b))
                Pi=[xi,yi]
                P.append(Pi)
        else:
            for yi in range(int(np.around(y2))):
                xi=int(np.around((yi-b)/k))
                Pi=[xi,yi]
                P.append(Pi)
        #print('下左','像素个数：',len(P))

    if check_down==1 and check_right==1:
        if k>=-1:
            for xi in range(int(np.around(x4)),x_len):
                yi=int(np.around(k*xi+b))
                Pi=[xi,yi]
                P.append(Pi)
        else:
            for yi in range(int(np.around(y2)),y_len):
                xi=int(np.around((yi-b)/k))
                Pi=[xi,yi]
                P.append(Pi)
        #print('下右','像素个数：',len(P))

    if check_left==1 and check_right==1:
        if k=='vertical':
            for yi in range(y_len):
                xi=b
                Pi=[xi,yi]
                P.append(Pi)
        else:
            for yi in range(y_len):
                xi=int(np.around((yi-b)/k))
                Pi=[xi,yi]
                P.append(Pi)
        #print('左右','像素个数：',len(P))
        
    return P,len(P)



# In[8]:


def frequency_radius(P,im,radius=3):
    radius_2=radius**2
    white_line=0
    black_line=0
    binary_line=0
    next_point=0

    while next_point<len(P)-1:
        original_point=next_point
        Pi=P[next_point]
        if (Pi[0]-P[-1][0])**2+(Pi[1]-P[-1][1])**2>radius_2:
            for j in range(original_point,len(P)):
                Pj=P[j]
                Pjp1=P[j+1]
                distance_2_j=(Pi[0]-Pj[0])**2+(Pi[1]-Pj[1])**2
                distance_2_jp1=(Pi[0]-Pjp1[0])**2+(Pi[1]-Pjp1[1])**2
                if distance_2_j<=radius_2 and distance_2_jp1>radius_2:
                    this_point=j
                    next_point=j+1
                    break
        else:
            this_point=len(P)-1
            next_point=len(P)


        this_line=[]
        white=0
        black=0
        #print(original_point,next_point)
        for k in range(original_point,next_point):
            this_line.append(P[k])
            #print(P[k])
            if im[P[k][0],P[k][1]]<100:
                white=white+1
            else:
                black=black+1
        if black==0:
            white_line=white_line+1
        if white<=min(radius-1,5):
            black_line=black_line+1
        if black>0 and white>min(radius-1,5):
            binary_line=binary_line+1
            
    #print(P,white_line,black_line,binary_line)
    frequency_p=white_line/(white_line+black_line+binary_line)
    frequency_m=black_line/(white_line+black_line+binary_line)
    
    
    return frequency_p,frequency_m


# In[9]:


def generate_kb(x_start,y_start):
    k=generate_k(x_start,y_start)
    b=generate_b(x_start,y_start,k)
    return k,b


# In[10]:


def get_line_points(x_len,y_len,k,b):
    y_x0,y_xlen,x_y0,x_ylen=calculate_interception(x_len,y_len,k,b)
    check_up,check_down,check_left,check_right,x1,y1,x2,y2,x3,y3,x4,y4=check_cross_points(x_len,y_len,y_x0,y_xlen,x_y0,x_ylen)
    P,len_P=get_points_list(x_len,y_len,k,b,check_up,check_down,check_left,check_right,x1,y1,x2,y2,x3,y3,x4,y4)
    #print(len_P)
    return P,len_P


# In[11]:


def generate_random_line(x_len,y_len):
    x_start,y_start=generate_start_point(x_len,y_len)
    k,b=generate_kb(x_start,y_start)
    P,len_P=get_line_points(x_len,y_len,k,b)
    #print(len_P)
    return P,len_P


# In[12]:


def get_statistic_per_radius(img_path='binary.png',radius=3,num_times=1000):
    x_len,y_len,im=read_image(img_path=img_path)
    RF_list_p=[]
    RF_list_m=[]
    for i in range(num_times):
        P,len_P=generate_random_line(x_len,y_len)
        #print(len_P)
        try:
            frequency_p,frequency_m=frequency_radius(P,im,radius)
            RF_points_p=[radius,frequency_p]
            RF_points_m=[radius,frequency_m]
            RF_list_p.append(RF_points_p)
            RF_list_m.append(RF_points_m)
        except ZeroDivisionError:
            pass
    return RF_list_p,RF_list_m


# In[13]:


def RF_list_average(RF_list):
    radius=RF_list[0][0]
    len_list=len(RF_list)
    sum_F=0
    for i in range(len_list):
        sum_F=sum_F+RF_list[i][1]
    average=sum_F/len_list
    
    return radius,average


# In[21]:


import matplotlib.pyplot as plt

mum_per_pixel=1/5.5

r_list=[]
f_list_p=[]
f_list_m=[]
for r in range(7,707,7):
    RF_list_p,RF_list_m=get_statistic_per_radius(img_path='./6 (4).tif',radius=r,num_times=200)
    radius_p,average_p=RF_list_average(RF_list_p)
    radius_p=radius_p*mum_per_pixel
    r_list.append(radius_p)
    f_list_p.append(average_p)
    if r<=10000:
        radius_m,average_m=RF_list_average(RF_list_m)
        f_list_m.append(average_m)
        print(radius_p,average_p,average_m)
    else:
        print(radius_p,average_p)

k_p,b_p = np.polyfit(r_list, np.log10(f_list_p), 1)
k_m,b_m = np.polyfit(r_list, np.log10(f_list_m), 1)
print(k_p,b_p,k_m,b_m)



# In[14]:


import matplotlib.pyplot as plt
import os

mum_per_pixel=1/5.5

target_folder='./txt_files/'
original_folder='./tif_files/'

filename_list=os.listdir(original_folder)
total_file=len(filename_list)
for index in range(total_file):
    filename=filename_list[index]
    if filename.endswith('.tif'):
        r_list=[]
        f_list_p=[]
        f_list_m=[]
        for r in range(7,707,7):
            RF_list_p,RF_list_m=get_statistic_per_radius(img_path=original_folder+filename,radius=r,num_times=200)
            radius_p,average_p=RF_list_average(RF_list_p)
            radius_p=radius_p*mum_per_pixel
            r_list.append(radius_p)
            if average_p==0:
                print('warning!!!!!!!!!!!!!!!!!!!!!!!! average_p zero!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
                average_p=1e-8/r
            f_list_p.append(average_p)
            radius_m,average_m=RF_list_average(RF_list_m)
            if average_m==0:
                print('warning!!!!!!!!!!!!!!!!!!!!!!!! average_m zero!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
                average_m=1e-8/r
            f_list_m.append(average_m)
            print(filename,index+1,'/',total_file,':',r/7,'/',100)
        
        log_f_list_p=np.log10(f_list_p)
        log_f_list_m=np.log10(f_list_m)
        k_p,b_p = np.polyfit(r_list, log_f_list_p, 1)
        k_m,b_m = np.polyfit(r_list, log_f_list_m, 1)

        
        files_directory=target_folder+filename[:-4]+'.csv'
        
        f=open(files_directory,'w')
        f.write('radius(um),Walls_frequency,log(Walls_frequency),Pores_frequency,log(Pores_frequency),k_Walls,b_Walls,k_Pores,b_Pores\n')
        for i in range(len(r_list)):
            if i==0:
                new_line=str(r_list[i])+','+str(f_list_p[i])+','+str(log_f_list_p[i])+','+str(f_list_m[i])+','+str(log_f_list_m[i])+','+str(k_p)+','+str(b_p)+','+str(k_m)+','+str(b_m)+'\n'
            else:
                new_line=str(r_list[i])+','+str(f_list_p[i])+','+str(log_f_list_p[i])+','+str(f_list_m[i])+','+str(log_f_list_m[i])+'\n'
            f.write(new_line)
        f.close()
        print(filename,'finished',k_p,b_p,k_m,b_m)


# In[ ]:




