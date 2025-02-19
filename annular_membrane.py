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
    return sci.jv(0,x)*sci.yv(0,2*x)-sci.yv(0,x)*sci.jv(0,2*x)


def n_eigen_function(eigen_values,n,x):
    return sci.jv(0,eigen_values[n]*x)-(sci.jv(0,eigen_values[n])/sci.yv(0,eigen_values[n]))*sci.yv(0,eigen_values[n]*x)

def n_coef(eigen_values,n):

    f = lambda x : n_eigen_function(eigen_values,n,x)
    f1=lambda x : f(x)*x*(x-1)*(2-x)
    a=quad(f1,1,2)[0]
    f2=lambda x : x*f(x)**2
    b=quad(f2,1,2)[0]
    sol=a/b
    return sol

eigen_values=find_zeros(f,0,200)
coefs=[n_coef(eigen_values,n) for n in range(0,200)]

def u(r,t):
    a=0
    for n in range(0,len(eigen_values)):
        a=a+coefs[n]*mb.cos(eigen_values[n]*t)*n_eigen_function(eigen_values,n,r)
    return a

    


fig, ax = plt.subplots(subplot_kw=dict(projection='3d'))

plt.title("Wave equation\nannular membrane",bbox=dict(facecolor='none', edgecolor='k', pad=5.0),size='x-large')

ax.set_xlim(-2.2,2.2)
ax.set_ylim(-2.2,2.2)
ax.set_zlim(-0.5,0.5)
ax.set_box_aspect((1, 1, 0.5)) 

imagen=Image.open('./EDP1.png')
imagen_array=np.array(imagen)

ax_imagen = fig.add_axes([-0.025,0.7,0.4,0.2])
ax_imagen.imshow(imagen)
ax_imagen.axis('off')





arg=np.arange(0,2*np.pi,0.01)
r=np.arange(1,2,0.05)
A,R=np.meshgrid(arg,r)

#Establezco los segundos que queremos que dure la animación y los frames por segundo:
s=40
fps=30

#Añado la ruta de ffmpeg.exe, le ponemos nombre y creador al video, y establecemos los fps.
plt.rcParams['animation.ffmpeg_path'] = 'Your ffmpeg.exe directory goes here'
metadata=dict(tittle='Movie',artist='Fran')
writer=FFMpegWriter(fps=30,metadata=metadata)


start = time()


if not os.path.exists("./animaciones"):
    os.makedirs('animaciones')

with writer.saving(fig,"./animaciones/membrane.mp4",250):
    times=np.linspace(0,s,s*fps)
    i=0
   
    for t in times:
        i=i+1
        print(str(i)+'/'+str(len(times)))

        temporal=ax.plot_surface(R*np.cos(A),R*np.sin(A),u(R,t),alpha=1,color='#a5f4f3', rstride=4, cstride=15, edgecolors='k')
        temporary=plt.suptitle('t = '+str('{0:.2f}'.format(round(t,2)))+' s',y=0.85, color='k',size='large',bbox=dict(facecolor='w', edgecolor='k', boxstyle='round'))
        writer.grab_frame()
        temporal.remove()



print(time() - start)







