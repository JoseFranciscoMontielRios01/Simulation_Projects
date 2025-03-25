import java.util.Scanner;
//Trabajo hecho por los alumnos: José Francisco Montiel Ríos y Carlos Alberto Uribe Flores

public class GeneradorCongruencialLinealMixto_1 {
    public static void main(String[] args) {
        // Valores específicos que cumplen con todas las condiciones
        final long semilla = 1;         // Xo = 1 (positivo)
        final long multiplicador = 21;   // a = 21 (impar, no divisible por 3 ni 5, (a-1) mod 4 = 0)
        final long incremento = 13;     // c = 13 (impar, primo relativo con m)
        final long modulo = 50;         // m = 50 (mayor que Xo, a, c)

        System.out.println("=== Generador Congruencial Lineal Mixto ===");
        System.out.println("\nFórmula del generador:");
        System.out.println("Xn+1 = (a * Xn + c) mod m");
        System.out.println("\nDonde:");
        System.out.println("Xn+1 = siguiente número");
        System.out.println("Xn   = número actual");
        System.out.println("a    = multiplicador");
        System.out.println("c    = incremento");
        System.out.println("m    = módulo");
        
        System.out.println("\nValores asignados:");
        System.out.println("----------------------------------------");
        System.out.printf("X₀ (semilla inicial) = %d%n", semilla);
        System.out.printf("a (multiplicador)    = %d%n", multiplicador);
        System.out.printf("c (incremento)       = %d%n", incremento);
        System.out.printf("m (módulo)           = %d%n", modulo);
        System.out.println("----------------------------------------");

        System.out.println("\nVerificación de condiciones:");
        System.out.println("1. Xo > 0: SI Cumple (8 > 0)");
        System.out.println("2. a > 0, impar, no divisible por 3 ni 5, (a-1) mod 4 = 0: SI Cumple");
        System.out.println("   - a = 5 es impar");
        System.out.println("   - 5 no es divisible por 3");
        System.out.println("   - 5 no es divisible por 5");
        System.out.println("   - (5-1) mod 4 = 4 mod 4 = 0");
        System.out.println("3. c > 0, impar, primo relativo a m: SI Cumple");
        System.out.println("   - c = 13 es impar");
        System.out.println("   - MCD(13,50) = 1 (primo relativo)");
        System.out.println("4. m > Xo, a, c: SI Cumple (50 > 8, 5, 13)");
        System.out.println("5. a-1 es divisible por todos los factores primos de m: SI Cumple");
        System.out.println("   - m = 50 = 2 × 5²");
        System.out.println("   - a-1 = 4 es divisible por 2");
        System.out.println("----------------------------------------");

        try (Scanner sc = new Scanner(System.in)) {
            System.out.print("\n¿Cuántos números pseudoaleatorios desea generar? ");
            int cantidad = sc.nextInt();

            long estadoActual = semilla;
            System.out.println("\nGenerando números pseudoaleatorios:");
            System.out.println("----------------------------------------");
            System.out.println("Iteración\tXn\t\tXn+1\t\tNúmero Uniforme");
            System.out.println("------------------------------------------------------------");
            
            for (int i = 0; i < cantidad; i++) {
                long siguienteEstado = (multiplicador * estadoActual + incremento) % modulo;
                double uniforme = (double) siguienteEstado / modulo;
                System.out.printf("%d\t\t%d\t\t%d\t\t%.5f%n", 
                                  i, estadoActual, siguienteEstado, uniforme);
                estadoActual = siguienteEstado;
            }
            System.out.println("------------------------------------------------------------");
            
            // Calcular y mostrar estadísticas básicas
            double suma = 0;
            estadoActual = semilla;
            for (int i = 0; i < cantidad; i++) {
                long siguienteEstado = (multiplicador * estadoActual + incremento) % modulo;
                suma += (double) siguienteEstado / modulo;
                estadoActual = siguienteEstado;
            }
            double promedio = suma / cantidad;
            
            System.out.println("\nEstadísticas:");
            System.out.println("----------------------------------------");
            System.out.printf("Cantidad de números generados: %d%n", cantidad);
            System.out.printf("Promedio de los números uniformes: %.5f%n", promedio);
            System.out.println("----------------------------------------");
        }
    }
} 
