#initialization
import matplotlib.pyplot as plt
import numpy as np
import math

# importing Qiskit
from qiskit import IBMQ, Aer, assemble, transpile
from qiskit import QuantumCircuit
from qiskit.providers.ibmq import least_busy
from qiskit.circuit.library import RYGate

# import basic plot tools
from qiskit.visualization import plot_histogram
import qiskit.quantum_info as qi
from qiskit.circuit.library import CSwapGate
from qiskit.circuit.library import RYGate

from trained import trained_vector

def run_experiment(circuit, verbose = False):
    aer_sim = Aer.get_backend('aer_simulator')
    transpiled_circuit = transpile(circuit, aer_sim)
    qobj = assemble(transpiled_circuit)
    results = aer_sim.run(qobj, shots=8192).result()
    counts = results.get_counts()
    return counts

def gate_from_state(a, b):
    norm = math.sqrt(a ** 2 + b ** 2)
    x, y = a / norm, b / norm
    if y >= 0:
        theta = np.arccos(x)
    elif x <= 0 and y <= 0:
        theta = 2 * np.pi - np.arccos(x)
    elif x >= 0 and y <= 0:
        theta = 2 * np.pi - np.arccos(x)
    U = RYGate(theta * 2) 
    U = RYGate(theta * 2)
    return U

def create_gate_from_4(x, y, z, t):
    norm = math.sqrt(x ** 2 + y ** 2 + z ** 2 + t ** 2)
    a, c, b, d = x / norm,  y / norm, z / norm, t / norm
    ab_norm = math.sqrt(a ** 2 + b ** 2)
    cd_norm = math.sqrt(c ** 2 + d ** 2)
    U_first = gate_from_state(ab_norm, cd_norm)
    U_ab = gate_from_state(a, b)
    U_ab_inverse = U_ab.inverse()
    
    U_cd = gate_from_state(c, d)
    
    qr = QuantumCircuit(1)
    qr.append(U_ab_inverse,[0])
    qr.append(U_cd,[0])
    U_ab_cd = qr.to_gate(label ="ab->cd")
    cU_ab_cd = U_ab_cd.control(1)
    
    main = QuantumCircuit(2)
    main.append(U_first, [0])
    main.append(U_ab, [1])
    main.append(cU_ab_cd, [0, 1])
    
    return main.to_gate(label = f"U")


def get_sim_score(v1, v2):
    g1 = create_gate_from_4(v1[0], v1[1], v1[2], v1[3])
    g2 = create_gate_from_4(v2[0], v2[1], v2[2], v2[3])
    qc = QuantumCircuit(5, 1)
    qc.i(0)
    qc.append(g1, [1, 2])
    qc.append(g2, [3, 4])
    qc.barrier()
    qc.h(0)
    qc.append(CSwapGate(), [0, 1, 3])
    qc.append(CSwapGate(), [0, 2, 4])
    qc.h(0)

    qc.barrier()
    qc.measure(0, 0)

    c = run_experiment(qc)
    if '1' in c:
        p = c['1'] / (c['0'] + c['1'])
    else:
        p = 0.0
    return 1 - 2 * p

def quantum_get_closest_index(vector):
    ans = None
    max_sim = 0
    for (i, t) in enumerate(trained_vector):
        score = get_sim_score(vector, t)
        if score > max_sim:
            ans = i
            max_sim = score
    return ans, max_sim
