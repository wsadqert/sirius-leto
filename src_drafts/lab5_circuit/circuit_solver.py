import numpy as np

class Resistor:
    def __init__(self, resistance, node1, node2):
        self.resistance = resistance
        self.node1 = node1
        self.node2 = node2

class VoltageSource:
    def __init__(self, voltage, node1, node2):
        self.voltage = voltage
        self.node1 = node1
        self.node2 = node2

class Circuit:
    def __init__(self):
        self.resistors = []
        self.voltage_sources = []
        self.nodes = set()

    def add_resistor(self, resistance, node1, node2):
        self.resistors.append(Resistor(resistance, node1, node2))
        self.nodes.update([node1, node2])

    def add_voltage_source(self, voltage, node1, node2):
        self.voltage_sources.append(VoltageSource(voltage, node1, node2))
        self.nodes.update([node1, node2])

    def solve(self):
        node_list = list(self.nodes)
        node_index = {node: i for i, node in enumerate(node_list)}
        num_nodes = len(node_list)

        # Create the matrix A and vector B
        A = np.zeros((num_nodes, num_nodes))
        B = np.zeros(num_nodes)

        # Treat 'ground' as the reference node
        if 'ground' not in node_index:
            raise ValueError("Ground node must be defined as 'ground'.")

        # Build equations based on KCL for each node (except ground)
        for node in node_list:
            if node == 'ground':
                continue

            node_eq_index = node_index[node]
            for resistor in self.resistors:
                if resistor.node1 == node:
                    other_node_index = node_index[resistor.node2]
                    A[node_eq_index, node_eq_index] += 1 / resistor.resistance
                    A[node_eq_index, other_node_index] -= 1 / resistor.resistance
                elif resistor.node2 == node:
                    other_node_index = node_index[resistor.node1]
                    A[node_eq_index, node_eq_index] += 1 / resistor.resistance
                    A[node_eq_index, other_node_index] -= 1 / resistor.resistance

            for source in self.voltage_sources:
                if source.node1 == node:
                    other_node_index = node_index[source.node2]
                    A[node_eq_index, node_eq_index] += 1  # KVL for voltage source
                    A[node_eq_index, other_node_index] -= 1  # KVL for voltage source
                    B[node_eq_index] -= source.voltage
                elif source.node2 == node:
                    other_node_index = node_index[source.node1]
                    A[node_eq_index, node_eq_index] += 1  # KVL for voltage source
                    A[node_eq_index, other_node_index] -= 1  # KVL for voltage source
                    B[node_eq_index] += source.voltage

        # Set ground node voltage to 0
        ground_index = node_index['ground']
        A[ground_index, :] = 0
        A[ground_index, ground_index] = 1
        B[ground_index] = 0

        # Enforce the voltage of the voltage sources
        for source in self.voltage_sources:
            if source.node1 == 'ground':
                node_eq_index = node_index[source.node2]
                A[node_eq_index, :] = 0  # Clear the equation for this node
                A[node_eq_index, node_eq_index] = 1  # Set the voltage at this node
                B[node_eq_index] = source.voltage  # Set the voltage to the source voltage

        # Solve the linear equations
        voltages = np.linalg.solve(A, B)
        return {node: voltages[i] for i, node in enumerate(node_list)}

# Example usage
circuit = Circuit()
circuit.add_voltage_source(10, 'ground', 'node1')
circuit.add_resistor(10, 'node1', 'node2')
circuit.add_resistor(3, 'node2', 'ground')
circuit.add_resistor(5, 'node2', 'node3')
circuit.add_resistor(2, 'node3', 'ground')

print(circuit.solve())
