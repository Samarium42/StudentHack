import math
#Equations:
# Gravitational Force
# Acceleration
# Velocity
# Momentum/Direction After Collisions

GRAVITATIONAL_CONSTANT = 6.674 * 10**-11

def calcGravitationalForce (Object1mass, Object2mass, Radius1, Radius2, Location1, Location2):
    Distance = math.sqrt((Location1[0] - Location2[0])**2 + (Location1[1] - Location2[1])**2 + (Location1[2] - Location2[2])**2)
    ForceMagnitude = GRAVITATIONAL_CONSTANT * (Object1mass * Object2mass) / Distance**2  # F=G*(m1*m2)/r^2
    Direction = [(Location2[i] - Location1[i]) / Distance for i in range(len(Location1))]  # Direction of the force
    Force = [ForceMagnitude * direction for direction in Direction]  # Force ratio-ed in each direction
    return Force

def calcAcceleration (Force,Mass):
    Acceleration = Force / Mass  # a=F/m
    return Acceleration

def calcVelocity (Acceleration,Time):
    Velocity = Acceleration * Time  # v=a*t
    return Velocity


"""
Takes in a list of objects and updates the position of the object at the given index
"""
def updatePosition (Objects, Index, Time):
    # Objects is a list of objects. Each object has properties: mass, radius, position, velocity
    # Position and Velocity are now 3D vectors: [x,y,z]
    PrimaryObject = Objects[Index]
    Position = PrimaryObject.position
    Velocity = PrimaryObject.velocity
    SumofForces = [0,0,0] 

    for object in Objects:
        if object == Objects[Index]:
            continue
        Force = calcGravitationalForce(PrimaryObject.mass, object.mass, PrimaryObject.radius, object.radius, PrimaryObject.position, object.position)
        SumofForces = [SumofForces[i] + Force[i] for i in range(3)]  # Update each component of the force

    # Update the velocity and position of the primary object
    Acceleration = [force / PrimaryObject.mass for force in SumofForces]  # F = ma, so a = F/m
    NewVelocity = [Velocity[i] + Acceleration[i] * Time for i in range(3)]  # v = u + at
    NewPosition = [Position[i] + NewVelocity[i] * Time for i in range(3)]  # s = ut + 1/2at^2

    PrimaryObject.velocity = NewVelocity
    PrimaryObject.position = NewPosition

    Objects[Index] = PrimaryObject


def modelCollisions (Objects, Index1, Index2):
    #Objects is a 3d array. Each row contains descriptors for each object: [mass, radius, position, velocity]
    #Velocity is an array: [x,y]
    Object1 = Objects[Index1]
    Object2 = Objects[Index2]
    Velocity1 = Object1.velocity
    Velocity2 = Object2.velocity

    #Calculating the new velocities of the objects after the collision
    NewVelocity1 = (Object1.mass - Object2.mass) / (Object1.mass + Object2.mass) * Velocity1 + (2 * Object2.mass) / (Object1.mass + Object2.mass) * Velocity2  #v1' = (m1-m2)/(m1+m2)*v1 + (2*m2)/(m1+m2)*v2
    NewVelocity2 = (Object2.mass - Object1.mass) / (Object1.mass + Object2.mass) * Velocity2 + (2 * Object1.mass) / (Object1.mass + Object2.mass) * Velocity1  #v2' = (m2-m1)/(m1+m2)*v2 + (2*m1)/(m1+m2)*v1

    Object1.velocity = NewVelocity1
    Object2.velocity = NewVelocity2

    Objects[Index1] = Object1
    Objects[Index2] = Object2

    return Objects