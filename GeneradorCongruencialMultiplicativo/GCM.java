import java.util.Random;
public class GCM {
	
    // módulo (m), semilla (X0), multiplicador (a), período teórico (m-1).
    private final long m, X0, a, periodo;
    private final Random numAleatorio = new Random(); 

    public GCM() {
        // Paso 1) Elegir tipo de módulo: 0=decimal, 1=binario, 2=primo.
        int tipo = numAleatorio.nextInt(3);  
        // Genera un entero 0, 1 o 2 para seleccionar uno de los tres casos.

        if (tipo == 0) {
            // ---------- Caso DECIMAL ----------
            // m = 10^d, con d >= 1
            int dDec;  
            do {
                dDec = 1 + numAleatorio.nextInt(8);  
                // Elige un valor dDec entre 1 y 8 (inclusive).
            } while (dDec < 1);  
            this.m = (long) Math.pow(10, dDec);  
            // Convierte 10^dDec a long y lo asigna a m.

            // Paso 2) Generar semilla X0 aleatoria en ∈ [1,2,..., m−1], impar, no divisible entre 5.
            long valorSemilla;  
            do {
                valorSemilla = Math.abs(numAleatorio.nextLong()) % m;  
                // Genera un long aleatorio (puede ser negativo), lo hace positivo con abs, y lo reduce al rango [0, m-1] con % m.
            } while (valorSemilla == 0 || valorSemilla % 2 == 0 || valorSemilla % 5 == 0);
            // Repite si valorSemilla es 0, par o divisible por 5.
            this.X0 = valorSemilla; // Asigna la semilla final a X0.

            // Paso 3) Generar 'a' de la forma 200·t ± p.
            int[] pVals = {3, 11, 13, 19, 21, 27, 29, 37, 53, 59, 61, 67, 69, 77, 83, 91}; // Arreglo con valores permitidos de p
            long candA;  
            do {
                int t = 1 + numAleatorio.nextInt(1000); // Elige un entero t en [1, 1000]
                int p = pVals[numAleatorio.nextInt(pVals.length)]; // Elige aleatoriamente uno de los valores de pVals 
                if (numAleatorio.nextBoolean()) {
                    candA = 200L * t + p;  // Calcula 200·t + p.
                } else {
                    candA = 200L * t - p;  // Calcula 200·t - p.
                }
            } while (candA <= 0 || candA >= m || candA % 2 == 0 || candA % 5 == 0); // Repite si candA es ≤ 0, ≥ m, par o divisible por 5.
            this.a = candA; // Asigna el multiplicador final "a".  

            // Paso 4) Período decimal.
            if (dDec >= 5) {
                this.periodo = 5L * (long) Math.pow(10, dDec - 2); // Si dDec ≥ 5, período = 5 × 10^(dDec−2).
            } else {
                long per2 = (dDec == 1) ? 1 : (long) Math.pow(2, dDec - 2); // Si dDec<5, calcula período de la parte 2^x: si dDec=1 => per2=1; sino 2^(dDec−2).
                long per5 = 4L * (long) Math.pow(5, dDec - 1); // Calcula período de la parte 5^x: 4 × 5^(dDec−1).
                this.periodo = mcm(per2, per5); // El período es el MCM de per2 y per5.
            }

        } else if (tipo == 1) {
            // ---------- Caso BINARIO ----------
            // m = 2^d, con d >= 3.
            int dBin;
            do {
                dBin = 3 + numAleatorio.nextInt(6);
                // Elige dBin en [3, 8].
            } while (dBin < 3);  
            this.m = 1L << dBin; // Equivale a 2^dBin, usando desplazamiento de bits.

            // Paso 2) Generar semilla X0 aleatoria en ∈ [1,2,..., m−1], impar.
            long valorSemilla;
            do {
                valorSemilla = Math.abs(numAleatorio.nextLong()) % m;
                // Genera número aleatorio positivo en [0, m-1].
            } while (valorSemilla == 0 || valorSemilla % 2 == 0);
            // Repite si es 0 o par
            this.X0 = valorSemilla; // Asigna la semilla impar final.

            // Paso 3) Generar 'a' de la forma 8·t ± 3.
            long candA;
            do {
                int t = 1 + numAleatorio.nextInt(1000);
                // Elige un entero t en [1, 1000].
                candA = 8L * t + 3;  
                // Calcula 8·t + 3.
                if (candA >= m) {
                    candA = 8L * t - 3;  
                    // Si 8·t+3 ≥ m, usar 8·t−3.
                }
            } while (candA <= 0 || candA >= m || candA % 2 == 0);
            // Repite si candA ≤ 0, ≥ m o par
            this.a = candA;  
            // Asigna el multiplicador impar final.

            // Paso 4) Período binario = m / 4.
            this.periodo = this.m / 4;  
            // Equivalente a 2^(dBin−2).

        } else {
            // ---------- Caso PRIMO ----------
            // Paso 1) Generar m primo pseudoaleatorio.
            long valorM;
            do {
                valorM = Math.abs(numAleatorio.nextLong()) % 100000L + 2;
                // Genera número en [2,100001]
            } while (!esPrimo(valorM));
            // Repite hasta que valorM sea primo.
            this.m = valorM;  
            // Asigna m como primo encontrado

            // Paso 2) Generar semilla X0 en ∈ [1,2,..., m−1].
            long valorSemilla;
            do {
                valorSemilla = Math.abs(numAleatorio.nextLong()) % m;
                // Número aleatorio en [0, m-1].
            } while (valorSemilla == 0);
            // Repite si es 0
            this.X0 = valorSemilla;  
            // Asigna la semilla en [1, m-1].

            // Paso 3) Generar 'a' probando candidatos aleatorios en ∈ [2,3,..., m−1].
            this.a = generarRaizPrimitivaAleatoria(this.m);
            // Llama al método que busca raíz primitiva

            // Paso 4) Período para primo = m − 1.
            this.periodo = m - 1;
        }
    }
    
