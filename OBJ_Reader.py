class ObjReader:
    def __init__(self, file):
        self.file = file
        self.vertexList = list()
        self.textureList = list()
        self.normalList = list()
        self.vertices = list()
        self.uvs = list()
        self.normals = list()

        objFile = open(file, 'r')

        for line in objFile:
            split = line.split()
            #if blank line, skip
            if not len(split):
                continue
            if split[0] == "v":
                self.vertexList.append([float(i) for i in split[1:]])
            elif split[0] == "vt":
                self.textureList.append([float(i) for i in split[1:]])
            elif split[0] == "vn":
                self.normalList.append([float(i) for i in split[1:]])
            elif split[0] == "f":
                for s in split[1:]:
                    s = s.split('/')
                    self.vertices.append(self.vertexList[int(s[0])-1])
                    self.uvs.append(self.textureList[int(s[1])-1])
                    self.normals.append(self.normalList[int(s[2])-1])
        objFile.close()

        self.trios = list()
        for i in range(0, len(self.vertices), 3):
            self.trios.append([self.vertices[i], self.vertices[i + 1], self.vertices[i + 2]])

