# import matplotlib.pyplot as plt
class Population:
    def __init__(self, N, beta, gamma, mu, crossInfectivity, infected=True, quarantineLeak = 1.0, quarantineLength = 1):
        self.N = N
        self.beta = beta
        self.gamma = gamma
        self.mu = mu
        self.crossInfectivity = crossInfectivity

        self.time = 0

        # if a population begins infected, 1 person will have infection
        if infected:
            self.S = N - 1
            self.I = 1
        else:
            self.S = N
            self.I = 0

        self.R = 0
        self.D = 0

        # use for quarantine calculations

        if infected:
            self.quarantine = {0: 1}
        else:
            self.quarantine = {0: 0}

        # leak represents the proportion of people who do not follow quarantine
        self.quarantineLeak = quarantineLeak

        # how long does an infected remain in quarantine
        self.quarantineLength = quarantineLength

    def SIRD(self):

        # keep a tally of infected who are out of quarantine or choose to ignore quarantine
        activeInfected = self.GetActiveInfected()

        for day in self.quarantine.keys():
            # while we are here, update infected populations by day. Infected in quarantine die or recover still
            self.quarantine[day] += -(self.gamma * self.quarantine[day]) - (self.mu * self.quarantine[day])

        newInfected = (self.beta * self.S * activeInfected) / self.N
        recoveredInfected = self.gamma * self.I
        deadInfected = self.mu * self.I

        changeS = -newInfected
        changeI = newInfected - recoveredInfected - deadInfected
        changeR = recoveredInfected
        changeD = deadInfected

        self.time += 1
        self.quarantine[self.time + self.quarantineLength] = newInfected

        self.S += changeS
        self.I += changeI
        self.R += changeR
        self.D += changeD

    def GetActiveInfected(self):
        # keep a tally of infected who are out of quarantine or choose to ignore quarantine
        activeInfected = 0
        for day in self.quarantine.keys():
            if day <= self.time:
                activeInfected += self.quarantine[day]
            else:
                activeInfected += self.quarantine[day] * self.quarantineLeak

        return activeInfected

    def apply_vaccination(self, num_vaccinated, efficacy=1.0):
        vaccinated = min(num_vaccinated, self.S)
        effective_vaccinated = efficacy * vaccinated
        self.S -= vaccinated
        self.R += effective_vaccinated

# when two groups connect, they infect one another
def crossInfect(pop1, pop2):

    # calculate the active infected
    activeInfected1 = pop1.GetActiveInfected()
    activeInfected2 = pop2.GetActiveInfected()

    changeI1 = (pop1.S * pop2.crossInfectivity * activeInfected2)/pop1.N

    changeI2 = (pop2.S * pop1.crossInfectivity * activeInfected1) / pop2.N

    pop1.S -= changeI1
    pop1.I += changeI1

    pop2.S -= changeI2
    pop2.I += changeI2



# group1 = Population(10000, 0.5, 0.1, 0.01, 0.1, True, 0.25, 21)
#
# group2 = Population(1000, 0.3, 0.1, 0.01, 0.1, True, 0.25, 21)
#
# S = [group1.S + group2.S]
# I = [group1.I + group2.I]
# R = [group1.R + group2.R]
# D = [group1.D + group2.D]
#
# for i in range(100):
#     group1.SIRD()
#     group2.SIRD()
#
#     crossInfect(group1, group2)
#
#     S.append(group1.S + group2.S)
#     I.append(group1.I + group2.I)
#     R.append(group1.R + group2.R)
#     D.append(group1.D + group2.D)
#
# plt.plot(S, label="S")
# plt.plot(I, label="I")
# plt.plot(R, label="R")
# plt.plot(D, label="D")
# plt.xlabel("Time")
# plt.ylabel("Populations")
# plt.title("SIRD MODEL SIMULATION")
# plt.legend()
# plt.show()