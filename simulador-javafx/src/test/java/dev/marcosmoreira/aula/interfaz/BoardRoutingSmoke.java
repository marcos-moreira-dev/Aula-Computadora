package dev.marcosmoreira.aula.interfaz;

import dev.marcosmoreira.aula.circuitos.Nand2Lesson.Net;
import dev.marcosmoreira.aula.circuitos.Nand2Lesson.Signal;

import java.util.EnumSet;

/** Pruebas geométricas de rutas y tintas sin JavaFX ni Maven. */
public final class BoardRoutingSmoke {
    private BoardRoutingSmoke() { }

    public static void main(String[] args) {
        int checks = 0;
        EnumSet<Net> nets = EnumSet.noneOf(Net.class);
        for (BoardRouting.Segment segment : BoardRouting.SEGMENTS) {
            nets.add(segment.net());
            require(segment.a().x() == segment.b().x()
                    || segment.a().y() == segment.b().y(), "Ruta diagonal");
            checks++;
        }
        require(nets.equals(EnumSet.allOf(Net.class)), "Falta una red"); checks++;
        require(!BoardRouting.signalColor(Net.Y, 0, 0, Signal.ONE).equals(
                BoardRouting.signalColor(Net.Y, 1, 1, Signal.ZERO)), "Y no distingue 0/1"); checks++;
        require(!BoardRouting.signalColor(Net.A, 0, 1, Signal.ONE).equals(
                BoardRouting.signalColor(Net.A, 1, 1, Signal.ONE)), "A no cambia"); checks++;
        require(!BoardRouting.signalColor(Net.B, 1, 0, Signal.ZERO).equals(
                BoardRouting.signalColor(Net.B, 1, 1, Signal.ZERO)), "B no cambia"); checks++;
        require(BoardRouting.signalColor(Net.MID, 0, 0, null).equals(
                BoardRouting.signalColor(Net.MID, 1, 1, Signal.ONE)),
                "MID no tiene nivel computado"); checks++;
        System.out.println("OK: " + checks + " controles de rutas/tintas (sin JavaFX)");
    }

    private static void require(boolean ok, String message) {
        if (!ok) throw new AssertionError(message);
    }
}
