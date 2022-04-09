class D_PIN:
    name = ''
    digitalAddress = 0
    node = 0

    def __init__(self, name):
        self.name = name


class NOT:
    out = 0
    name = ''
    node = {'out': 0}

    def __init__(self, unit, pins):
        self.name = unit
        for pin in range(len(pins)):
            self.node[pins[pin]] = 0

    def process(self):
        pass


class AND:
    out = 0
    name = ''
    node = {'out': 0}

    def __init__(self, unit, pins):
        self.name = unit
        for pin in range(len(pins)):
            self.node[pins[pin]] = 0

    def process(self):
        pass


class OR:
    out = 0
    name = ''
    node = {'out': 0}

    def __init__(self, unit, pins):
        self.name = unit
        for pin in range(len(pins)):
            self.node[pins[pin]] = 0

    def process(self):
        pass
