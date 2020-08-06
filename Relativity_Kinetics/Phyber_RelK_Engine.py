from Phyber_RelK_Entities import Event, Object, Math, C, Log

class RelK:
    def __init__(self, objects, autoCalcTDeltas=True):
        assert isinstance(objects, list)
        self.objects = objects
        if autoCalcTDeltas:
            self.Calculate_Delta_time()
        self.logData = list()

    def Calculate_Delta_time(self):
        for i in range(len(self.objects)):
            for n in range(len(self.objects[i].events)):
                #set delta t primes for a delta t on 1s
                self.objects[i].events[n].delta_t = Math.LorentzDeltaTPrime(1, self.objects[i].velMag)

    @staticmethod
    def Snapshot_time(obj, s_time):
        assert isinstance(obj, Object)
        data = list()
        for e in obj.events:
            tp = e.delta_t * s_time
            xp = e.x
            yp = e.y
            x = Math.LorentzX(s_time, xp, obj.vel[0])
            y = Math.LorentzX(s_time, yp, obj.vel[1])
            data.append([e.name, (s_time, x, y), (tp, xp, yp)])
        # data is [ [ event name, (coords ov event 1 in S), (coord of event 1 in S') ],
        #           [ event name, (coords ov event 2 in S), (coord of event 2 in S') ]
        #           ...]        
        return data

    def CalculateIteration_time(self, t_start, t_end, t_step):
        for o in self.objects:
            data = list()
            orderedData = list()
            t = t_start
            while t < t_end:
                data.append(self.Snapshot_time(o, t))
                t += t_step
            for d in data:
                for element in d:
                    orderedData.append(element)
            self.logData.append(orderedData)
        return orderedData

    def LogData(self):
        for obj in self.logData:
            Log.LogEventsInSystems(obj)

def main():
    import math
    e1 = Event(0, 0, 'back1')
    e2 = Event(1, 0, 'front1')
    e3 = Event(0, 0, 'back2')
    e4 = Event(2, 2, 'front2')
    e5 = Event(0, 0, 'back3')
    e6 = Event(1, 1, 'front3')
    o1 = Object([e1, e2], math.sqrt((3/4) * (C**2)), 0, 'Object 1')
    o2 = Object([e3, e4], C / 10, C / 10, 'Object 2')
    o3 = Object([e5, e6], C, 0, 'Object 3')
    r = RelK([o1, o2, o3])
    #allData = r.Snapshot_time(1)
    r.CalculateIteration_time(0, 1, 0.1)
    r.LogData()

if __name__ == '__main__':
    main()