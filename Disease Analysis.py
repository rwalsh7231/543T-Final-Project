import matplotlib.pyplot as plt


class Population:
    def __init__(self, N, beta, gamma, mu, crossInfectivity):
        self.N = N
        self.beta = beta
        self.gamma = gamma
        self.mu = mu
        self.crossInfectivity = crossInfectivity

        self.S = N - 1
        self.I = 1
        self.R = 0
        self.D = 0

    def SIRD(self):
        changeS = -(self.beta * self.S * self.I) / self.N
        changeI = ((self.beta * self.S * self.I) / self.N) - (self.gamma * self.I) - (self.mu * self.I)
        changeR = self.gamma * self.I
        changeD = self.mu * self.I

        self.S += changeS
        self.I += changeI
        self.R += changeR
        self.D += changeD

# when two groups connect, they infect one another
def crossInfect(pop1, pop2):
    changeI1 = (pop1.S * pop2.crossInfectivity * pop2.I)/pop1.N

    changeI2 = (pop2.S * pop1.crossInfectivity * pop1.I) / pop2.N

    pop1.S -= changeI1
    pop1.I += changeI1

    pop2.S -= changeI2
    pop2.I += changeI2



group1 = Population(10000, 0.5, 0.1, 0.01, 0.1)

group2 = Population(1000, 0.3, 0.1, 0.01, 0.1)

S = [group1.S + group2.S]
I = [group1.I + group2.I]
R = [group1.R + group2.R]
D = [group1.D + group2.D]

for i in range(100):
    group1.SIRD()
    group2.SIRD()

    crossInfect(group1, group2)

    S.append(group1.S + group2.S)
    I.append(group1.I + group2.I)
    R.append(group1.R + group2.R)
    D.append(group1.D + group2.D)

plt.plot(S, label="S")
plt.plot(I, label="I")
plt.plot(R, label="R")
plt.plot(D, label="D")
plt.xlabel("Time")
plt.ylabel("Populations")
plt.title("SIRD MODEL SIMULATION")
plt.legend()
plt.show()