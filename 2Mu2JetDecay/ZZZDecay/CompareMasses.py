if __name__ == "__main__":
    count = 0
    with open("JesusMasses.txt") as f:
        JesusMass = f.read().splitlines()
    with open("Masses.txt") as f:
        CamMass = f.read().splitlines()

    differences = []

    for x in range(len(CamMass)):
        differences.append(abs(float(CamMass[x]) - float(JesusMass[x])))

    diffs = [x for x in differences if x > 0.001]
    print(len(diffs))
    



