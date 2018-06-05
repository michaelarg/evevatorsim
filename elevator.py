import sys,os
import itertools
import operator
import collections
from scipy.stats import truncnorm
import numpy as np

import matplotlib.animation as animation

from collections import Counter

class Lift:
    newid = itertools.count().next
    global count
    def __init__(self):
        self.id = Lift.newid()
        self.maxcap = 20
        self.occup = 0
        self.currentfloor = 0
        self.active = 0
        self.doortime = 5
        self.liftopentime = 3
        self.floortime = 5
        self.inlift = [] #this is a person agent.
        self.liftseccount = 0
        self.flr = []
        self.transition = 0 #Bool
        self.atfloor = 0 #Bool yes or no
        self.trips = 0
        self.triptime = []
        self.timedown = []
        self.unqfloors = []
        print "Lift {} has been created".format(self.id)

    #I have two agents - they want to travel together, how am I best to say these pairs must travel together

    def enterme(self):
        global gfloor
        global liftlist
        print "LIFT ENTRY FUNCTION for Lift {} been called".format(self.id)
        global agentlist

        #print "nothing after this??"
        

        #This should be the id of the lift with the least amount of people in it
       
       # [x for x in liftlist if x.active == 0 and x.currentfloor == 0 ] )
        
        if len(gfloor) != 0:
            print ([len(val.inlift) for idx,val in enumerate(liftlist) ])
            minlift = np.argmin([len(val.inlift) for idx,val in enumerate(liftlist) ])
            print "min lift", minlift

            if self.id != minlift:
                print "Person goes for lift with least amount of people in it!"
                return
            
            for per in gfloor: #unfortunately this can only put this lot of gfloor in one lift.
                #YOU ARE ITERATING THROUGH A GLOBAL VARIABLE IN A PARTICULAR INSTANCE OF AN OBJECT ->
                #What does this mean? Persons on Floor <------ Lift 1 to capacity and then Lift 2 object can take from Floor,
                #but we want it to be as if Person can walk into a different lift at the same time.
                #Attempted solution - control capacities, break from loop to engage next Lift object -- > seems like it would be alot slower.

                
                
                
                #self.id == [idx for idx, val in enumerate(self.inlift) if val == min(self.inlift) ][0]

                #you can actually start each lift instance with a fake person

                if len(self.inlift) == 0: #Every lift should hit this once!
                    print "Person {} entered lift {} which is empty right --> {} should be zero".format(per, self.id, len(self.inlift))
                    self.inlift.append(per)
                    #print "A person entered lift {}".format(self.id)
                    break
                                                                            #Not correct you are taking the min of the inlift value wtf. it needs to be the lift list.append liftlist global inlift
                elif len(self.inlift) < self.maxcap and len(self.inlift) != 0: #and len(gfloor) != 0:

                #What is going on here?

                    self.inlift.append(per)
                    self.occup +=1
                    print "Person {} entered lift {} which has --> {} in it".format(per, self.id, len(self.inlift))
                    break
     
                elif len(self.inlift) == self.maxcap:
                    print "Lift {} is at capacity!".format(self.id)
                    break

                elif len(per) == 0:
                    print "No one in that group"
                
                else:
                    print "No conditions executed - you are wrong"

                #elif self.id != [idx for idx, val in enumerate(self.inlift) if val == min(self.inlift) ][0]:
                 #   print "I aint getting in dat!"
                  #  break
        else:
            print "No one is on the ground floor to pickup"
       
        gfloor = [x for x in gfloor if x not in self.inlift ]

        #del gfloor[0:len(self.inlift)]

        print "Folks remaining on ground floor", len(gfloor)
        print "There are {} Folks in lift {} ".format(len(self.inlift), self.id)

        if self.occup == self.maxcap:
            print "I'm lift {} and I am full - start to deliver people".format(self.id)
            self.inlift.sort(key = operator.attrgetter("requestfloor"))
            self.currentfloor = 0
            self.active = 1
            self.liftseccount = 0

        if len(gfloor) == 0 and len(self.inlift) != 0:
            
            elaptime = self.liftopentime - self.liftseccount
            
            print "I am lift {} and I've got everyone from groundfloor - waiting {} secs for others".format(self.id, elaptime)
            self.inlift.sort(key = operator.attrgetter("requestfloor"))
            self.currentfloor = 0
            self.active = 0
            self.liftseccount += 1

        if len(gfloor) == 0 and liftseccount == self.liftopentime:
            print "I am door {}, Doors shut after {} seconds - I've got everyone from groundfloor - start to deliver people".format(self.id, liftseccount)
            self.inlift.sort(key = operator.attrgetter("requestfloor"))
            self.currentfloor = 0
            self.active = 1
            self.liftseccount = 0
        
        if self.occup != 0 and liftseccount == self.liftopentime:
            print "Doors closed nah nah"
            self.inlift.sort(key = operator.attrgetter("requestfloor"))
            self.currentfloor = 0
            self.active = 1
            self.liftseccount = 0

        elaptime = self.liftopentime - self.liftseccount
        if self.active != 1 and len(gfloor) != 0 :
            print "I am lift {} and I've got people waiting patiently for doors to shut in {} seconds".format(self.id, elaptime)
           
        return self.inlift

    def move(self):
        global startcount
        global mapfloor
        global inlift

        if self.currentfloor == 0:
            
            self.flr = [self.inlift[i].requestfloor for i in range(len(self.inlift)) ]
            
            self.unqfloors = list(set(self.flr))
            self.unqfloors.insert(0,0)
            startcount = count
            print "||Lift {} is beginning takeoff||".format(self.id)
            self.mapfloor = self.tripmap(self.unqfloors, count)
            
           
        print "ACTIVE -> at time =", count
        print "{} Folks in lift {} at time {} -> {}".format(len(self.flr), self.id, count, self.flr)
        print "# of people", len(self.flr)
     
        self.transition = 1
        self.trips += 1

        try:
            topflr = max(self.flr)
        except ValueError:
            topflr = 0

        timedown = topflr * self.floortime
        self.timedown.append(topflr * self.floortime)

        self.active = 1

        finishcount = len(self.mapfloor)-1

        try:
            indexesmap = [val[0] for val in self.mapfloor]
            idmap = indexesmap.index(count)
            print "Lift {} event-> {} ".format(self.id, self.mapfloor[idmap][1])

            if self.mapfloor[idmap][1] == "GTFO":
                self.flr = [x for x in self.flr if x != min(self.flr)]

        except ValueError:
            print "ACTIVATE G FLOOR METHOD"
            self.gfloor()
            self.inlift = []
            self.flr = []
            self.active = 0
            self.occup = 0
            print "I come back here at floor {}".format(self.currentfloor)
            
        return self.flr

    def tripmap(self, floors, count):
        print "Called Trip Map"
        timeofevent = []
        event = []
        print floors
        tript=count
        print "TRIPT", tript
        
        for i in xrange(1,len(floors)): #xrange instead of range - xrange is generator object unlike range, it doesn't create a list.
                                    #Why does xrange appear to slow this code down?
            
            if i != 1:
                tript = tript+1

            eventdes = "lift in transition to floor {} trip time is {} seconds".format(k[i], tript)
            timeofevent.append(tript)
            event.append(eventdes)
            
            tofloor = floors[i]
            tript = tript + (floors[i]-floors[i-1])*5
            eventdes2 = "Arrived at floor {}, people getting out trip time is {} seconds".format(floors[i], tript)
            timeofevent.append(tript)
            event.append(eventdes2)
            self.currentfloor = floors[i]
            
            tript = tript + 5
            eventdes3 = "GTFO"
            timeofevent.append(tript)
            event.append(eventdes3)

        info= list(zip(timeofevent,event))    
        info = [list(tup) for tup in info]

        p = range(min(timeofevent),max(timeofevent)+1)
        d = np.repeat("noevent",len(p))

        master = list(zip(p,d))
        master = [list(tup) for tup in master]

        indexesi = [val[0] for val in master]

        for idx,event in info:
            id = indexesi.index(idx)
            master[id-1][1] = event 

        toptime = len(master) + count #time when you arrive at the top floor
        print "toptime", toptime
        bottomtime = toptime + (max(floors) * 5) #If it takes 15 secvonds to reach the bottom floor from the top floor

        times = range(toptime,bottomtime-1)
        eventattime = np.repeat("goingdown",len(times))

        downtime = zip(times, eventattime)
        downtime = [list(tup) for tup in downtime]
        master.extend(downtime)
       
        return master
             
    def gfloor(self):
        self.currentfloor = 0
        self.active = 0
        print "I am on floor {}".format(self.currentfloor)

