# Quantum Vector Classifier

This is the submission from Noah Mugan for the Fall 2023 UT Austin Fall Fest Hackathon

In this project, I set out to learn about how a quantum circuit can be used to classify vectors in logarithmic time, a significant speedup from the O(N) time taken by classical methods.

First, some background is in order. Let us first speak in terms of binary vectors.
Hamming distance is a value
which describes the number of inconsistencies between two binary
vectors. This is a useful value for comparisons. For example,
say that in a day's schedule, you have hour blocks in which you
are or are not busy. Your day's schedule could then be described
using a vector, with each dimension of the vector describing whether you
are or are not busy. If you find the Hamming distance between
two people's day vectors, you can determine how well their schedules align.

The symmetric inner product, or SIP, is a linearized version of 
Hamming distance. This means that if you sum the inner products of your vector
with a set of other vectors, that should equal the inner product
between your vector and the sum of that set. This is useful to us
because it means you can add up a set of training vectors and compare them all 
at once to a test vector. In a binary vector like our schedule above,
a vector which you can use to find the SIP would have a 1 for an open
hour and a -1 for a busy hour.

The Active inner product is similar to the SIP. While you would put
a -1 for busy hours when finding the SIP, you would put a 0 when finding
the AIP. When you find the AIP using that vector, it only 
counts the number of matching hours between the training cases
and your test case. This means that SIP is slightly better at finding
the similarity between vectors because it considers mismatches as well.

We can use a quantum circuit to approximate the inner product of two vectors.
For a vector of size N, we can use log(N) qubits to create a superposition of 
all possible states between 0 and N. The amplitude of each of these states 
is determined by the value for that state in our original vector.

By inscribing vectors onto a register of qubits as described
above, we can create a quantum circuit in which both our test and train
vectors are described by superpositions on different qubit sets.
We can then utilize an auxiliary qubit as a control for controlled
swap gates, each of which swap the corresponding qubits from each vector register.
By surrounding the set of controlled swap gates with hadamards on the
control qubit, we can measure the control qubit at the end to determine
the inner product between our two inscribed vectors.

When we measure the control qubit, the probability of measuring a 0
is 0.5 + 0.5 * |<vector_1 | vector_2>|^2. As such, the more we measure 0 in repeated trials,
the higher the inner product of vector_1 and vector_2 is.

However, you may notice from our formula that there is no distinction between a 
positive and negative inner product. In binary vectors, this could be solved by taking
the AIP instead of the SIP, since the AIP can only be found from 
vectors with nonnegative terms. 

I employed a similar approach to extend this algorithm to more than
just binary vectors. In my algorithm, I find the inner product of two vectors 
(analogous to the SIP) and then I also find the inner product of 
the two vectors when all negative terms are set to 0 (analogous to the AIP).
By averaging these two quantities, I am able to filter out which vectors only had a high
inner product because it was negative while still retaining some of the accuracy of the AIP.

Because the inner product can be found in a quantum circuit using log(N)
qubits, it presents a speedup compared to classical algorithms characterized
as O(N). As a result, this program is an effective way to showcase
the power of quantum computing and encourage further education.