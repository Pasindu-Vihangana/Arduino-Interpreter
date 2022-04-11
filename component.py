###################################################
#        # edit case after adding device #        #
###################################################
def deviceBuild(logicType, nodes):
    match logicType.split('_')[0]:
        case 'not':
            # print("NOT")
            return NOT(logicType, nodes)
        case 'and':
            # print("AND")
            return AND(logicType, nodes)
        case 'or':
            # print("OR")
            return OR(logicType, nodes)
        case 'nand':
            # print("NOT")
            return NAND(logicType, nodes)
        case 'nor':
            # print("AND")
            return NOR(logicType, nodes)
        case 'xor':
            # print("OR")
            return XNOR(logicType, nodes)
        case 'xnor':
            # print("OR")
            return XNOR(logicType, nodes)
###################################################
###################################################


class D_PIN:
    name = ''
    digitalAddress = 0

    def __init__(self, name):
        self.name = name
        self.value = False
        self.node = {'pin': self.value}
        self.type = 'pin'

    def process(self):
        self.node['pin'] = self.value

    def out(self):
        return self.value


class NOT:
    def __init__(self, unit, pins):
        self.name = unit
        self.value = False
        self.node = {'out': self.value}
        for pin in range(len(pins)):
            self.node[pins[pin]] = False

    def process(self):
        self.value = not(self.node['in'])
        self.node['out'] = self.value

    def out(self):
        return self.value


class AND:
    def __init__(self, unit, pins):
        self.name = unit
        self.value = False
        self.node = {'out': self.value}
        for pin in range(len(pins)):
            self.node[pins[pin]] = False

    def process(self):
        inputs = [val for key, val in self.node.items() if 'in' in key]
        input_keys = [key for key, val in self.node.items() if 'in' in key]
        self.value = inputs[0]
        for index in range(1, len(inputs)):
            self.value = self.value and inputs[index]
        self.node['out'] = self.value

    def out(self):
        return self.value


class OR:
    def __init__(self, unit, pins):
        self.name = unit
        self.value = False
        self.node = {'out': self.value}
        for pin in range(len(pins)):
            self.node[pins[pin]] = False

    def process(self):
        inputs = [val for key, val in self.node.items() if 'in' in key]
        input_keys = [key for key, val in self.node.items() if 'in' in key]
        self.value = inputs[0]
        for index in range(1, len(inputs)):
            self.value = self.value or inputs[index]
        self.node['out'] = self.value

    def out(self):
        return self.value


class NAND:
    def __init__(self, unit, pins):
        self.name = unit
        self.value = False
        self.node = {'out': self.value}
        for pin in range(len(pins)):
            self.node[pins[pin]] = False

    def process(self):
        inputs = [val for key, val in self.node.items() if 'in' in key]
        input_keys = [key for key, val in self.node.items() if 'in' in key]
        self.value = inputs[0]
        for index in range(1, len(inputs)):
            self.value = self.value and inputs[index]
        self.value = not self.value
        self.node['out'] = self.value

    def out(self):
        return self.value


class NOR:
    def __init__(self, unit, pins):
        self.name = unit
        self.value = False
        self.node = {'out': self.value}
        for pin in range(len(pins)):
            self.node[pins[pin]] = False

    def process(self):
        inputs = [val for key, val in self.node.items() if 'in' in key]
        input_keys = [key for key, val in self.node.items() if 'in' in key]
        self.value = inputs[0]
        for index in range(1, len(inputs)):
            self.value = self.value or inputs[index]
        self.value = not self.value
        self.node['out'] = self.value

    def out(self):
        return self.value


class XOR:
    def __init__(self, unit, pins):
        self.name = unit
        self.value = False
        self.node = {'out': self.value}
        for pin in range(len(pins)):
            self.node[pins[pin]] = False

    def process(self):
        inputs = [val for key, val in self.node.items() if 'in' in key]
        input_keys = [key for key, val in self.node.items() if 'in' in key]
        self.value = inputs[0]
        for index in range(1, len(inputs)):
            self.value ^= inputs[index]
        self.node['out'] = self.value

    def out(self):
        return self.value


class XNOR:
    def __init__(self, unit, pins):
        self.name = unit
        self.value = False
        self.node = {'out': self.value}
        for pin in range(len(pins)):
            self.node[pins[pin]] = False

    def process(self):
        inputs = [val for key, val in self.node.items() if 'in' in key]
        input_keys = [key for key, val in self.node.items() if 'in' in key]
        self.value = inputs[0]
        for index in range(1, len(inputs)):
            self.value ^= inputs[index]
        self.value = not self.value
        self.node['out'] = self.value

    def out(self):
        return self.value
