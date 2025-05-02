'''
DiseaseAnalysis.py
Developed by Robert Walsh and Josh Sapira

This program file contains all the needed information on the creation of an advanced SIRD model with quarantine functionality.
'''


'''
This is a population, made up of N people, with a beta infection rate, a gamma recovery rate, and a mu death rate.
In addition, there is a crossInfectivity value which indicates the percentage of people who travel from one population to another.
We use this value to do multi-population analysis.
We also keep track of time for quarantine purposes and whether or not a population contains a "patient zero"
The quarantine is kept track of by using a dictionary which contains the number of still living infected on a day by day basis
Quarantine leak represents delinquency. The higher the amount, the fewer people actually follow quarantine.
Quarantine length represents how long an infected individual has before they can achieve full infectivity
'''
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

    '''
    This function is used to simulate SIRD for a population. We first find the total number of active infected (those out of quarantine or not listening)
    Then we go through each quarantine day to reduce the number of infected based on recovery and death rates
    We then determine the new infected, and add them to a new quarantine section, marking the day in which they can leave
    '''
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

    '''
    This function helps us find out who is following the quarantine and who is out of quarantine.
    If the day is less than the current date, the infected are free, otherwise infected are limited by who ignores quarantine.
    '''
    def GetActiveInfected(self):
        # keep a tally of infected who are out of quarantine or choose to ignore quarantine
        activeInfected = 0
        for day in self.quarantine.keys():
            if day <= self.time:
                activeInfected += self.quarantine[day]
            else:
                activeInfected += self.quarantine[day] * self.quarantineLeak

        return activeInfected

    '''
    A vaccination method, moves the susceptible to the recovered/immune group based on vaccine efficiency
    '''
    def apply_vaccination(self, num_vaccinated, efficacy=1.0):
        vaccinated = min(num_vaccinated, self.S)
        effective_vaccinated = efficacy * vaccinated
        self.S -= vaccinated
        self.R += effective_vaccinated

'''
This function takes a group of infected populations and applies cross-infectivity to them.
Each day, some percentage of people visit another community. If the infected are among them, then they also infect the other communities.
'''
# when multiple groups connect, they infect one another
def crossInfect(pops):

    activeInfected = []

    for pop in pops:
        activeInfected.append(pop.GetActiveInfected())

    changeI = []

    for i in range(len(pops)):
        change = 0
        for j in range(len(pops)):
            if i != j:
                change += (pops[i].S * pops[j].crossInfectivity * activeInfected[j])/pops[i].N

        changeI.append(change)

    for i in range(len(changeI)):
        pops[i].S -= changeI[i]
        pops[i].I += changeI[i]



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