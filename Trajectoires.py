from Regles import LoiGravitation

def calculate(bodies, stepSize, stepSpeed, steps):
    positions = [bodies]
    for i in range(steps):
        LoiGravitation.apply()
        positions.append(LoiGravitation.apply(positions[-1], stepsize))
    return(positions)


            

        