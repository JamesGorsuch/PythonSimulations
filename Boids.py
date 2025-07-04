import turtle, random, math

turtle.setworldcoordinates(0, 0, 400, 400)
turtle.delay(0)
turtle.Screen().bgcolor('white')
    

class Boid(turtle.Turtle):
    def __init__(self, posx, posy, color, vx, vy, shape, _type,z, vz):
        turtle.Turtle.__init__(self)
        self.penup()
        self.speed(0)
        self.goto(posx, posy)
        self.color(color)
        self.shape(shape)
        self.vx = vx
        self.vy = vy
        self.vz = vz
        self.z = z
        self.shapesize(z,z)
        self.species = _type
        self.animate()
    
    def animate(self):
        xpos_avg = 0
        ypos_avg = 0
        zpos_avg = 0
        xvel_avg = 0
        yvel_avg = 0
        zvel_avg = 0
        neighboring_boids = 0
        close_dx = 0
        close_dy = 0
        close_dz = 0
        pred_dx = 100
        pred_dy = 100
        pred_dz = 100
        
        if self.species == 'pred':
            ownList = boidList
        if self.species == 'green':
            ownList = greenList + predList + predList2
        if self.species == 'blue':
            ownList = blueList + predList + predList2
        if self.species == 'pred2':
            ownList = boidList
        
        for OtherBoid in ownList:
            dx = self.xcor() - OtherBoid.xcor()
            dy = self.ycor() - OtherBoid.ycor()
            dz = self.z - OtherBoid.z
            
            if (abs(dx)<visual_range and abs(dy)<visual_range and abs(dz)<Zvisual_range):
                squared_distance = dx*dx + dy*dy + dz*dz
                
                if (squared_distance < (protected_range * protected_range)):
                    close_dx += self.xcor() - OtherBoid.xcor()
                    close_dy += self.ycor() - OtherBoid.ycor()
                    close_dz += self.z - OtherBoid.z
                    
                #pred avoidance
                if (OtherBoid.species == 'pred'):
                    #self.color('red')
                    pred_dx = close_dx
                    pred_dy = close_dy
                    pred_dz = close_dz
                    pred_x = OtherBoid.xcor()
                    pred_y = OtherBoid.ycor()
                    pred_z = OtherBoid.z

                #pred avoiances
                if (OtherBoid.species == 'pred2' and self.species != 'pred2' and self.species != 'pred'):
                    pred_dx = close_dx
                    pred_dy = close_dy
                    pred_dz = close_dz
                    pred_x = OtherBoid.xcor()
                    pred_y = OtherBoid.ycor()
                    pred_z = OtherBoid.z
                
                #get these ready to calc averages
                elif (squared_distance < (visual_range * visual_range)):
                    xpos_avg += OtherBoid.xcor()
                    ypos_avg += OtherBoid.ycor()
                    zpos_avg += OtherBoid.z
                    zvel_avg += OtherBoid.vz
                    xvel_avg += OtherBoid.vx
                    yvel_avg += OtherBoid.vy
                    
                    neighboring_boids += 1
                    
        if (neighboring_boids > 0):
            #calculate averages
            xpos_avg = xpos_avg/neighboring_boids 
            ypos_avg = ypos_avg/neighboring_boids
            zpos_avg = zpos_avg/neighboring_boids
            xvel_avg = xvel_avg/neighboring_boids
            yvel_avg = yvel_avg/neighboring_boids
            zvel_avg = zvel_avg/neighboring_boids
            
            #set own velocities
            self.vx = (self.vx + (xpos_avg - self.xcor())*centering_factor + (xvel_avg - self.vx)*matching_factor)   
            self.vy = (self.vy + (ypos_avg - self.ycor())*centering_factor + (yvel_avg - self.vy)*matching_factor)
            self.vz = (self.vz + (zpos_avg - self.z)*centering_factor + (zvel_avg-self.vz)*matching_factor)
               
                
              
        #avoid the other boids
        self.vx = self.vx + (close_dx*avoid_factor) 
        self.vy = self.vy + (close_dy*avoid_factor) 
        self.vz = self.vz + (close_dz*avoid_factor)
        
        #avoid the predators
        if pred_dx < pred_range and self.species != 'pred':
            if self.xcor() > pred_x:
                self.vx = self.vx + pred_avoid_factor
            if self.xcor() < pred_x:
                self.vx = self.vx - pred_avoid_factor
        if pred_dy < pred_range and self.species != 'pred':
            if self.ycor() > pred_y:
                self.vy = self.vy + pred_avoid_factor
            if self.ycor() < pred_y:
                self.vy = self.vy - pred_avoid_factor
        if pred_dz < pred_range and self.species != 'pred':
            if self.z > pred_z:
                self.vz = self.vz + Zpred_avoid_factor
            if self.z< pred_z:
                self.vz = self.vz - Zpred_avoid_factor
              
        #avoid the walls
        if self.ycor() > top_margin:
            self.vy = self.vy - turn_factor
        if self.ycor() < bottom_margin:
            self.vy = self.vy + turn_factor
        if self.xcor() > right_margin:
            self.vx = self.vx - turn_factor
        if self.xcor() < left_margin:
            self.vx = self.vx + turn_factor
        if self.z < back_margin: 
            self.vz = self.vz + turn_factor
        if self.z > front_margin:
            self.vz = self.vz - turn_factor
              
        
        speed = math.sqrt(self.vx*self.vx + self.vy*self.vy + self.vz*self.vz)   
        if speed < minspeed:
            self.vx = (self.vx/speed)*minspeed
            self.vy = (self.vy/speed)*minspeed
            self.vz = (self.vz/speed)*minspeed
        if speed > maxspeed:
            self.vx = (self.vx/speed)*maxspeed
            self.vy = (self.vy/speed)*maxspeed  
            self.vz = (self.vz/speed)*maxspeed  
              
        if self.shape == 'triangle':
            self.vx = self.vx/10
            self.vy = self.vy/10
        newx = self.xcor() + self.vx
        newy = self.ycor() + self.vy 
        newz = self.z + self.vz
        
        self.goto(newx, newy)
        self.shapesize(newz,newz)
        turtle.ontimer(self.animate, 30)

    
    
    
