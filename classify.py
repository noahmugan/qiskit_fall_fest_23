from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, Aer, execute
import math
from typing import Union, Tuple, Dict
import numpy as np
import matplotlib.pyplot as plt


class Classifier:
    def __init__(self, initial_dimensions: int):
        self.log_dim = int(math.ceil(np.log2(initial_dimensions)))
        self.dimensions = 2**self.log_dim
        self.train_vecs = {}
    def add_train_data(self, cl: str, vec: Union[list, np.ndarray]):
        vec = list(vec) + [0] * (self.dimensions - len(vec))
        if cl in self.train_vecs:
            self.train_vecs[cl] = np.add(vec, self.train_vecs[cl])
        else:
            self.train_vecs[cl] = vec
        return self.train_vecs

    def find_sip(self, test_vec: Union[list, np.ndarray], show_circuit: bool = False)-> Dict[str,int]:
        results = {}
        for cl, train_vec in self.train_vecs.items():
            last_class = cl
            train = QuantumRegister(self.log_dim, name=f"{cl} train qubit")
            test = QuantumRegister(self.log_dim, name="Test qubit")
            swap = QuantumRegister(1, name="Swap qubit")
            cr = ClassicalRegister(1)
            qc = QuantumCircuit(train, test, swap, cr)
            qc.initialize(self.train_vecs[cl], train[:], normalize=True)
            qc.initialize(test_vec, test[:], normalize=True)
            qc.barrier()
            qc.h(swap)
            for i in range(self.log_dim):
                qc.cswap(swap[0], train[i], test[i])
            qc.h(swap)
            qc.measure(swap, cr)
            backend = Aer.get_backend('qasm_simulator')
            job = execute(qc, backend, shots=1024)
            data = job.result().get_counts(qc)
            if '0' in data:
                results[cl] = data['0']
            else:
                results[cl] = 0
        if show_circuit:
            print(f'Showing circuit for {last_class} SIP (Close matplot window to proceed)')
            qc.draw('mpl')
            plt.show()

        return results

    def find_aip(self, test_vec: Union[list, np.ndarray])-> Dict[str,int]:
        altered_test_vec = [i if i > 0 else 0 for i in test_vec]
        altered_train_vecs = {cl: [i if i > 0 else 0 for i in self.train_vecs[cl]] for cl in self.train_vecs.keys()}
        results = {}
        for cl, train_vec in altered_train_vecs.items():
            train = QuantumRegister(self.log_dim, name=f"{cl} train qubit")
            test = QuantumRegister(self.log_dim, name="Test qubit")
            swap = QuantumRegister(1, name="Swap qubit")
            cr = ClassicalRegister(1)
            qc = QuantumCircuit(train, test, swap, cr)
            qc.initialize(altered_train_vecs[cl], train[:], normalize=True)
            qc.initialize(altered_test_vec, test[:], normalize=True)
            qc.barrier()
            qc.h(swap)
            for i in range(self.log_dim):
                qc.cswap(swap[0], train[i], test[i])
            qc.h(swap)
            qc.measure(swap, cr)
            backend = Aer.get_backend('qasm_simulator')
            job = execute(qc, backend, shots=1024)
            data = job.result().get_counts(qc)
            if '0' in data:
                results[cl] = data['0']
            else:
                results[cl] = 0

        return results

    def classify(self, test_vec: Union[list, np.ndarray], show_circuit: bool = False)-> Union[Tuple[str, Dict[str,int], Dict[str, int], Dict[str, int]],Tuple[None,None, None, None]]:
        test_vec = test_vec + [0]*(self.dimensions - len(test_vec))
        if len(self.train_vecs) > 0:
            sip_results = self.find_sip(test_vec=test_vec, show_circuit=show_circuit)
            aip_results = self.find_aip(test_vec=test_vec)

            averaged_results = {cl: (sip_results[cl] + aip_results[cl])/2 for cl in sip_results}
            match = None
            for cl, count in averaged_results.items():
                if match is None or averaged_results[match] < count:
                    match = cl
            return match, averaged_results, sip_results, aip_results
        else:
            return None, None


if __name__ == '__main__':
    test = Classifier(3)
    test.add_train_data("one", [1,2,1,4])
    test.add_train_data('two', [1,6,3,3])
    test.add_train_data('three', [4,7,9,2])

    print(test.classify(np.array([1,2,1,4])))