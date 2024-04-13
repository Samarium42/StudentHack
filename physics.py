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
def updatePosition (Objects, Index, Time=1):
    # Objects is a list of objects. Each object has properties: mass, radius, position, velocity
    # Position and Velocity are now 3D vectors: [x,y,z]
    PrimaryObject = Objects[Index]
    Position = PrimaryObject.attributes.position
    Velocity = PrimaryObject.attributes.velocity
    SumofForces = [0,0,0] 

    for object in Objects:
        if object == Objects[Index]:
            continue
        Force = calcGravitationalForce(PrimaryObject.attributes.mass, object.attributes.mass, PrimaryObject.attributes.radius, object.attributes.radius, PrimaryObject.attributes.position, object.attributes.position)
        SumofForces = [SumofForces[i] + Force[i] for i in range(3)]  # Update each component of the force

    # Update the velocity and position of the primary object
    Acceleration = [force / PrimaryObject.attributes.mass for force in SumofForces]  # F = ma, so a = F/m
    NewVelocity = [Velocity[i] + Acceleration[i] * Time for i in range(3)]  # v = u + at
    NewPosition = [Position[i] + NewVelocity[i] * Time for i in range(3)]  # s = ut + 1/2at^2

    PrimaryObject.attributes.velocity = NewVelocity
    PrimaryObject.attributes.position = NewPosition

    Objects[Index] = PrimaryObject


def modelCollisions (Objects, Index1, Index2):
    #Objects is a 3d array. Each row contains descriptors for each object: [mass, radius, position, velocity]
    #Velocity is an array: [x,y]
    Object1 = Objects[Index1]
    Object2 = Objects[Index2]
    Velocity1 = Object1.attributes.velocity
    Velocity2 = Object2.attributes.velocity

    #Calculating the new velocities of the objects after the collision
    NewVelocity1 = (Object1.attributes.mass - Object2.attributes.mass) / (Object1.attributes.mass + Object2.attributes.mass) * Velocity1 + (2 * Object2.attributes.mass) / (Object1.attributes.mass + Object2.attributes.mass) * Velocity2  #v1' = (m1-m2)/(m1+m2)*v1 + (2*m2)/(m1+m2)*v2
    NewVelocity2 = (Object2.attributes.mass - Object1.attributes.mass) / (Object1.attributes.mass + Object2.attributes.mass) * Velocity2 + (2 * Object1.attributes.mass) / (Object1.attributes.mass + Object2.attributes.mass) * Velocity1  #v2' = (m2-m1)/(m1+m2)*v2 + (2*m1)/(m1+m2)*v1

    Object1.attributes.velocity = NewVelocity1
    Object2.attributes.velocity = NewVelocity2

    Objects[Index1] = Object1
    Objects[Index2] = Object2

    return Objects

def updateAllObjects (Objects, Time=1):
    for i in range(len(Objects)):
        updatePosition(Objects, i, Time)
        """
        ADD CHECK THAT OBJECTS ARE NOT OUT OF BOUNDS SUCH AS BELOW
        """
        if (Objects[i].attributes.position[0] < 0 or Objects[i].attributes.position[1] < 0 or Objects[i].attributes.position[2] < 0):
            Objects.pop(i)
            i -= 1
        
        """CHECK FOR COLLISIONS"""
        for j in range(i+1, len(Objects)):
            if (math.sqrt((Objects[i].attributes.position[0] - Objects[j].attributes.position[0])**2 + (Objects[i].attributes.position[1] - Objects[j].attributes.position[1])**2 + (Objects[i].attributes.position[2] - Objects[j].attributes.position[2])**2) < Objects[i].attributes.radius + Objects[j].attributes.radius):
                modelCollisions(Objects, i, j)
    return Objects
