import socket

N = 15910596760311511967802161284357         #(p*q)
e = 35421826192615868656164957915281

bufferSize  = 4096

localIP     = "127.0.0.1"
localPort   = 30000

UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDPServerSocket.bind((localIP, localPort))

while (True):
    bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
    message = bytesAddressPair[0].decode()
    address = bytesAddressPair[1]
    message = message.split(" ")

    for i in range(0,len(message)-1):
        print(message[i])

#finding d by attacker :(

for i in range (2,sqrt(N)+1):
    p = i
    if(N%p == 0):
        q = N//p
        break

d = modInverse(e, (p-1)*(q-1))

secret_message = ""
for i in range (0, len(message)-1):
    secret_message += chr(pow(int(message[i]),d,N))

print(secret_message)

#Run the below code in google colab to find d



#finding d by attacker using Shor's algorithm
#Source: https://colab.research.google.com/github/quantumlib/Cirq/blob/master/docs/experiments/shor.ipynb#scrollTo=0f-6DbifYArF

#Shor's Algorithm
#Since we are using google colab to run this quantum algorithm
#we are installing cirq library here

# try:
#     import cirq
# except ImportError:
#     !pip install --quiet cirq

# import fractions
# import math
# import random
# import numpy as np
# import sympy
# from typing import Callable, Iterable, List, Optional, Sequence, Union
# import cirq


# """Defines the modular exponential gate used in Shor's algorithm."""
# class ModularExp(cirq.ArithmeticGate):
#     """Quantum modular exponentiation.

#     This class represents the unitary which multiplies base raised to exponent
#     into the target modulo the given modulus. More precisely, it represents the
#     unitary V which computes modular exponentiation x**e mod n:

#         V|y⟩|e⟩ = |y * x**e mod n⟩ |e⟩     0 <= y < n
#         V|y⟩|e⟩ = |y⟩ |e⟩                  n <= y

#     where y is the target register, e is the exponent register, x is the base
#     and n is the modulus. Consequently,

#         V|y⟩|e⟩ = (U**e|y)|e⟩

#     where U is the unitary defined as

#         U|y⟩ = |y * x mod n⟩      0 <= y < n
#         U|y⟩ = |y⟩                n <= y
#     """
#     def __init__(
#         self,
#         target: Sequence[int],
#         exponent: Union[int, Sequence[int]],
#         base: int,
#         modulus: int
#     ) -> None:
#         if len(target) < modulus.bit_length():
#             raise ValueError(
#                 f'Register with {len(target)} qubits is too small for modulus'
#                 f' {modulus}'
#             )
#         self.target = target
#         self.exponent = exponent
#         self.base = base
#         self.modulus = modulus

#     def registers(self) -> Sequence[Union[int, Sequence[int]]]:
#         return self.target, self.exponent, self.base, self.modulus

#     def with_registers(
#         self, *new_registers: Union[int, Sequence[int]]
#     ) -> 'ModularExp':
#         """Returns a new ModularExp object with new registers."""
#         if len(new_registers) != 4:
#             raise ValueError(
#                 f'Expected 4 registers (target, exponent, base, '
#                 f'modulus), but got {len(new_registers)}'
#             )
#         target, exponent, base, modulus = new_registers
#         if not isinstance(target, Sequence):
#             raise ValueError(
#                 f'Target must be a qubit register, got {type(target)}'
#             )
#         if not isinstance(base, int):
#             raise ValueError(
#                 f'Base must be a classical constant, got {type(base)}'
#             )
#         if not isinstance(modulus, int):
#             raise ValueError(
#               f'Modulus must be a classical constant, got {type(modulus)}'
#             )
#         return ModularExp(target, exponent, base, modulus)

#     def apply(self, *register_values: int) -> int:
#         """Applies modular exponentiation to the registers.

#         Four values should be passed in.  They are, in order:
#           - the target
#           - the exponent
#           - the base
#           - the modulus

#         Note that the target and exponent should be qubit
#         registers, while the base and modulus should be
#         constant parameters that control the resulting unitary.
#         """
#         assert len(register_values) == 4
#         target, exponent, base, modulus = register_values
#         if target >= modulus:
#             return target
#         return (target * base**exponent) % modulus

#     def _circuit_diagram_info_(
#       self, args: cirq.CircuitDiagramInfoArgs
#     ) -> cirq.CircuitDiagramInfo:
#         """Returns a 'CircuitDiagramInfo' object for printing circuits.

#         This function just returns information on how to print this operation
#         out in a circuit diagram so that the registers are labeled
#         appropriately as exponent ('e') and target ('t').
#         """
#         assert args.known_qubits is not None
#         wire_symbols = [f't{i}' for i in range(len(self.target))]
#         e_str = str(self.exponent)
#         if isinstance(self.exponent, Sequence):
#             e_str = 'e'
#             wire_symbols += [f'e{i}' for i in range(len(self.exponent))]
#         wire_symbols[0] = f'ModularExp(t*{self.base}**{e_str} % {self.modulus})'
#         return cirq.CircuitDiagramInfo(wire_symbols=tuple(wire_symbols))

# """Function to make the quantum circuit for order finding."""
# def make_order_finding_circuit(x: int, n: int) -> cirq.Circuit:
#     """Returns quantum circuit which computes the order of x modulo n.

#     The circuit uses Quantum Phase Estimation to compute an eigenvalue of
#     the following unitary:

#         U|y⟩ = |y * x mod n⟩      0 <= y < n
#         U|y⟩ = |y⟩                n <= y

