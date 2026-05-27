import turtle
t=turtle.Turtle()
t.speed(1)
t.pensize(30)

t.pencolor("red")

for i in range(3):
    # if i==1:
    #      t.circle(40,60)
    #      continue
    t.circle(50,60)
    t.circle(-50,60)
    if(i==2):
         t.circle(50,30)
    
# t.left(90)
t.forward(25)
t.circle(20,180)
# t.forward(50)
t.forward(25)

turtle.done()