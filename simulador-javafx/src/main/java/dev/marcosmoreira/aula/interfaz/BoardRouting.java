package dev.marcosmoreira.aula.interfaz;

import dev.marcosmoreira.aula.circuitos.Nand2Lesson.Net;
import dev.marcosmoreira.aula.circuitos.Nand2Lesson.Signal;
import dev.marcosmoreira.aula.circuitos.Nand2Lesson.Slot;

import java.util.List;

/**
 * Plano normalizado de la placa educativa: una fuente para los trazos 2D/3D.
 * Las redes son las del modelo digital, no pistas validadas para fabricación.
 * Tampoco representan buses de datos de una CPU: este taller es de un bit.
 */
final class BoardRouting {
    record Point(double x, double y) { }
    record Segment(Net net, Point a, Point b) { }

    private BoardRouting() { }

    static Point slot(Slot slot) {
        return switch (slot) {
            case P1 -> new Point(.33, .36);
            case P2 -> new Point(.67, .36);
            case N1 -> new Point(.33, .72);
            case N2 -> new Point(.67, .72);
        };
    }

    static String color(Net net) {
        return switch (net) {
            case VDD -> "#d0a55d";
            case GND -> "#a0bdaf";
            case Y -> "#e1c877";
            case MID -> "#c1afe0";
            case A -> "#91bdd7";
            case B -> "#9dd2c4";
        };
    }

    /** Tinta didáctica de una red; MID no recibe un nivel inventado. */
    static String signalColor(Net net, int a, int b, Signal output) {
        if ((a != 0 && a != 1) || (b != 0 && b != 1)) {
            throw new IllegalArgumentException("Las entradas deben ser binarias");
        }
        return switch (net) {
            case A -> a == 1 ? "#a8e5f5" : "#688c9f";
            case B -> b == 1 ? "#a5e9cf" : "#638f82";
            case Y -> output == null ? "#a5b4b3" : switch (output) {
                case ONE -> "#f4dd76";
                case ZERO -> "#839995";
                case X -> "#e69a62";
                case Z -> "#b5b9c1";
            };
            case VDD, GND, MID -> color(net);
        };
    }

    private static Segment line(Net net, double x1, double y1, double x2, double y2) {
        return new Segment(net, new Point(x1, y1), new Point(x2, y2));
    }

    static final List<Segment> SEGMENTS = List.of(
            // Alimentación y ramas PMOS paralelas.
            line(Net.VDD, .12,.21, .88,.21),
            line(Net.VDD, .33,.21, .33,.30),
            line(Net.VDD, .67,.21, .67,.30),
            // Salida común: PMOS P1/P2 y entrada de N1.
            line(Net.Y, .33,.42, .33,.50),
            line(Net.Y, .67,.42, .67,.50),
            line(Net.Y, .33,.50, .88,.50),
            line(Net.Y, .33,.50, .33,.66),
            // Nodo intermedio de dos NMOS en serie: N1 drenador -> N2 fuente.
            line(Net.MID, .33,.78, .50,.78),
            line(Net.MID, .50,.78, .50,.62),
            line(Net.MID, .50,.62, .67,.62),
            line(Net.MID, .67,.62, .67,.66),
            line(Net.GND, .67,.78, .67,.90),
            line(Net.GND, .12,.90, .88,.90),
            // Compuertas A y B; cruzan Y sin punto eléctrico de unión.
            line(Net.A, .12,.36, .26,.36),
            line(Net.A, .19,.36, .19,.72),
            line(Net.A, .19,.72, .26,.72),
            line(Net.B, .74,.36, .88,.36),
            line(Net.B, .81,.36, .81,.72),
            line(Net.B, .74,.72, .81,.72)
    );
}
