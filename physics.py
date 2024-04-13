import math
#Equations:
# Gravitational Force
# Acceleration
# Velocity
GRAVITATIONAL_CONSTANT = 6.674 * 10**-11

def calcGravitationalForce (Object1mass,Object2mass,Radius1,Radius2, Location1, Location2):
    Force = GRAVITATIONAL_CONSTANT * (Object1mass * Object2mass) / (Radius1 - Radius2)**2  # F=G*(m1*m2)/r^2
    Theta = math.atan2(Location1[0]-Location2[0],Location1[1]-Location2[1])  #The angle of the objects
    Force_x = math.cos(Theta)*Force  #Horizontal Force
    Force_y = math.sin(Theta)*Force  #Vertical Force
    return [Force_x, Force_y]

def calcAcceleration (Force,Mass):
    Acceleration = Force / Mass  # a=F/m
    return Acceleration

def calcVelocity (Acceleration,Time):
    Velocity = Acceleration * Time  # v=a*t
    return Velocity


"""
Takes in a list of objects and updates the position of the object at the given index
"""
def updatePosition (Objects, Index,Time):
    #Objects is a 3d array. Each row contains descriptors for each object: [mass, radius, position, velocity]
    #Velocity is an array: [x,y]
    PrimaryObject = Objects[Index]
    Position = PrimaryObject[2]
    Velocity = PrimaryObject[3]
    SumofForces = [0,0]

    for object in Objects:
        if object == Objects[Index]:
            continue
        Force = calcGravitationalForce(PrimaryObject.mass,object.mass,PrimaryObject.radius,object.radius,PrimaryObject.position,object.position)
        SumofForces += Force

    Acceleration = calcAcceleration(SumofForces,PrimaryObject.mass)
    Velocity += calcVelocity(Acceleration,Time)
    Position += [Velocity * Time] # s = v*t

    PrimaryObject[2] = Position
    PrimaryObject[3] = Velocity
    Objects[Index] = PrimaryObject
    return Objects
