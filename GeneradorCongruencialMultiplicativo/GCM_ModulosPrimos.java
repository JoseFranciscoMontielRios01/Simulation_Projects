import java.util.Random;

public class GCM_ModulosPrimos {
    // Lista fija de posibles módulos primos (cada uno con sufijo L para indicarle a Java que son long)
    private static final long[] moduloP = {
        32057L, 32537L, 32911L, 32687L, 32603L, 32707L, 32933L
    };

    // Variables fundamentales:
    // m        → El módulo actual que usará este objeto
    // X0       → La semilla inicial aleatoria en [1 .. m−1]
    // a        → El multiplicador (una raíz primitiva módulo m)
    // periodo  → El período teórico máximo, igual a m−1 para m primo
    private final long m, X0, a, periodo;

    // Objeto Random de Java para todas las elecciones aleatorias que necesitemos
    private final Random numAleatorio = new Random();

    /**
     * Constructor que recibe un módulo específico (ya no elige aleatorio entre moduloP).
     * Para ese módulo genera:
     *   1) Semilla X0 aleatoria en [1 .. m−1]
     *   2) Multiplicador 'a' (raíz primitiva módulo m)
     *   3) Calcula el período teórico (m−1)
     *
     * @param moduloFijo El módulo primo específico para este generador
     */
    public GCM_ModulosPrimos(long moduloFijo) {
        this.m = moduloFijo; // Asignamos directamente el módulo recibido

        long valorSemilla;   // Declaramos la variable para la semilla X0
        do {
            // Generamos un long aleatorio, lo hacemos positivo con Math.abs(),
            // luego tomamos % (m−1) para llevarlo al rango [0 .. m−2], y finalmente +1 para [1 .. m−1].
            valorSemilla = 1 + (Math.abs(numAleatorio.nextLong()) % (m - 1));
        } while (valorSemilla == 0); // Aseguramos que sea distinto de 0 (aunque con +1 no debería, pero por seguridad)
        this.X0 = valorSemilla;     // Asignamos la semilla X0 en el rango [1 .. m−1]

        // Generamos el multiplicador 'a', buscando una raíz primitiva módulo m
        this.a = generarRaizPrimitivaAleatoria(this.m);

        // El período máximo teórico para un módulo primo es m−1
        this.periodo = m - 1;
    }

    /**
     * Imprime en consola todos los parámetros del generador para el módulo actual:
     *   - Valor de m (módulo)
     *   - Valor de X0 (semilla inicial)
     *   - Valor de a (multiplicador / raíz primitiva)
     *   - Valor del período teórico (m−1)
     */
    public void ImprimirParametros() {
        System.out.println("=== Parámetros para m = " + m + " ===");
        System.out.println("Valor para 'm' (módulo)           : " + m);
        System.out.println("Valor para 'X0' (semilla inicial) : " + X0);
        System.out.println("Valor para 'a' (multiplicador)    : " + a);
        System.out.println("¿Cuál es el período teórico?      : " + periodo);
        System.out.println(); // Línea en blanco para separar de la siguiente sección
    }

    /**
     * Genera un multiplicador 'a' que sea raíz primitiva módulo m.
     * 
     * Proceso:
     *  1) Calcula φ(m) = m − 1      (porque m es primo)
     *  2) Factoriza φ(m) en sus factores primos únicos
     *  3) Prueba candidatos aleatorios en [2 .. m−1] hasta encontrar uno que cumpla:
     *     Para cada factor f de φ, candidato^(φ/f) mod m != 1
     *
     * @param m El módulo primo para el cual buscamos raíz primitiva
     * @return Una raíz primitiva 'a' en [2 .. m−1]
     */
    private long generarRaizPrimitivaAleatoria(long m) {
        long phi = m - 1;                   // φ(m) = m − 1 para m primo
        long[] factores = factorizarN(phi); // Factoriza φ en factores primos únicos

        while (true) {
            // Generamos un candidato en [2 .. m−1]:
            //   Primero obtenemos un long aleatorio, lo hacemos positivo,
            //   tomamos % (m−2) → rango [0 .. m−3], y le sumamos 2 → [2 .. m−1].
            long candidato = 2 + (Math.abs(numAleatorio.nextLong()) % (m - 2));
            boolean esRaiz = true;           // Suponemos que es raíz primitiva hasta demostrar lo contrario

            // Verificamos la condición de raíz primitiva:
            //   Para cada factor f de φ(m):
            //     calculamos candidato^(φ/f) mod m, si alguno == 1, no es raíz
            for (long f : factores) {
                if (powMod(candidato, phi / f, m) == 1) {
                    esRaiz = false; // Si alguna potencia parcial es 1, el candidato no sirve
                    break;          // Salimos del bucle de factores
                }
            }
            if (esRaiz) {
                return candidato; // Si pasó todas las pruebas, devolvemos el candidato
            }
            // Si no es raíz, el while se repite y probamos otro candidato
        }
    }