#starting boids
boidList = []
blueList = []
greenList = []
predList = []
predList2 = []

visual_range = 40
Zvisual_range = 40
protected_range = 8
Zprotected_range = 8
centering_factor = 0.001
matching_factor = 0.1
avoid_factor = 0.05
turn_factor = 0.5
pred_avoid_factor = 1.5
Zpred_avoid_factor = 0.5
pred_range = 5

minspeed = 3
maxspeed = 6

top_margin = 380
bottom_margin = 20
left_margin = 20
right_margin = 380
front_margin = 3
back_margin = 0.1

#bounds
def DrawBounds():
    turtle.pensize(3)
    turtle.color('black')
    turtle.pu()
    turtle.goto(0, 0)
    turtle.pd()
    turtle.goto(0, 400)
    turtle.goto(400,400)
    turtle.goto(400, 0)
    turtle.goto(0,0)
    turtle.pu()

#margins
def DrawMargins():
    turtle.color('red')
    turtle.goto(20, 20)
    turtle.pd()
    turtle.goto(20, 380)
    turtle.goto(380,380)
    turtle.goto(380, 20)
    turtle.goto(20,20)
    turtle.pu()

def SummonPred():
    xpos = random.uniform(0, 400)
    ypos = random.uniform(0, 400)
    z = random.uniform(0.1,3)
    xvel = random.uniform(-4, 4)
    yvel = random.uniform(-4, 4)
    vz = random.uniform(-1,1)
    color = random.choice(['red','darkred','red1','red2','red3','red4'])
    shape = 'triangle'
    _type = 'pred'
    z = 1
    boid = Boid(xpos, ypos, color, xvel, yvel, shape, _type, z, vz)
    boidList.append(boid)
    predList.append(boid)
    
def SummonPred2():
    xpos = random.uniform(0, 400)
    ypos = random.uniform(0, 400)
    xvel = random.uniform(-4, 4)
    yvel = random.uniform(-4, 4)
    color = random.choice(['orange','orange1','orange2','orange3','orange4'])
    shape = 'triangle'
    _type = 'pred2'
    z = 1
    boid = Boid(xpos, ypos, color, xvel, yvel, shape, _type, z)
    boidList.append(boid)
    predList2.append(boid)
    
def SummonBlue():
    xpos = random.uniform(0, 400)
    ypos = random.uniform(0, 400)
    z = random.uniform(0.1,3)
    xvel = random.uniform(-4, 4)
    yvel = random.uniform(-4, 4)
    vz = random.uniform(-1,1)
    color = random.choice(['cyan', 'cyan1', 'cyan2', 'cyan3', 'cyan4', 'aquamarine', 'aquamarine1', 'aquamarine2', 'aquamarine3', 'aquamarine4', 'darkcyan', 'darkblue'])
    shape = 'circle'
    _type = 'blue'
    
    boid = Boid(xpos, ypos, color, xvel, yvel, shape, _type, z, vz)
    boidList.append(boid)
    blueList.append(boid)
    

def SummonGreen():
    xpos = random.uniform(0, 400)
    ypos = random.uniform(0, 400)
    z = random.uniform(0.1,3)
    xvel = random.uniform(-4, 4)
    yvel = random.uniform(-4, 4)
    vz = random.uniform(-1,1)
    color = random.choice(['green', 'green1','green2', 'green3', 'green4'])
    shape = 'circle'
    _type = 'green'
    boid = Boid(xpos, ypos, color, xvel, yvel, shape, _type,z, vz)
    boidList.append(boid)
    greenList.append(boid)
    
for i in range(15):
    SummonBlue()
    #SummonGreen()

for i in range(1):   
    SummonPred()
    
for i in range(0):
    SummonPred2()



turtle.mainloop()
