import matplotlib.pyplot as plt
import scipy.special as sci
import numpy as np
from scipy.optimize import fsolve
from scipy.integrate import quad
import math as mb
import matplotlib.pyplot as  plt
from matplotlib.animation import FFMpegWriter
import os
from time import time
from PIL import Image



def intervals_zeros2(func,a,b):
    seq=np.arange(a,b,0.02)
    intervals=[]
    for i in range(0,len(seq)-1):
        sign_test=func(seq[i])*func(seq[i+1])
        if sign_test<0:
            intervals.append([seq[i],seq[i+1]])
    return intervals


def intervals_zeros(func,a,n):
    intervals=[]
    while len(intervals)<n:
        b=a+0.02
        sign_test=func(a)*func(b)
        if sign_test<0:
            intervals.append([a,b])
        a=b
    return intervals


def find_zeros(func,a,n):
    intervals=intervals_zeros(func,a,n)
    list_zeros=[]
    for i in range(0,len(intervals)):
        interval=intervals[i]
        x0=(interval[0]+interval[1])/2
        sol=fsolve(func,x0)
        list_zeros.append(sol[0])
    return list_zeros


def f(x):
    return sci.jv(0,x)



eigen_value=find_zeros(f,0,2)[1]


def u(r,t):
    return -np.cos(eigen_value*t)*sci.jv(0,eigen_value*r)

    


fig, ax = plt.subplots(subplot_kw=dict(projection='3d'))

plt.title("Wave equation\ncircular membrane",bbox=dict(facecolor='none', edgecolor='k', pad=5.0),size='x-large')

ax.set_xlim(-1.2,1.2)
ax.set_ylim(-1.2,1.2)
ax.set_zlim(-1,1)
ax.set_box_aspect((1, 1, 0.25))
ax.set_zticks([-1,0,1]) 

imagen=Image.open('./EDP2.png')
imagen_array=np.array(imagen)

ax_imagen = fig.add_axes([-0.025,0.7,0.4,0.2])
ax_imagen.imshow(imagen)
ax_imagen.axis('off')





arg=np.arange(0,2*np.pi,0.01)
r=np.arange(0,1,0.05)
A,R=np.meshgrid(arg,r)


s=40
fps=30


plt.rcParams['animation.ffmpeg_path'] = 'D:\\Fran\\python\\Astronomía\\ffmpeg-2024-11-28-git-bc991ca048-full_build\\bin\\ffmpeg.exe'
metadata=dict(tittle='Movie',artist='Fran')
writer=FFMpegWriter(fps=30,metadata=metadata)




start = time()


if not os.path.exists("./animaciones"):
    os.makedirs('animaciones')

with writer.saving(fig,"./animaciones/membrane2.mp4",250):

    times=np.linspace(0,s,s*fps)
    i=0
   
    for t in times:
        i=i+1
        print(str(i)+'/'+str(len(times)))

        temporal=ax.plot_surface(R*np.cos(A),R*np.sin(A),u(R,t),alpha=1,color='#a5f4f3', rstride=4, cstride=40, edgecolors='k')
        temporary=plt.suptitle('t = '+str('{0:.2f}'.format(round(t,2)))+' s',y=0.85, color='k',size='large',bbox=dict(facecolor='w', edgecolor='k', boxstyle='round'))
        writer.grab_frame()
        temporal.remove()



print(time() - start)