    /**
     * Calcula el siguiente valor en la secuencia congruencial multiplicativa:
     *   X_{n+1} = (a * X_n) mod m
     *
     * @param xi El valor actual X_n
     * @return  El siguiente valor X_{n+1}
     */
    private long siguienteValorXn(long xi) {
        return (a * xi) % m; // Multiplicamos xi por a y tomamos módulo m
    }

    /**
     * Factoriza un número n en sus factores primos únicos.
     *
     * Proceso:
     *  1) Separa factor 2 si aplica
     *  2) Prueba divisores impares desde 3 hasta sqrt(n)
     *  3) Si queda un residuo > 1, lo agrega como factor primo final
     *
     * @param n El número a factorizar (en general φ(m))
     * @return  Un arreglo con los factores primos únicos de n
     */
    private long[] factorizarN(long n) {
        long[] arrTemp = new long[64]; // Arreglo temporal para acumular factores (tamaño arbitrario 64)
        int contador = 0;              // Contador de cuántos factores hemos encontrado
        long num = n;                  // Copia de trabajo del valor n

        // Paso 1: Factorizar 2 (único primo par)
        if (num % 2 == 0) {
            arrTemp[contador++] = 2;   // Registramos el factor 2
            while (num % 2 == 0) {
                num /= 2;             // Dividimos repetidamente por 2 hasta que ya no sea múltiplo
            }
        }

        // Paso 2: Factorizar impares (3, 5, 7, ...) hasta sqrt(num)
        for (long i = 3; i * i <= num; i += 2) {
            if (num % i == 0) {
                arrTemp[contador++] = i; // Registramos el factor primo i
                while (num % i == 0) {
                    num /= i;           // Dividimos repetidamente por i
                }
            }
        }

        // Paso 3: Si queda un residuo > 1, también es primo
        if (num > 1) {
            arrTemp[contador++] = num;
        }

        // Creamos el arreglo definitivo con el tamaño exacto de factores encontrados
        long[] factores = new long[contador];
        System.arraycopy(arrTemp, 0, factores, 0, contador);
        return factores; // Devolvemos solo los factores válidos
    }

    /**
     * Implementa exponenciación modular rápida:
     *   Calcula (base^exp) % mod en O(log exp) usando algoritmo binario.
     *
     * @param base La base de la potencia
     * @param exp  El exponente
     * @param mod  El módulo
     * @return     (base^exp) mod mod
     */
    private long powMod(long base, long exp, long mod) {
        long resultado = 1;     // Inicializamos resultado = 1
        base %= mod;            // Reducimos la base al rango [0 .. mod−1]
        while (exp > 0) {       // Mientras queden bits en el exponente
            if ((exp & 1) == 1) {
                // Si el bit menos significativo de exp es 1, multiplicamos resultado por base y tomamos mod
                resultado = (resultado * base) % mod;
            }
            // Elevamos base al cuadrado y tomamos mod
            base = (base * base) % mod;
            // Desplazamos exp a la derecha → exp = exp / 2
            exp >>= 1;
        }
        return resultado; // Devolvemos la potencia modular
    }

    /**
     * Para este módulo en particular (m, X0, a), avanza la secuencia hasta la iteración (periodo − n),
     * y luego imprime las últimas n iteraciones junto con su valor uniforme [0,1).
     *
     * @param n Número de iteraciones finales que deseamos imprimir
     */
    public void imprimirIteraciones(int n) {
        System.out.println("=== Últimas " + n + " iteraciones para m = " + m + " ===");

        long xi = X0;                  // Iniciamos con la semilla X0
        long corte = periodo - n;      // Calculamos en qué punto debemos empezar a imprimir

        // Avanzamos la secuencia hasta la iteración X_{corte}, comprobando si la semilla reaparece antes
        for (long i = 1; i <= corte; i++) {
            xi = siguienteValorXn(xi); // Calculamos X_i = (a * X_{i−1}) mod m

            // Si en algún punto regresamos a X0, el período es menor de lo teórico
            if (xi == X0) {
                System.out.println("Semilla X0 reapareció en iteración " + i + ", período incompleto. Período = " + i);
                System.out.println();
                return; // Salimos porque ya no tiene sentido imprimir las últimas n
            }
        }

        // Si llegamos aquí, la semilla no reapareció antes de X_{corte}. Imprimimos las últimas n iteraciones:
        for (int i = 1; i <= n; i++) {
            xi = siguienteValorXn(xi);               // Calculamos X_{corte+i}
            double uniforme = xi / (double) m;        // Convertimos Xi a número uniforme en [0,1)
            System.out.printf("Xn = %d | Núm. uniforme = %.5f%n", corte + i, uniforme);
        }

        System.out.println("Periodo completo encontrado en la iteración " + periodo + ".");
        System.out.println();
    }

    public static void main(String[] args) {
        // Recorremos TODOS los módulos definidos en moduloP
        for (long mod : moduloP) {
            // Para cada módulo, instanciamos el generador con ese módulo fijo
            GCM_ModulosPrimos generador = new GCM_ModulosPrimos(mod);

            // Imprimimos las últimas 5 iteraciones y sus valores uniformes
            generador.imprimirIteraciones(5);

            // Imprimimos los parámetros generados para este módulo
            generador.ImprimirParametros();
        }
    }
}
