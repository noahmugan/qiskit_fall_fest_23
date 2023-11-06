import pickle
import numpy as np

from classify import Classifier


def get_pickled_data(file_path: str) -> np.ndarray:
    with open(file_path, 'rb') as file:
        vector = pickle.load(file)
    return vector

def pickle_data(file_path: str = "/Users/noahmugan/Dropbox/fall_fest_23/") -> None:
    with open(file_path, 'wb') as file:
        # Write the NumPy array to the pickle file
        pickle.dump(file_path, file)

class SizeError(Exception):
    pass

def blank_terminal():
    """
    Helper to blank the terminal.
    """
    print("\033c")

def example() -> bool:
    blank_terminal()
    print(
        "The 8-hour school day of 9am-5pm can be represented by an 8-dimensional vector, where every dimension represents the availability of a given hour.")
    print(
        "Say that professor A is free from 9-10 and 2-5, professor B is free from 9-12 and 3-4, and professor C is free from 10-2.")
    print(
        "To implement SIP with these schedules, we can represent the professors' schedules with the following vectors:")
    print("\tProfessor A: [1, -1, -1, -1, -1, 1, 1, 1]")
    print("\tProfessor B: [1, 1, 1, -1, -1, -1, 1, -1]")
    print("\tProfessor C: [-1, 1, 1, 1, 1, -1, -1, -1]\n")
    print("Say that a student wants to work with the professor whose schedule most closely aligns with their own.")
    print(
        "We can determine the appropriate professor by finding the Hamming distance between the student's schedule and each professor.\n")
    valid = False
    while not valid:
        student_str = input(
            "Input the student's schedule as a list of 8 chronological values separated by spaces, with 1 being a free hour and -1 being a busy hour.\n").strip()
        student_schedule = student_str.split()
        if len(student_schedule) == 8:
            try:
                student_schedule = [int(i) for i in student_schedule]
                valid = True
            except ValueError:
                print(
                    'Invalid input. List values must be "1" to designate a free hour or "-1" to designate a busy hour.')
        else:
            print("Invalid input. Enter 8 values separated by spaces.")
    print("We can now find the SIP and AIP of the student's vector and each professor's vector to find the best match.")
    show_circuit = input("Would you like to see the resulting SIP circuit? (y/n)\n").lower().strip() == 'y'
    p_A = [1, -1, -1, -1, -1, 1, 1, 1]
    p_B = [1, 1, 1, -1, -1, -1, 1, -1]
    p_C = [-1, 1, 1, 1, 1, -1, -1, -1]
    classifier = Classifier(8)
    classifier.add_train_data("Professor A", p_A)
    classifier.add_train_data("Professor B", p_B)
    classifier.add_train_data("Professor C", p_C)
    match, avg_results, sip_results, aip_results = classifier.classify(student_schedule, show_circuit=show_circuit)
    print("SIP Results:")
    for prof, count in sip_results.items():
        print(f"{prof}: {count}")
    print("\nAIP Results:")
    for prof, count in aip_results.items():
        print(f"{prof}: {count}")
    print("\nThe SIP is a slightly more accurate standard of measuring the distance between vectors.\n"
          "However, the quantum circuit to calculate the inner product is unable to distinguish between a positive and negative value.\n"
          "As such, we can set all negative values in every vector equal to 0 and find the AIP as well, which will dramatically decrease the counts for inner products which were negative.\n"
          "If we average these two quantities, we can come up with a good metric for vector closeness.\n")
    print("Averaged Results:")
    for prof, count in avg_results.items():
        print(f"{prof}: {count}")
    print(f"Since {match} had the highest average count of |0> measurements, your student should work with {match}.\n")
    go = input("Continue? (y/n)\n").lower().strip()
    return go == 'y'

