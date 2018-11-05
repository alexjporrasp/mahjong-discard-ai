class Meld:
    @classmethod
    def decode(Meld, data):
        data = int(data)
        meld = Meld()
        meld.fromPlayer = data & 0x3
        if data & 0x4:
            meld.decodeChi(data)
        elif data & 0x18:
            meld.decodePon(data)
        else:
            meld.decodeKan(data)
        return meld

    def decodeChi(self, data):
        self.type = "chi"
        t0, t1, t2 = (data >> 3) & 0x3, (data >> 5) & 0x3, (data >> 7) & 0x3
        baseAndCalled = data >> 10
        self.called = baseAndCalled % 3
        base = baseAndCalled // 3
        base = (base // 7) * 9 + base % 7
        self.tiles =  (t0 + 4 * (base + 0)),  (t1 + 4 * (base + 1)),  (t2 + 4 * (base + 2))
    
    def decodePon(self, data):
        t4 = (data >> 5) & 0x3
        t0, t1, t2 = ((1,2,3),(0,2,3),(0,1,3),(0,1,2))[t4]
        baseAndCalled = data >> 9
        self.called = baseAndCalled % 3
        base = baseAndCalled // 3
        if data & 0x8:
            self.type = "pon"
            self.tiles =  (t0 + 4 * base),  (t1 + 4 * base),  (t2 + 4 * base)
        else:
            self.type = "chakan"
            self.tiles =  (t0 + 4 * base),  (t1 + 4 * base),  (t2 + 4 * base),  (t4 + 4 * base)
    
    def decodeKan(self, data):
        baseAndCalled = data >> 8
        if self.fromPlayer:
            self.called = baseAndCalled % 4
        else:
            del self.fromPlayer
        base = baseAndCalled // 4
        self.type = "kan"
        self.tiles =  (4 * base),  (1 + 4 * base),  (2 + 4 * base),  (3 + 4 * base)