    public void ImprimirParametros () {
        System.out.println("=== Parámetros para un Generador Congruencial Multiplicativo ===");
        System.out.println("Valor para ´m´ (módulo)           : " + m + "  (Valor binario: " + Long.toBinaryString(m) + ")");
        System.out.println("Valor para ´Xo´ (semilla inicial) : " + X0 + "  (Valor binario: " + Long.toBinaryString(X0) + ")");
        System.out.println("Valor para ´a´ (multiplicador)    : " + a + "  (Valor binario: " + Long.toBinaryString(a) + ")");
        System.out.println("¿Cuál es el período teórico?      : " + periodo);
        System.out.println();
    }

    // Verifica si 'n' es primo (optimización 6k ± 1).
    private boolean esPrimo(long n) {
        if (n <= 3) {
            return n > 1;  
            // Retorna true si n es 2 o 3; false si n <= 1.
        }
        if (n % 2 == 0 || n % 3 == 0) {
            return false;  
            // Si n divisible por 2 o 3, no es primo.
        }
        for (long i = 5; i * i <= n; i += 6) {
            // Probar i de la forma 6k−1 y 6k+1
            if (n % i == 0 || n % (i + 2) == 0) {
                return false;  
                // Si n divisible por i o i+2, no es primo.
            }
        }
        return true;  
        // Si pasa todas las pruebas, n es primo
    }

