package dev.marcosmoreira.aula.circuitos;

import static dev.marcosmoreira.aula.circuitos.Nand2Lesson.MosType.*;
import static dev.marcosmoreira.aula.circuitos.Nand2Lesson.Slot.*;

/** Ejecutable sin dependencias para auditoría del modelo con javac/java. */
public final class Nand2LessonSmoke {
    private Nand2LessonSmoke() { }

    public static void main(String[] args) {
        int checks = 0;
        Nand2Lesson lesson = new Nand2Lesson();
        require(!lesson.readyToTest(), "No se debe probar un molde vacío"); checks++;
        require(lesson.place(P1, PMOS), "Instalar P1"); checks++;
        require(lesson.place(P2, PMOS), "Instalar P2"); checks++;
        require(lesson.place(N1, NMOS), "Instalar N1"); checks++;
        require(lesson.place(N2, NMOS), "Instalar N2"); checks++;
        require(lesson.readyToTest(), "Listo con cuatro piezas"); checks++;
        for (Nand2Lesson.TruthRow row : lesson.testTruthTable()) {
            require(row.passes(), "Vector NAND incorrecto: " + row); checks++;
            require(lesson.observe(row.a(), row.b()) == row.observed(),
                    "Vista en vivo inconsistente: " + row); checks++;
        }
        require(lesson.isConducting(P1, 0, 0), "P1 activo con A=0"); checks++;
        require(!lesson.isConducting(P1, 1, 0), "P1 inactivo con A=1"); checks++;
        require(!lesson.isConducting(N2, 0, 0), "N2 inactivo con B=0"); checks++;
        require(lesson.isConducting(N2, 0, 1), "N2 activo con B=1"); checks++;
        var saved = lesson.snapshot();
        require(lesson.remove(P1), "Quitar P1"); checks++;
        require(!lesson.readyToTest(), "Prueba deshabilitada sin P1"); checks++;
        lesson.restore(saved);
        require(lesson.readyToTest(), "Restaurar montaje"); checks++;
        lesson.restore(java.util.Map.of());
        require(lesson.place(P1, NMOS), "Admite error de tipo en P1"); checks++;
        require(lesson.place(P2, PMOS), "P2"); checks++;
        require(lesson.place(N1, PMOS), "Admite error de tipo en N1"); checks++;
        require(lesson.place(N2, NMOS), "N2"); checks++;
        require(lesson.testTruthTable().stream().anyMatch(row -> !row.passes()),
                "El modelo debe mostrar un síntoma real de discrepancia"); checks++;
        require(!lesson.place(P1, NMOS), "No sobrescribir un hueco ocupado"); checks++;
        lesson.restore(java.util.Map.of());
        lesson.place(P1, NMOS); lesson.place(P2, PMOS);
        lesson.place(N1, NMOS); lesson.place(N2, PMOS);
        require(lesson.testTruthTable().get(1).observed() == Nand2Lesson.Signal.Z,
                "Detectar nodo flotante ideal"); checks++;
        lesson.restore(java.util.Map.of());
        lesson.place(P1, PMOS); lesson.place(P2, NMOS);
        lesson.place(N1, PMOS); lesson.place(N2, NMOS);
        require(lesson.testTruthTable().get(1).observed() == Nand2Lesson.Signal.X,
                "Detectar contención ideal"); checks++;
        System.out.println("OK: " + checks + " controles de lógica y montaje NAND2 (solo anfitrión)");
    }

    private static void require(boolean ok, String label) {
        if (!ok) throw new AssertionError(label);
    }
}
