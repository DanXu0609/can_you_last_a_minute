import random

WIDTH = 800
HEIGHT = 600
'''
0 -> right
1 -> left
2 -> bottom
3 -> top
'''
def generateLocation(choice):
    match choice:
        case 0:
            return random.randint(WIDTH + 1, WIDTH+5), random.randint(-10,HEIGHT+10)
        case 1:
            return random.randint(-10,-5), random.randint(-10,HEIGHT+10)
        case 2:
            return random.randint(-10,WIDTH+10),random.randint(HEIGHT+1,HEIGHT+5)
        case 3:
            return random.randint(-10,WIDTH+10),random.randint(-10,-5)

def determineSpeed(choice, slope):
    slopeAdjust = 0.1 * slope if abs(slope) > 50 else 0.05 * slope if abs(slope) > 100 else 0.01 * slope if abs(slope) > 200 else slope
    if choice == 0:
        speedx = random.randint(-6,-2)
        if slope == 0.0:
            return speedx, 0
        else:
            return speedx, -1 * slopeAdjust * speedx
    elif choice == 1:
        speedx = random.randint(2,6)
        if slope == 0.0:
            return speedx, 0
        else:
            return speedx, -1 * slopeAdjust * speedx
    elif choice == 2:
        speedy = random.randint(-6,-2)
        if slope == 0.0:
            return 0, speedy
        else:
            return  -1 * slopeAdjust* speedy, speedy 
    else:
        speedy = random.randint(2,6)
        if slope == 0.0:
            return 0, speedy
        else:
            return  -1 * slopeAdjust * speedy, speedy

    