    // Genera un multiplicador 'a' que sea raíz primitiva módulo "m",
    // probando candidatos aleatorios en ∈ [2,3,..., m−1]. Nota: La función totiente de Euler cuenta los enteros positivos hasta un número dado "n" que son relativamente primos a "n".
    private long generarRaizPrimitivaAleatoria(long m) {
        long phi = m - 1;                                  // El método recibe el módulo φ(m) o phi(m) para que sea = m−1.
        long[] factores = factorizarN(phi);                // Llamamos a factorizarN(φ), que devuelve un arreglo con los factores primos únicos de φ.

        // Probamos un buble infinito de candidatos aleatorios en el rango ∈ [2,3,..., m−1] hasta encontrar raíz primitiva.
        while (true) {
            // Genera un número aleatorio en el rango ∈ [2,3,..., m−1]:
            long candidato = 2 + (Math.abs(numAleatorio.nextLong()) % (m - 2)); // Se genera un número al azar (quizás negativo); se reduce al rango [0, m-3] + 2 = [2, m-1]. Potencial "a".
            boolean esRaiz = true;                          // Supondremos que es efectivamente raíz primitiva, hasta verificar lo contrario.

            // Verificamos la condición de la raíz primitiva: para cada factor de φ,
            // candidato^(φ/f) mod m. Un número "g" es raíz primitiva si su orden multiplicativo es exactamente "𝜙". Nos aseguramos de que ninguna de las potencias parciales sea 1.
            for (long f : factores) {
                if (powMod(candidato, phi / f, m) == 1) {   // Si resulta ser 1 (no debería); entonces esRaiz = false y salimos del for. 
                    esRaiz = false;
                    break;                                  // Salimos del bucle de factores.
                }
            }
            if (esRaiz) { // Si pasó todas las pruebas, devolvemos el candidato calculado y totalmente válido.
                return candidato;
            }
        } 
    } // Sino, bucle que se repite sin parar, y así se prueba otro candidato.
    
    // Exponenciación modular rápida, denominada powMod: implementa el algoritmo de exponenciación modular en tiempo O(log exp).
    // Este método calcula la (base^exp) % modulo usando “exponenciación rápida” (algoritmo binario). Es para calcular el candidato^(φ/f) mod m sin crear números enormes. 
    private long powMod(long base, long exp, long mod) {
        long resultado = 1;                                  // Inicializamos siempre el resultado en 1.
        base %= mod;                                         // Reducimos la base % m al rango ∈ [0,..., m−1] antes de empezar. Así trabajamos siempre con números reducidos.
        while (exp > 0) {                                    // Mientras el exponente exp sea mayor que 0, seguimos iterando.
            if ((exp & 1) == 1) {                            // Si el bit menos significativo de exp es 1. Esto equivale a decir “si exp es impar”.
                resultado = (resultado * base) % mod;        // En ese caso, multiplicamos el resultado por la base, y volvemos a tomar % mod.
            }											   	 // Es la parte que “incluye” el factor actual en la potencia.
            base = (base * base) % mod;                      // Con cada iteración elevamos la base al cuadrado y tomamos el módulo. Con cada paso es: base → base^2; exp → exp/2.
            exp >>= 1;                                       // El operador >>= 1 desplaza todos los bits de exp una posición a la derecha. Equivale a exp = exp/2 (enteros).
        }
        return resultado;                                    // Devuelve el resultado que contiene: base^exp % mod. Para esto está diseñado el powMod.
    }