#     Args:
#         x: positive integer whose order modulo n is to be found
#         n: modulus relative to which the order of x is to be found

#     Returns:
#         Quantum circuit for finding the order of x modulo n
#     """
#     L = n.bit_length()
#     target = cirq.LineQubit.range(L)
#     exponent = cirq.LineQubit.range(L, 3 * L + 3)

#     # Create a ModularExp gate sized for these registers.
#     mod_exp = ModularExp([2] * L, [2] * (2 * L + 3), x, n)

#     return cirq.Circuit(
#         cirq.X(target[L - 1]),
#         cirq.H.on_each(*exponent),
#         mod_exp.on(*target, *exponent),
#         cirq.qft(*exponent, inverse=True),
#         cirq.measure(*exponent, key='exponent'),
#     )

# def process_measurement(result: cirq.Result, x: int, n: int) -> Optional[int]:
#     """Interprets the output of the order finding circuit.

#     Specifically, it determines s/r such that exp(2πis/r) is an eigenvalue
#     of the unitary

#         U|y⟩ = |xy mod n⟩  0 <= y < n
#         U|y⟩ = |y⟩         n <= y
    
#     then computes r (by continued fractions) if possible, and returns it.

#     Args:
#         result: result obtained by sampling the output of the
#             circuit built by make_order_finding_circuit

#     Returns:
#         r, the order of x modulo n or None.
#     """
#     # Read the output integer of the exponent register.
#     exponent_as_integer = result.data["exponent"][0]
#     exponent_num_bits = result.measurements["exponent"].shape[1]
#     eigenphase = float(exponent_as_integer / 2**exponent_num_bits)

#     # Run the continued fractions algorithm to determine f = s / r.
#     f = fractions.Fraction.from_float(eigenphase).limit_denominator(n)
    
#     # If the numerator is zero, the order finder failed.
#     if f.numerator == 0:
#         return None
    
#     # Else, return the denominator if it is valid.
#     r = f.denominator
#     if x**r % n != 1:
#         return None
#     return r

# def quantum_order_finder(x: int, n: int) -> Optional[int]:
#     """Computes smallest positive r such that x**r mod n == 1.
    
#     Args:
#         x: integer whose order is to be computed, must be greater than one
#            and belong to the multiplicative group of integers modulo n (which
#            consists of positive integers relatively prime to n),
#         n: modulus of the multiplicative group.
#     """
#     # Check that the integer x is a valid element of the multiplicative group
#     # modulo n.
#     if x < 2 or n <= x or math.gcd(x, n) > 1:
#         raise ValueError(f'Invalid x={x} for modulus n={n}.')

#     # Create the order finding circuit.
#     circuit = make_order_finding_circuit(x, n)
    
#     # Sample from the order finding circuit.
#     measurement = cirq.sample(circuit)
    
#     # Return the processed measurement result.
#     return process_measurement(measurement, x, n)

# """Functions for factoring from start to finish."""
# def find_factor_of_prime_power(n: int) -> Optional[int]:
#     """Returns non-trivial factor of n if n is a prime power, else None."""
#     for k in range(2, math.floor(math.log2(n)) + 1):
#         c = math.pow(n, 1 / k)
#         c1 = math.floor(c)
#         if c1**k == n:
#             return c1
#         c2 = math.ceil(c)
#         if c2**k == n:
#             return c2
#     return None


# def find_factor(
#     n: int,
#     order_finder: Callable[[int, int], Optional[int]] = quantum_order_finder,
#     max_attempts: int = 30
# ) -> Optional[int]:
#     """Returns a non-trivial factor of composite integer n.

#     Args:
#         n: Integer to factor.
#         order_finder: Function for finding the order of elements of the
#             multiplicative group of integers modulo n.
#         max_attempts: number of random x's to try, also an upper limit
#             on the number of order_finder invocations.

#     Returns:
#         Non-trivial factor of n or None if no such factor was found.
#         Factor k of n is trivial if it is 1 or n.
#     """
#     # If the number is prime, there are no non-trivial factors.
#     if sympy.isprime(n):
#         print("n is prime!")
#         return None
    
#     # If the number is even, two is a non-trivial factor.
#     if n % 2 == 0:
#         return 2
    
#     # If n is a prime power, we can find a non-trivial factor efficiently.
#     c = find_factor_of_prime_power(n)
#     if c is not None:
#         return c
    
#     for _ in range(max_attempts):
#         # Choose a random number between 2 and n - 1.
#         x = random.randint(2, n - 1)
        
#         # Most likely x and n will be relatively prime.
#         c = math.gcd(x, n)
        
#         # If x and n are not relatively prime, we got lucky and found
#         # a non-trivial factor.
#         if 1 < c < n:
#             return c
        
#         # Compute the order r of x modulo n using the order finder.
#         r = order_finder(x, n)
        
#         # If the order finder failed, try again.
#         if r is None:
#             continue
        
#         # If the order r is even, try again.
#         if r % 2 != 0:
#             continue
        
#         # Compute the non-trivial factor.
#         y = x**(r // 2) % n
#         assert 1 < y < n
#         c = math.gcd(y - 1, n)
#         if 1 < c < n:
#             return c

#     print(f"Failed to find a non-trivial factor in {max_attempts} attempts.")
#     return None

# """Example of factoring via Shor's algorithm (order finding)."""
# # Number to factor
# n = 6

# # Attempt to find a factor
# p = find_factor(n, order_finder=quantum_order_finder)
# q = n // p

# print("Factoring n = pq =", n)
# print("p =", p)
# print("q =", q)

# d = modInverse(e, (p-1)*(q-1))

# print(d)


