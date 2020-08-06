import math

C = 299792458
C2 = C**2

class Event:
    def __init__(self, x, y, name=''):
        self.name = name
        self.delta_t = 0
        self.x = x
        self.y = y

class Object:
    def __init__(self, events, vel_x, vel_y, name=''):
        assert isinstance(events, list)
        self.events = events
        self.vel = (vel_x, vel_y)
        self.velMag = math.sqrt(self.vel[0]**2 + self.vel[1]**2)
        self.name = name
        for i in range(len(self.events)):
            self.events[i].name = self.name + ': ' + self.events[i].name

class Math:
    @staticmethod
    def Gamma(v):
        if v == C:
            return math.inf # lim when v -> C = infinity
        else:
            return 1/math.sqrt(1-(v**2)/(C2))

    @staticmethod
    def Beta(v):
        return v/C
    
    @staticmethod
    def LorentzTPrime(t, x, v):
        return Math.Gamma(v) * (t - (v * x) / C2)

    @staticmethod
    def LorentzT(tp, x, v):
        return tp / Math.Gamma(v) + (v * x) / C2

    @staticmethod
    def LorentzXPrime(t, x, v):
        return Math.Gamma(v) * (x - v * t)

    @staticmethod
    def LorentzX(t, xp, v):
        return xp / Math.Gamma(v) + v * t
    
    @staticmethod
    def LorentzCT(t, x, v):
        return Math.Gamma(v) * (C * t - Math.Beta(v) * x)

    @staticmethod
    def LorentzVPrime(v, V):
        return (v - V) / (1 - (v * V) / C2)

    @staticmethod
    def LorentzDeltaTPrime(delta_t, v):
        return delta_t / Math.Gamma(v)

class Log:
    def __init__(self, systemCount, charCount):
        self.systemCount = systemCount
        self.charCount = charCount

    def LogBegin(self):
        print(Table.Header(Log.LogMakeHeader(self.systemCount), self.charCount))

    def LogRow(self, data):
        # [
        #   [t, x, y] --> in system S
        #   [t, x, y] --> in system S'
        #   ...
        # ]
        logData = list()
        for s in data:
            logData.append('')
            for c in s:
                logData.append(c)
            logData.append('')
        print(Table.Row(logData[:len(logData) - 1], self.charCount))

    def LogRows(self, data):
        # [
        #   [
        #       [t, x, y] --> in system S   --> Event 1
        #       [t, x, y] --> in system S'
        #       ...
        #   ]
        #   [
        #       [t, x, y] --> in system S   --> Event 2
        #       [t, x, y] --> in system S'
        #       ...
        #   ]
        #   ...
        # ]
        for e in data:
            self.LogRow(e)

    def EndTable(self):
        print(Table.EndTable(self.systemCount, self.charCount))

    @staticmethod
    def LogMakeHeader(sysCount):
        header = list()
        s = 'S'
        header.append('Event name')
        header.append('')
        for _ in range(sysCount):
            header.append(' ' + s + ' ')
            header.append(' t ')
            header.append(' x ')
            header.append(' y ')
            header.append('')
            s += "'"
        return header[:len(header) - 1]

    @staticmethod
    def LogMakeRow(data, charLength):
        # [
        #   [t, x, y] --> in system S
        #   [t, x, y] --> in system S'
        #   ...
        # ]
        loggableData = list()
        for s in data:
            loggableData.append('')
            for c in s:
                string = str(c)
                if len(string) > charLength:
                    string = string[:charLength]
                loggableData.append(string)
        return loggableData
        
    @staticmethod
    def LogEvent(t, x, y=None):
        decimals = 12
        headers = [' t ', ' x ']
        data = [str(round(t, decimals)), str(round(x, decimals))]
        if y != None:
            headers.append(' y ')
            data.append(str(round(y, decimals)))
        print(Table.Table(headers, [data]))

    @staticmethod
    def LogEventsInSystems(data):
        # [[[t, x, y] in system S, [t, x, y] in system S', ...] Event 1
        #  [[t, x, y] in system S, [t, x, y] in system S', ...] Event 2
        #  ...]
        decimals = 12
        sysCount = 0
        for e in data:
            if len(e) - 1 > sysCount:
                sysCount = len(e) - 1
        rows = list()
        for e in data:
            r = [e[0]]
            e = e[1:]
            r.append('')
            r.append('')
            for s in e:
                for c in s:
                    r.append(str(round(c, decimals)))
                r.append('')
                r.append('')
            r = r[:len(r) - 2]
            rows.append(r)
        print(Table.Table(Log.LogMakeHeader(sysCount), rows))

class Table:
    @staticmethod
    def Table(headers, rows):
        maxCharLengths = list()
        maxListLength = len(headers)
        for c in rows:
            if len(c) > maxListLength:
                maxListLength = len(c)

        for i in range(maxListLength):
            currLength = 0
            if len(headers) > i:
                currLength = len(headers[i])
            for c in rows:
                if len(c) > i:
                    if len(c[i]) > currLength:
                        currLength = len(c[i])
            maxCharLengths.append(currLength)            

        def MakeHeaderLine(mcl):
            t = '+'
            for l in mcl:                
                for _ in range(l):
                    t += '-'
                t += '+'
            return t + '\n'
                
        def MakeRow(mcl, cols):
            t = '|'
            for i in range(len(cols)):
                t += cols[i]
                diff = mcl[i] - len(cols[i])    
                for _ in range(diff):
                    t += ' '
                t += '|'
            return t + '\n'

        s = MakeHeaderLine(maxCharLengths)
        s += MakeRow(maxCharLengths, headers)
        s += MakeHeaderLine(maxCharLengths)
        for c in rows:
            s += MakeRow(maxCharLengths, c)
        s += MakeHeaderLine(maxCharLengths)

        return(s)

    @staticmethod
    def MakeHeaderLine(titleCount, charCount):
        s = '+'
        for _ in range(titleCount):
            for _ in range(charCount):
                s += '-'
            s += '+'
        return s

    @staticmethod
    def Header(header, spacing):
        s = Table.MakeHeaderLine(len(header), spacing)
        s += '\n|'
        for h in header:
            s += h
            for _ in range(spacing - len(h)):
                s += ' '
            s += '|'
        s += '\n'
        s += Table.MakeHeaderLine(len(header), spacing)

        return s

    @staticmethod
    def Row(data, spacing):
        s = '|'
        for d in data:
            ds = str(d)
            if len(ds) < spacing:
                s += ds
                for _ in range(spacing - len(ds)):
                    s += ' '
            elif len(ds) > spacing:
                t = ds[:spacing]
                s += t
            else:
                s += ds
            s += '|'
        return s
            

    @staticmethod
    def EndTable(sysCount, spacing):
        return Table.MakeHeaderLine(sysCount * 5 - 1, spacing)