import java.util.Random;

/**
 * Clase que implementa un Generador Congruencial Lineal Mixto (GCLM).
 * Este generador produce una secuencia de números pseudoaleatorios basada en la fórmula:
 * Xn+1 = (a * Xn + c) mod m
 * donde:
 * - Xn+1: siguiente número en la secuencia
 * - Xn: número actual
 * - a: multiplicador
 * - c: incremento
 * - m: módulo
 */
public class Generador_CLM {
    // Generador de números pseudoaleatorios para inicializar los parámetros
    Random random = new Random();
    
    // Parámetros del sistema
    byte p = 2, d = 64; // p: base del sistema, d: número de bits
    // El número más grande posible es p^d, en este caso 2^64
    
    // Módulo que determina el período del generador
    // Se recomienda que sea lo más grande posible
    long m = (long) Math.pow(p, d);
    
    // Semilla inicial (Xo)
    // Debe ser positiva y menor que m
    long Xo = Math.abs(random.nextLong()) % m;
    
    // Incremento (c)
    // Debe ser positivo, impar y coprimo con m
    long c = Math.abs(random.nextLong()) % m | 1;
    
    /**
     * Genera el multiplicador (a) que cumple con las siguientes condiciones:
     * - a > 0
     * - a debe ser impar
     * - a no debe ser divisible por 3 ni por 5
     * - (a - 1) mod 4 = 0
     * - (a - 1) debe ser divisible por los factores primos de m
     * @return El multiplicador que cumple con todas las condiciones
     */
    public long generarA() {
        long a;
        do {
            // Genera un número impar menor que m
            a = Math.abs(random.nextLong()) % m | 1;
        } while (a % 3 == 0 || a % 5 == 0 || (a - 1) % 4 != 0);
        return a;
    }
    
    /**
     * Método principal que demuestra el uso del generador
     * Crea una instancia del generador y muestra los parámetros generados
     */
    public static void main(String[] args) {
        Generador_CLM generador = new Generador_CLM();
        long a = generador.generarA();
        
        // Muestra los parámetros del generador
        System.out.println("Xo: " + generador.Xo);
        System.out.println("a: " + a);
        System.out.println("c: " + generador.c);
        System.out.println("m: " + generador.m);
    }
}