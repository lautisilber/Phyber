import matplotlib.pyplot as plt
from matplotlib.widgets import Button
from Phyber_RelK_Engine import RelK
from Phyber_RelK_Entities import Event, Object, C

class Graph:
    def __init__(self, data):
        self.data = data

    def PlotObjectsVsMainSystem(self):
        coords1 = self.data[0][0][1]
        coords2 = self.data[0][0][2]
        object1 = self.data[0]

        ax1 = plt.subplot(121, projection='3d')
        ax2 = plt.subplot(122, projection='3d')

        for events in object1:
            ax1.scatter(events[1][1], events[1][2], events[1][0], marker='o')
            ax2.scatter(events[2][1], events[2][2], events[2][0], marker='o')

        ax1.set_xlabel('X Label')
        ax1.set_ylabel('Y Label')
        ax1.set_zlabel('Z Label')

        ax2.set_xlabel('X Label')
        ax2.set_ylabel('Y Label')
        ax2.set_zlabel('Z Label')

        plt.show()


def main():
    e1 = Event(0, 0, 'bottom left')
    e2 = Event(1, 0, 'bottom right')
    e3 = Event(1, 1, 'top right')
    e4 = Event(0, 1, 'top left')

    o1 = Object([e1, e2, e3, e4], (3**(1/2) * C / 2), 0, 'obj 1')

    engine = RelK([o1])
    engine.CalculateIteration_time(0, .000000001, .0000000005)
    engine.LogData()
    data = engine.GetData()

    gr = Graph(data)
    gr.PlotObjectsVsMainSystem()

if __name__ == '__main__':
    main()