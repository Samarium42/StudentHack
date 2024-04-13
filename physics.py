import math
#Equations:
# Gravitational Force
# Acceleration
# Velocity
# Momentum/Direction After Collisions

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


def modelCollisions (Objects, Index1, Index2):
    #Objects is a 3d array. Each row contains descriptors for each object: [mass, radius, position, velocity]
    #Velocity is an array: [x,y]
    Object1 = Objects[Index1]
    Object2 = Objects[Index2]
    Velocity1 = Object1[3]
    Velocity2 = Object2[3]

    #Calculating the new velocities of the objects after the collision
    NewVelocity1 = (Object1.mass - Object2.mass) / (Object1.mass + Object2.mass) * Velocity1 + (2 * Object2.mass) / (Object1.mass + Object2.mass) * Velocity2  #v1' = (m1-m2)/(m1+m2)*v1 + (2*m2)/(m1+m2)*v2
    NewVelocity2 = (Object2.mass - Object1.mass) / (Object1.mass + Object2.mass) * Velocity2 + (2 * Object1.mass) / (Object1.mass + Object2.mass) * Velocity1  #v2' = (m2-m1)/(m1+m2)*v2 + (2*m1)/(m1+m2)*v1

    Object1[3] = NewVelocity1
    Object2[3] = NewVelocity2

    Objects[Index1] = Object1
    Objects[Index2] = Object2

    return Objects

def kineticEnergy (Objects):
    #Objects is a 3d array. Each row contains descriptors for each object: [mass, radius, position, velocity]
    #Velocity is an array: [x,y]
    TotalKineticEnergy = 0
    for object in Objects:
        Velocity = object[3]
        KineticEnergy = 0.5 * object.mass * (Velocity[0]**2 + Velocity[1]**2)  # KE = 0.5*m*v^2
        TotalKineticEnergy += KineticEnergy
    return TotalKineticEnergy