class Agent:
    newid = itertools.count().next
    def __init__(self,requestfloor,arrivaltime):
        self.id = Agent.newid()
        self.arrivaltime = arrivaltime
        self.requestfloor = requestfloor
        self.company =  ["A" if x == 1 else "B" for x in [np.random.random_integers(0,1)]][0]
        self.group = []
        self.officeid = str(self.requestfloor) + self.company

        #So a solution to this is to essentially put each agent in their own group if when on the ground floor and
        #same floor requests come in and same company -> group those guys together.
        
        #If requestfloor and company are the same individual agents should group and be one object but obviously count individually towards
        #lift capacity

class Floor: 
    def __init__(self,id, occup, pressed):
        self.id = id
        self.occup = occup
        self.pressed = 0

arrivaldist = np.random.poisson(7,1000)

global liftseccount
gfloor = []
numberoffloors = 5
agentlist = [ Agent(int(np.random.random_integers(1, numberoffloors, 1)), i ) for i in arrivaldist]

print "Number of agents in system ->", len(agentlist)
agentlist.sort(key = operator.attrgetter("arrivaltime"))

liftlist = [Lift() for i in range(2)]
liftseccount = 0

#def groupGF(gfloorlist):


def groupG(gfloor):
    flrs = range(1,6)
    offices = ["A","B"] #all floors and offices
    officeids = [str(i)+j for i in flrs for j in offices] 
    rr = dict.fromkeys(officeids)
    rr = {x:[] for x in rr}

    for agent in gfloor:
        for key, val in rr.items():
            if key == agent.officeid:
                rr[key].append(agent)                
    return rr.values()
    
count = 0
while(count < 200):
    for agent in agentlist:
        if agent.arrivaltime == count:
            gfloor.append(agent)
            agentlist.pop(0)

    print 
    if len(gfloor) != 0:
        gfloor = groupG(gfloor)
    
    print "Ground Floor",gfloor
            
    print "number of people on g floor", sum(len(x) for x in gfloor)

    if sum(len(x) for x in gfloor) != 0:
        map(lambda y: y.enterme(), [lift for lift in liftlist if lift.active == 0 and lift.currentfloor == 0 ] )
        print "Entry Function Finished"
        map(lambda y: y.move(), [lift for lift in liftlist if lift.active == 1 and lift.currentfloor == 0] )
        print "Ground Floor Move Function Complete"
        map(lambda y: y.move(), [lift for lift in liftlist if lift.active == 1 and lift.currentfloor != 0] )
        print "During Floor Move Function Complete"
    
    print "Elapsed Time = {} Seconds".format(count)
    
    count += 1
