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

def create_gate_from_4(x, y, z, t, verbose = False):
    norm = math.sqrt(x ** 2 + y ** 2 + z ** 2 + t ** 2)
    a, c, b, d = x / norm,  y / norm, z / norm, t / norm
    if verbose:
        print(a, b, c, d)
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


def create_curcuit(testing_gate, trained_gates):
    qc = QuantumCircuit(3 + 2 + 2 + 8 + 4, 2 + 1)
    # h of the control qubit for the swap test
    qc.h([0])
    # h for the indecies
    qc.h([5,6])
    
    #  append test gate    
    qc.append(testing_gate, [1, 2])
    
    qc.barrier()
    # case 11, controls 18
    qc.ccx(5, 6, 18)
    qc.barrier()
    # case 01, controls 16
    qc.ccx(5, 6, 16)
    qc.cx(5, 16)
    qc.barrier()
    # case 10, controls 17
    qc.ccx(5, 6, 17)
    qc.cx(6, 17)
    qc.barrier()
    # case 00, controls 15     
    qc.x([5,6])
    qc.ccx(5, 6, 15)
    qc.x([5,6])
    qc.barrier()
    
    # adding the trained gates
    for i in range(4):
        qc.append(trained_gates[i], [2 * i + 7, 2 * i + 8])
    
    qc.barrier()
    # reading indecies and swapping the states
    qc.append(CSwapGate(), [15, 3, 7])
    qc.append(CSwapGate(), [15, 4, 8])

    qc.append(CSwapGate(), [16, 3, 9])
    qc.append(CSwapGate(), [16, 4, 10])
    
    qc.append(CSwapGate(), [17, 3, 11])
    qc.append(CSwapGate(), [17, 4, 12])
    
    qc.append(CSwapGate(), [18, 3, 13])
    qc.append(CSwapGate(), [18, 4, 14])
    
    qc.barrier()
    
    qc.barrier()
    qc.append(CSwapGate(), [0, 1, 3])
    qc.append(CSwapGate(), [0, 2, 4])
    qc.h(0)
    
    qc.barrier()
    qc.measure(0, 0)
    qc.measure(6, 1)
    qc.measure(5, 2)
    
    return qc

def run_experiment_with_shots(circuit, shots, verbose = True):
    aer_sim = Aer.get_backend('aer_simulator')
    transpiled_circuit = transpile(circuit, aer_sim)
    qobj = assemble(transpiled_circuit)
    results = aer_sim.run(qobj, shots=shots).result()
    counts = results.get_counts()
    if verbose:
        display(plot_histogram(counts))
    return counts

def process_counts(counts, state_to_key, verbose = True):
    res = {}
    for k in counts.keys():
        gate_index, v, value = state_to_key[k[:2]], k[2], counts[k]
        if gate_index in res:
            d = res[gate_index]
            if v in d:
                d[v] += value
            else:
                d[v] = value
        else:
            res[gate_index] = {v: value}

    experiment_results = {}
    for k in sorted(res.keys()):
        d = res[k]
        if '1' in d:
            p = d['1']/(d['1'] + d['0'])
        else:
            p = 0
        experiment_results[k] = p
        if verbose:
            print(f"Probability of 1 in gate {k} is {p}")
    
    return experiment_results

def get_sim_4_vectors(test, four_vectors_with_index, shots=1024, verbose = True):
    assert(len(four_vectors_with_index) == 4)
    id0, vec0 = four_vectors_with_index[0]
    id1, vec1 = four_vectors_with_index[1]
    id2, vec2 = four_vectors_with_index[2]
    id3, vec3 = four_vectors_with_index[3]
    
    gates = list(map(lambda x: create_gate_from_4(*x), [vec0, vec1, vec2, vec3]))
    
    test_gate = create_gate_from_4(*test)
    
    state_to_key = {'00': id0, '01': id1, '10': id2, '11': id3}

    qc = create_curcuit(test_gate, gates)
    
    counts = run_experiment_with_shots(qc, shots, verbose)
    counts_processed = process_counts(counts, state_to_key, verbose)
    
    res = {}
    for k, p in counts_processed.items():
        squared = 1 - 2 * p
        res[k] = squared
    return res

def get_sim_new(test_vector, trained_vectors = trained_vector, shots=4096):
    n = (len(trained_vectors) // 4) * 4
    # all_res = []
    max_score = 0
    max_id = None
    for i in range(0, n, 4):
        sample_trained_vectors = list(map(lambda j: (j, trained_vectors[j]), [i, i+1, i+2, i+3]))
        sims = get_sim_4_vectors(test_vector, sample_trained_vectors, shots=shots, verbose=False)
        # all_res.append(sims)
        res = []
        for k, v in sims.items():
            res.append((v, k))
            if v > max_score:
                max_id = k
                max_score = v
    # print(all_res)
    return max_id, max_score