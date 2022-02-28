import requests as rq
import random as rd

def flipCoin():
    return rd.randint(0,1) == 1


class privot:
    def __init__(self, Acore, t=None, r=None, b=None, l=None):
        self.Acoor = Acore
        self.t = t
        self.r = r
        self.b = b
        self.l = l
    def Lcoor(self):
        x = 0
        y = 0
        node = self
        while node.l is not None:
            node = node.l
            x+=1
        node = self
        while node.t is not None:
            node = node.t
            y+=1
        return y,x
    def vLink(self, other):
        self.b = other
        other.t = self
    def hLink(self, other):
        self.r = other
        other.l = self
    def blockDim(self):
        x, y = 1, 1
        n = self
        while n.r is not None:
            n = n.r
            x+=1
        while n.b is not None:
            n = n.b
            y+=1
        return y,x
    def blockSize(self):
        x, y = self.blockDim()
        return x*y

class graph:
    def __init__(self, size: tuple):
        self.size = size
        self.root = self.chain(size[0], (0,0))
        self.fragments = [self.root]
        p = self.root
        for i in range(1, size[1]):
            np = self.chain(size[0], (0,i))
            self.zip(p, np)
            p = np

    def chain(self, length, coor):
        head = privot(coor)
        p = head
        for i in range(1, length):
            np = privot((coor[0]+i, coor[1]))
            p.vLink(np)
            p = np
        return head
    def zip(self, c1: privot, c2: privot):
        n1, n2 = c1, c2
        while n1 is not None and n2 is not None:
            n1.hLink(n2)
            n1, n2 = n1.b, n2.b
    def index(self,y,x, n = None):
        print(f"Indexing {y},{x}")
        n = self.root if n is None else n
        for _ in range(x):
            if n.r is None:
                break
            n = n.r
        for _ in range(y):
            if n.b is None:
                break
            n = n.b
        return n
    def vSnip(self, lx, fragment: privot = None):
        fragment = self.root if fragment is None else fragment
        newHead = self.index(0,lx,n=fragment)
        n = newHead
        print(n.blockDim())
        # print(f"> {fragment.Lcoor()} {newHead.Lcoor()} {[newHead, n.l.r, n.b]}")
        if n.l is None or None in [newHead, n.l.r]:
            print("vSnip Invalid")
            return
        while n is not None:
            n.l.r = None
            n.l = None
            n = n.b
        print(f"added {newHead.blockDim() if newHead is not None else 'None'}")
        self.fragments.append(newHead)
        print([e.blockDim() for e in self.fragments])
        print([e.Acoor for e in self.fragments])
        print([(e.blockSize(), 0) for e in self.fragments])
    def hSnip(self, ly, fragment: privot = None):
        fragment = self.root if fragment is None else fragment
        newHead = self.index(ly,0,n=fragment)
        n = newHead
        print(n.blockDim())
        # print(f"> {fragment.Lcoor()} {newHead.Lcoor()} {[newHead, n.t.b, n.r]}")
        if n.t is None or None in [newHead, n.t.b]:
            print("hSnip Invalid")
            return
        while n is not None:
            n.t.b = None
            n.t = None
            n = n.r
        print(f"added {newHead.blockDim() if newHead is not None else 'None'}")
        self.fragments.append(newHead)
        print([e.blockDim() for e in self.fragments])
        print([e.Acoor for e in self.fragments])
        print([(e.blockSize(), 0) for e in self.fragments])
    def graphSize(self):
        return self.size[0]*self.size[1]

def genClues(graph):
    res = []
    for clue in graph.fragments:
        res.append({
            "position":{
                "x":clue.Acoor[1],
                "y":clue.Acoor[0]
            },
            "size":clue.blockSize()
        })
    return res

def random(graph: graph, n=None, max=None):
    max = max if max is not None else graph.graphSize()*10
    n = n if n is not None else int(graph.graphSize()*0.4)
    i = 0
    while len(graph.fragments) < n and i <= max:
        i += 1
        # print(graph.fragments)
        a = [n for n in graph.fragments if n.blockSize() > 1]
        # print([e.blockDim() for e in graph.fragments], sum([e.blockSize() for e in graph.fragments]))
        # print([e.Acoor for e in graph.fragments])
        # print([(e.blockSize(), 0) for e in graph.fragments])
        if len(a) > 0:
            choice = rd.choices(a)[0]
        else:
            break
        if 1 in choice.blockDim():
            print(f"choice : {choice.blockDim()}")
            if choice.blockDim()[0] > 2:
                print("a")
                r = rd.randint(1, choice.blockDim()[0]-1)
                print(r)
                # print(f"a {r} {choice.blockDim()}")
                graph.hSnip(r, choice)
            elif choice.blockDim()[1] > 2:
                print("b")
                r = rd.randint(1, choice.blockDim()[1]-1)
                print(r)
                # print(f"b {r} {choice.blockDim()}")
                graph.vSnip(r, choice)
        else:
            if flipCoin():
                r = rd.randint(1, choice.blockDim()[0]-1)
                # print(f"a {r} {choice.blockDim()}")
                graph.hSnip(r, choice)
            else:
                r = rd.randint(1, choice.blockDim()[1]-1)
                # print(f"b {r} {choice.blockDim()}")
                graph.vSnip(r, choice)


if __name__ == "__main__":
    g = graph((10,10))
    random(g)
    pk = {
            "numberOfRows": g.size[0],
            "numberOfCols": g.size[1],
            "clues": genClues(g)
        }
    print(f"Block num: {len(g.fragments)}")
    print("+++++++++++++++++++++++++++++++++++++++++++")
    print(pk)
    print(len(rq.post("http://localhost:9000/depth-first-search", json=pk).json()))