def arbitrary():
    blank_terminal()
    print("First, input training vectors as either a .pkl file or a list.")
    classifier = None
    input_type = input('Input "pkl" to load a pkl file or "lst" to load a list:\n')
    while input_type != "done" or classifier is None:
        vector = None
        if input_type == 'pkl':
            filepath = input("Input the filepath for the .pkl file:\n").strip()
            try:
                vector = get_pickled_data(filepath)
            except FileNotFoundError:
                print("Invalid file path")
        elif input_type == 'lst':
            vec_list = input(
                "\nInput the vector as a list of floats or integers separated by spaces. For Hamming distance, have 1 equal a match and -1 be a mismatch\n").strip().split()
            try:
                vector = [float(i) for i in vec_list]
            except ValueError:
                print(
                    'Invalid input. List values must be floats or integers')
        else:
            print("Invalid input.")
        if input_type in ("pkl", "lst") and vector is not None:
            try:
                if classifier is None:
                    classifier = Classifier(len(vector))
                    print()
                else:
                    if len(vector) > classifier.dimensions:
                        raise SizeError
                    print(f"\nYour current classifications are {[i for i in classifier.train_vecs.keys()]}")
                cl = input(
                    "Input the classification for the just-entered vector.\nThis can be more data for an existing classification or data for a new one:\n").strip()
                classifier.add_train_data(cl, vector)
            except SizeError:
                print(f"Error - Dimensions of new data do not match previously established dimensions: {classifier.dimensions}")

        if classifier is None:
            input_type = input('\nInput "pkl" to load a pkl file or "lst" to load a list\n')
        else:
            input_type = input('\nInput "pkl" to load a pkl file, "lst" to load a list, or "done" to finish:\n')

    valid = False
    while not valid:
        test_vector = input(
            "\nInput the test vector as a list of floats or integers separated by spaces. For Hamming distance, have 1 equal a match and -1 be a mismatch\n").strip().split()
        if len(test_vector) <= classifier.dimensions:
            try:
                test_vector = [float(i) for i in test_vector]
                valid = True
            except ValueError:
                print(
                    'Invalid input. List values must be floats or integers')
        else:
            print(f"Error - Dimensions of new data do not match previously established dimensions: {classifier.dimensions}")
    show_circuit = input("Would you like to see the resulting circuit? (y/n)\n").lower().strip() == 'y'
    match, avg_results, sip_results, aip_results = classifier.classify(test_vector, show_circuit=show_circuit)
    print("\nSIP Results:")
    for prof, count in sip_results.items():
        print(f"{prof}: {count}")
    print("\nAIP Results:")
    for prof, count in aip_results.items():
        print(f"{prof}: {count}")
    print("\nAveraged Results:")
    for prof, count in avg_results.items():
        print(f"{prof}: {count}")
    print(f"\nBest match: {match}")
    go = input("\nContinue? (y/n)\n").lower().strip()
    return go == 'y'


if __name__ == '__main__':
    blank_terminal()
    print("Hello. Welcome to the Qiskit-based vector classifier.")
    print("\nThis program uses a quantum algorithm for the symmetric inner-product (SIP) and active inner product (AIP) between vectors to perform linearized Hamming distance-based classification.")
    print("\nGiven a space (e.g. time, the human genome, etc.) you can represent that space via a binary vector, \nwhere each term of the vector corresponds with the existence or absence of a trait within a division of that space.\n")
    print("You can either classify a vector using your own training set, or use our example schedule classifier.")
    choice = input('Type "ex" to try the example scheduler, "stop" to exit the program, or just hit enter to submit your own training data.\n').lower().strip()
    while choice != 'stop':
        print()
        if choice == 'ex':
            go = example()
            if not go:
                choice = 'stop'
            else:
                blank_terminal()
                choice = input(
                    'What next? Type "ex" to try the example scheduler again, "stop" to exit the program, or just hit enter to submit your own training data.\n').lower().strip()

        elif choice == '':
            go = arbitrary()
            if not go:
                choice = 'stop'
            else:
                blank_terminal()
                choice = input(
                    'What next? Type "ex" to try the example scheduler, "stop" to exit the program, or just hit enter to submit your own training data again.\n').lower().strip()

        elif choice != 'stop':
            print("\nInvalid input.")
            choice = input(
                'Type "ex" to try the example scheduler, "stop" to exit the program, or just hit enter to submit your own training data.\n').lower().strip()

