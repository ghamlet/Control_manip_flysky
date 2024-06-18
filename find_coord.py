from read_serial import MoveToPointCallback

file = open("valid_coord.txt", "a+")

for x in range(600):
    for y in range(600):
        for z in range(600):

            if MoveToPointCallback(x, y, z):
                file.write(str("\n" +str(x) +  " " + str(y) + " " + str(z)))              

file.close()