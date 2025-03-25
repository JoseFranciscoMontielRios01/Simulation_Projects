# Simulation_Projects
This repository contains a Java implementation of a Linear Congruential Generator (LCG), a fundamental algorithm for generating sequences of pseudo-random numbers. The LCG is widely recognized for its simplicity and efficiency in producing pseudo-random sequences.

Overview
The core of this implementation revolves around the recurrence relation:

lua
Copiar
Editar
Xₙ₊₁ = (a * Xₙ + c) mod m
Where:

Xₙ₊₁ is the next number in the sequence.

Xₙ is the current number.

a is the multiplier.

c is the increment.

m is the modulus.

Features
Parameter Verification: The program verifies that the chosen parameters (a, c, m, and the initial seed X₀) satisfy conditions necessary for achieving a full-period sequence, ensuring the generator's effectiveness.

User Interaction: Upon execution, the program prompts the user to specify the number of pseudo-random numbers to generate.

Detailed Output: For each iteration, the program displays:

The iteration number.

The current state (Xₙ).

The next state (Xₙ₊₁).

The normalized pseudo-random number (Xₙ₊₁ / m).

Statistical Analysis: After generating the sequence, the program calculates and displays the average of the generated pseudo-random numbers, providing insight into their distribution.

Usage
Compilation: Compile the Java source file using a Java compiler:

nginx
Copiar
Editar
javac GeneradorCongruencialLinealMixto_1.java
Execution: Run the compiled class file:

nginx
Copiar
Editar
java GeneradorCongruencialLinealMixto_1
Interaction: Follow the on-screen prompts to specify the number of pseudo-random numbers you wish to generate.

Example Output
markdown
Copiar
Editar
=== Generador Congruencial Lineal Mixto ===

Fórmula del generador:
Xn+1 = (a * Xn + c) mod m

Donde:
Xn+1 = siguiente número
Xn   = número actual
a    = multiplicador
c    = incremento
m    = módulo

Valores asignados:
----------------------------------------
X₀ (semilla inicial) = 1
a (multiplicador)    = 21
c (incremento)       = 13
m (módulo)           = 50
----------------------------------------

Verificación de condiciones:
1. Xo > 0: SI Cumple (1 > 0)
2. a > 0, impar, no divisible por 3 ni 5, (a-1) mod 4 = 0: SI Cumple
   - a = 21 es impar
   - 21 no es divisible por 3
   - 21 no es divisible por 5
   - (21-1) mod 4 = 20 mod 4 = 0
3. c > 0, impar, primo relativo a m: SI Cumple
   - c = 13 es impar
   - MCD(13,50) = 1 (primo relativo)
4. m > Xo, a, c: SI Cumple (50 > 1, 21, 13)
5. a-1 es divisible por todos los factores primos de m: SI Cumple
   - m = 50 = 2 × 5²
   - a-1 = 20 es divisible por 2 y 5
----------------------------------------

¿Cuántos números pseudoaleatorios desea generar? 10

Generando números pseudoaleatorios:
----------------------------------------
Iteración	Xn		Xn+1		Número Uniforme
------------------------------------------------------------
0		1		34		0.68000
1		34		27		0.54000
2		27		20		0.40000
3		20		13		0.26000
4		13		6		0.12000
5		6		49		0.98000
6		49		42		0.84000
7		42		35		0.70000
8		35		28		0.56000
9		28		21		0.42000
------------------------------------------------------------

Estadísticas:
----------------------------------------
Cantidad de números generados: 10
Promedio de los números uniformes: 0.55000
----------------------------------------
Notes
The chosen parameters (a = 21, c = 13, m = 50, X₀ = 1) are selected to fulfill conditions that ensure a full-period LCG, meaning the generator will produce all possible values before repeating any.

The program includes detailed explanations and verifications of these conditions to provide users with a clear understanding of the generator's setup.
