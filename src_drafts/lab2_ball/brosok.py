import math
#===============================
#   Calculator(Ax, Ay, Vx, Vy, dt, x, y)
#   действия в зависимости от того есть ли столкновения
#===============================
def Calculator(Ax, Ay, Vx, Vy, dt, x, y):
    if WillBounce(Ax, Ay,x,y,Vx,Vy,dt)!=False:
        return WillBounce(Ax, Ay,x,y,Vx,Vy,dt)
    return Rate(Ax,Ay, Vx,Vy, x,y, dt)

#===============================
#   WillBounce(x,y,Vx,Vy)
#  проверка на возможное столкновение 
#   модель: смещение на малом времени есть отрезок
#   если есть пересечения с стенкой, то есть и столкновение
#===============================
def WillBounce(Ax, Ay,x,y,Vx,Vy,dt):
    from shapely.geometry import LineString
    global every_obstacle
    for elem in every_obstacle:
        line = LineString([(elem.Xstart, elem.Ystart), (elem.Xend, elem.Yend)]) # стенка
        other = LineString([(x,y), (x+Vx*dt,y+Vy*dt)]) # генерация перемещения без столкновения
        if line.intersects(other):
            alpha=elem.angle 
            beta=math.atan(Vy/(Vx+1e-5)) # касательная к скорости
            angle=math.pi/2-alpha+beta # угол между касательной и препятствием
            
            Velocity=math.sqrt(Vx**2+Vy**2)
            VelCollinear=Velocity*math.sin(angle)
            VelPerp=Velocity*math.cos(angle)*(1-elem.BRate) # посчитали параллельную и перп. части, перп. часть отражается
            
            Vy=VelCollinear*math.sin(alpha)+VelPerp*math.cos(alpha)
            Vx=VelCollinear*math.cos(alpha)+VelPerp*math.sin(alpha)
            return Rate(Ax,Ay,Vx,Vy, x,y, dt)   
    return False #если нет пересечения

#===============================
#   Rate(Ax,Ay, Vx,Vy, x,y, dt)
#  Расчёт скорости изменения величин (уравнения движения):
#   V' = A      ( dV = A*dt )
#   X' = V      ( dx = V*dt )
#===============================
def Rate(Ax,Ay, Vx,Vy, x,y, dt):
    dVx = Ax*dt
    dVy = Ay*dt
    dx  = Vx*dt
    dy  = Vy*dt
    return  Vx, Vy, dVx, dVy, dx, dy


def main():
    # TRAJECTORY

    #== Параметры задачи. Всё в СИ, углы в градусах ==
    Vo = 17          
    angle_deg = 60
    dt = 1e-3      

    g = 9.8155              # ускорение свободного падения
    Xo = 0        # координаты точки броска
    Yo = 0              #   ось икс вправо, ось игрек влево
    L =  90              # моделируемая длина
    BRate = 0.2    # доля скорости, теряющаяся при ударе о препятствие (от 0 до 1)
    
    # стенки
    class Obstacles():
        all_obstacles=[] # список всех препятствий для обработки
        def __init__(self,Xstart,Xend,Ystart,Yend,BRate,name):
            self.Xstart=Xstart 
            self.Xend=Xend
            self.Ystart=Ystart
            self.Yend=Yend
            self.name=name
            self.BRate=BRate
            self.tangent=(Yend-Ystart)/(Xend-Xstart+1e-5)
            self.angle=math.atan(self.tangent)
            
            Obstacles.all_obstacles.append(self)
            
    obstacle1=Obstacles(0,L,-1e-10,-1e-10,0.2,'Поверхность Земли')
    # здесь задаются другие стенки
    obstacle2=Obstacles(0,L,9.26,2,0.1,'Потолок')
    obstacle3=Obstacles(20,81,7,-2,0,'Стенка')

    global every_obstacle
    every_obstacle=Obstacles.all_obstacles

    #== Изменяющиеся переменные ==
    Ax = 0              # ускорение
    Ay = -g

    phi = angle_deg*math.pi/180
    Vx = Vo*math.cos(phi)    # скорость
    Vy = Vo*math.sin(phi)
    x = Xo              # координаты
    y = Yo

    Xsav = []           # списки сохранённых координат
    Ysav = []           #   - для отрисовки траектории


    while x<L and len(Xsav)<10000:
        Xsav.append(x)
        Ysav.append(y)
        deltas=list(Calculator(Ax, Ay, Vx, Vy, dt, x, y)) # каждую итерацию пересчитываем скорости
        Vx, Vy, x, y = deltas[0]+deltas[2],deltas[1]+deltas[3], x+deltas[4], y+deltas[5]

    import matplotlib.pyplot as PLT
    import numpy as np
    import matplotlib.animation as animation

    fig = PLT.figure()
    ax = PLT.axes(xlim=(-10, 100), ylim=(-1, 10))
    line, = ax.plot([], [], lw=3)

    def init():
        line.set_data([], [])
        return line,
    def animate(i):
        x = Xsav[:i]
        y = Ysav[:i]
        line.set_data(x, y)
        return line,

    anim = animation.FuncAnimation(fig, animate, init_func=init, frames=len(Xsav), interval=2, blit=True)
    PLT.plot(Xsav, Ysav, label="Траектория тела") # рисуем траекторию тела
    for elem in Obstacles.all_obstacles:
        PLT.plot([elem.Xstart,elem.Xend],[elem.Ystart,elem.Yend],label=elem.name) # рисуем препятствия
    PLT.legend()
    PLT.show()                                    # показать окно matplotlib
main()
