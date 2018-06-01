import sys,os
import itertools
import operator
from scipy.stats import truncnorm
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.pyplot as plt
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
        print "LIFT ENTRY FUNCTION been called"
        global agentlist
        
        for per in gfloor: #unfortunately this can only put this lot of gfloor in one lift
            
            #self.id == [idx for idx, val in enumerate(self.inlift) if val == min(self.inlift) ][0]

            #you can actually start each lift instance with a fake person

            if self.occup < self.maxcap and len(self.inlift) == 0: #Every lift should hit this once!
                print "Person {} entered lift {} which is empty right --> {} should be zero".format(per, self.id, len(self.inlift))
                self.inlift.append(per)
                #print "A person entered lift {}".format(self.id)
                break
                
            
            elif self.occup < self.maxcap and self.id != [idx for idx, val in enumerate(self.inlift) if val == min(self.inlift) ][0] and len(self.inlift) != 0: #and len(gfloor) != 0:
                #This says that the lift is not at capacity and this lift is not the lift with the fewest people in it
                #self.inlift.append(per)
                #print "A person entered lift {}".format(self.id)
                print "I'm not getting in the lift with that stinky bugger, choosing lift with least people"
                break

            elif self.occup < self.maxcap and self.id == [idx for idx, val in enumerate(self.inlift) if val == min(self.inlift) ][0] and len(self.inlift) != 0: #and len(gfloor) != 0:
                self.inlift.append(per)
                
                print "Person {} entered lift {} which has --> {} in it".format(per, self.id, len(self.inlift))
                break


                #IF I CAN'T GO IN WITH MY COLLEAGUES WE WILL WAIT
                #IF LIFT IS OVER 70% FULL I AINT GOING IN DAT SHEET

                print "lift capacity of lift {} is {}".format(self.id,len(self.inlift))

                #append everyone if count is == to arrivaltime
                self.occup +=1
            elif self.occup == self.maxcap:
                print "Lift {} is at capacity!".format(self.id)
                break

            #elif self.id != [idx for idx, val in enumerate(self.inlift) if val == min(self.inlift) ][0]:
             #   print "I aint getting in dat!"
              #  break
       
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

    def tripmap(self, k, count):
        print "Called Trip Map"
        timeofevent = []
        event = []
        print k
        tript=count
        print "TRIPT", tript
        
        for i in range(1,len(k)):
            if i != 1:
                tript = tript+1

            eventdes = "lift in transition to floor {} trip time is {} seconds".format(k[i], tript)
            timeofevent.append(tript)
            event.append(eventdes)
            
            tofloor = k[i]
            tript = tript + (k[i]-k[i-1])*5
            eventdes2 = "Arrived at floor {}, people getting out trip time is {} seconds".format(k[i], tript)
            timeofevent.append(tript)
            event.append(eventdes2)
            self.currentfloor = k[i]
            
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
        bottomtime = toptime + (max(k) * 5) #If it takes 15 secvonds to reach the bottom floor from the top floor

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

class Floor: 
    def __init__(self,id, occup, pressed):
        self.id = id
        self.occup = occup
        self.pressed = 0

arrivaldist = np.random.poisson(7,1000)
n, bins, patches = plt.hist(arrivaldist, 50, normed=1, facecolor='green', alpha=0.75)
global liftseccount
gfloor = []
agentlist = [ Agent(int(np.random.random_integers(1, 5, 1)), i ) for i in arrivaldist]

print "Number of agents in system ->", len(agentlist)
agentlist.sort(key = operator.attrgetter("arrivaltime"))

liftlist = [Lift() for i in range(2)]
liftseccount = 0

count = 0
while(count < 200):
    for agent in agentlist:
        if agent.arrivaltime == count:
            gfloor.append(agent)
            agentlist.pop(0)
            
    print "number of people on g floor", len(gfloor)
    
    map(lambda y: y.enterme(), [x for x in liftlist if x.active == 0 and x.currentfloor == 0 ] )
    map(lambda y: y.move(), [x for x in liftlist if x.active == 1 and x.currentfloor == 0] )
    map(lambda y: y.move(), [x for x in liftlist if x.active == 1 and x.currentfloor != 0] )

    print "Elapsed Time = {} Seconds".format(count)
    
    count += 1

#every lift should be instantiated with an occupent that has a floor request of 99 or something that will never be satisfied.
#this just makes it easier than dealing with empty sets

    

#Logic for which lift someone will choose when many available i.e. at start of day
    #if they come with someone on the same floor and business - those two ride the same elevator
    #most people will choose the closest lift open
    #if lift over 50% full most folks will wait for another lift
    #
