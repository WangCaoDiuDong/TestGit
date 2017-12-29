#!/usr/bin/env.python
# -*- coding:utf-8 -*-
import time
import random
import math

people = [('Seymout', 'BOS'), ('Franny', 'DAL'), ('Zooey', 'CAK'),
          ('Walt', 'MIA'), ('Buddy', 'ORD'), ('LES', 'OMA')]


# LaGuarddia airport in New York
destination = 'LGA'

flights = {}
for line in open('schedule.txt'):
    origin, dest, depart, arrive, price = line.strip().split(',')
    flights.setdefault((origin, dest), [])

    # Add details to the list of possible flights
    flights[(origin, dest)].append((depart, arrive, int(price)))


def getminutes(t):
    x = time.strptime(t, "%H:%M")
    return x[3]*60+x[4]

def printschedule(r):
    for d in range(0, int(len(r)/2)):
        name = people[d][0]
        origin = people[d][1]
        out = flights[(origin, destination)][r[2*d]]
        ret = flights[(destination, origin)][r[2*d+1]]
        print('%10s%10s %5s-%5s $%3s %5s-%5s &%3s' % (name, origin, out[0], out[1], out[2], ret[0], ret[1], ret[2]))

def schedulecost(sol):
    totalprice = 0
    latestarrival = 0
    earliestdep = 24*60
    for d in range(int(len(sol)/2)):
        # Get the inbound and outbound flights
        origin = people[d][1]
        outbound = flights[(origin, destination)][int(sol[2*d])]
        returnf = flights[(destination, origin)][int(sol[2*d+1])]

        # Total price is the price of all outbound and return flights
        totalprice += outbound[2]
        totalprice += returnf[2]

        # Track the latest arrival and earliest departure
        if latestarrival < getminutes(outbound[1]):
            latestarrival = getminutes(outbound[1])
        if earliestdep > getminutes(returnf[0]):
            earliestdep = getminutes(returnf[0])

    # Every person must wait at the airport until the latest person arrives.
    # They also must arrive ath the time and wait for their flights.
    totalwait = 0
    for d in range(int(len(sol)/2)):
        origin = people[d][1]
        outbound = flights[(origin, destination)][int(sol[2*d])]
        returnf = flights[(destination, origin)][int(sol[2*d+1])]
        totalwait += latestarrival-getminutes(outbound[1])
        totalwait += getminutes(returnf[0]) - earliestdep

    # Does this solution require an extra day of car rental? That'll be $50!
    if latestarrival < earliestdep:
        totalprice += 5

    return totalprice+totalwait

#
def randomoptimize(domain, costf):
    best = 999999999
    bestr = None
    for i in range(0, 1000):
        # Create a random solution
        r = [float(random.randint(domain[i][0], domain[i][1]))
             for i in range(len(domain))]
        # Get the cost
        cost = costf(r)

        # Compare it to the best one so far
        if cost < best:
            best = cost
            bestr = r

    return r

s=[4, 4, 4, 2, 2, 6, 5, 4, 5, 6, 7, 0]
schedulecost(s)
#domain=[(0,9)]*(len(people)*2)
#randomoptimize(domain, schedulecost)