    // Factoriza n en sus factores primos únicos.
    private long[] factorizarN(long n) {
        long[] arrTemp = new long[64]; // Arreglo temporal para factores con un tamaño 64 que usaremos para acumular posibles factores primos.
        int contador = 0; // El Contador llevará la cuenta de cuántos factores encontramos.
        long num = n; // Copia de "n" que iremos reduciendo al dividir por sus factores.

        // Probar divisor 2 (único par).
        if (num % 2 == 0) { 
        	arrTemp[contador++] = 2; // Si num es divisible entre 2, guardamos el “factor 2” en el contador.
            while (num % 2 == 0) {
                num /= 2; // Luego, con el while dividimos repetidamente num entre 2 hasta que ya no sea múltiplo de 2.
            }
        }

        // Probar divisores impares 3, 5, 7, ..., hasta sqrt(num), ósea, la raiz cuadrada (square root) de num.
        for (long i = 3; i * i <= num; i += 2) { // Aumentamos i += 2 (solo ímpares). La condición significa “hasta la raíz cuadrada de num”. Si no hay un factor hasta la raíz, resultará ser primo.
            if (num % i == 0) { // Cada vez que encuentras que num % i == 0, guardás i en el arreglo temporal con el contador en aumento.
            	arrTemp[contador++] = i;
                while (num % i == 0) { // Después, en el while; decidiremos que si num % i == 0: dividiremos el num entre i; esto reduce al máximo num dividiéndolo por i repetidamente.
                    num /= i;
                }
            }
        }

        if (num > 1) { // Después de dividir por todos los factores hasta la raíz, si aún sobra un valor mayor que 1, entonces es primo.
        	arrTemp[contador++] = num;
        }

        long[] factores = new long[contador]; // Creamos un nuevo arreglo factores de tamaño exacto de Contador.
        System.arraycopy(arrTemp, 0, factores, 0, contador);       // Copiamos los factores únicos (desde el arrTemp[0] hasta arrTemp[Contador-1]) al resultado del nuevo arreglo.
        return factores;                                     // Devolvemos factores, que contiene los factores primos únicos de "n".
    }

    // Mínimo común múltiplo.
    private long mcm(long a, long b) {
        return (a / mcd(a, b)) * b;  
        // mcm(a,b) = (a / gcd(a,b)) * b
    }

    // Máximo común divisor (Euclides).
    private long mcd(long a, long b) {
        while (b != 0) {
            long temp = b;  
            b = a % b;  
            a = temp;  
            // Intercambia y reduce hasta b = 0.
        }
        return a;  
        // Cuando b = 0, a es el GCD.
    }

    // Genera el siguiente valor de la secuencia: X_{n+1} = (a * X_n) mod m; la fórmula básica de un Generador Congruencial Multiplicativo.
    private long siguienteValorXn(long xi) {
        return (a * xi) % m; // Multiplica "xi" por "a" y aplica módulo "m".
    }

    public void imprimirIteraciones(int n) {
        // Imprime un encabezado indicando que vamos a mostrar las últimas n iteraciones.
        // junto con la verificación de si la semilla X₀ reaparece antes.
        System.out.println("=== Últimas " + n + " iteraciones y sus valores uniformes (con verificación de período) ===");

        long xi = X0;                // 1) Inicializamos 'xi' con la semilla X0.
        long corte = periodo - n;    // 2) Calculamos cuántos pasos debemos avanzar antes de imprimir los últimos n valores: 'corte' representa la posición X_{periodo−n} en la secuencia.

        for (long i = 1; i <= corte; i++) { // Primer bucle: avanzamos hasta X_{corte}, verificando si X₀ reaparece antes.
            xi = siguienteValorXn(xi);  // 3) Calculamos la siguiente iteración de la sucesión: Xi = (a * X_{i-1}) mod m.

            if (xi == X0) { // 4) Comprobamos si al calcular Xi volvimos a la semilla X₀:
                System.out.println("Semilla Xo reapareció en iteración " + i + ", período incompleto. Período = " + i);
                System.out.println();
                return;               // Salimos del método, ya no imprimimos los últimos n valores.
            }
        }

        // --- Si llegamos hasta aquí, significa que NO volvimos a X₀ antes de X_{corte}.
        // Ahora imprimimos las últimas n iteraciones (desde X_{corte+1} hasta X_{periodo}).
        for (int i = 1; i <= n; i++) {
            xi = siguienteValorXn(xi);        // 5) En cada paso, calculamos Xi para la posición corte + i.
            double uniforme = xi / (double) m; // 6) Convertimos Xi en número uniforme en [0,1].

            System.out.printf("Xn = %d | Núm. uniforme = %.5f%n", corte + i, uniforme);
        }

        System.out.println("Periodo completo encontrado en la iteración " + periodo + ".");
        System.out.println();
    }

    public static void main(String[] args) {
    	GCM generador = new GCM();
        generador.imprimirIteraciones(5);
        generador.ImprimirParametros ();
    }
}