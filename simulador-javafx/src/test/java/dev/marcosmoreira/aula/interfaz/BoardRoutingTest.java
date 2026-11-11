package dev.marcosmoreira.aula.interfaz;

import dev.marcosmoreira.aula.circuitos.Nand2Lesson.Net;
import dev.marcosmoreira.aula.circuitos.Nand2Lesson.Signal;
import dev.marcosmoreira.aula.circuitos.Nand2Lesson.Slot;
import org.junit.jupiter.api.Test;

import java.util.EnumSet;
import java.util.stream.Collectors;

import static org.junit.jupiter.api.Assertions.*;

/** La misma ruta de conexión se usa al dibujar la placa 2D y la 3D. */
class BoardRoutingTest {
    @Test
    void sixNamedNetsHaveOrthogonalBoardSegments() {
        assertEquals(19, BoardRouting.SEGMENTS.size());
        assertEquals(EnumSet.allOf(Net.class), BoardRouting.SEGMENTS.stream()
                .map(BoardRouting.Segment::net).collect(Collectors.toSet()));
        for (BoardRouting.Segment segment : BoardRouting.SEGMENTS) {
            assertTrue(segment.a().x() == segment.b().x()
                    || segment.a().y() == segment.b().y());
            for (BoardRouting.Point point : new BoardRouting.Point[]{segment.a(), segment.b()}) {
                assertTrue(point.x() >= 0 && point.x() <= 1);
                assertTrue(point.y() >= 0 && point.y() <= 1);
            }
        }
    }

    @Test
    void fourPhysicalSlotsRemainStableAndDistinct() {
        assertEquals(4, java.util.Arrays.stream(Slot.values())
                .map(BoardRouting::slot).distinct().count());
        assertEquals(BoardRouting.slot(Slot.P1).x(), BoardRouting.slot(Slot.N1).x());
        assertEquals(BoardRouting.slot(Slot.P2).x(), BoardRouting.slot(Slot.N2).x());
        assertTrue(BoardRouting.slot(Slot.P1).y() < BoardRouting.slot(Slot.N1).y());
        for (Net net : Net.values()) assertNotNull(BoardRouting.color(net));
    }

    @Test
    void liveSignalColorsOnlyFollowKnownDigitalLevels() {
        assertNotEquals(BoardRouting.signalColor(Net.A, 0, 0, Signal.ONE),
                BoardRouting.signalColor(Net.A, 1, 0, Signal.ONE));
        assertNotEquals(BoardRouting.signalColor(Net.B, 0, 0, Signal.ONE),
                BoardRouting.signalColor(Net.B, 0, 1, Signal.ONE));
        assertNotEquals(BoardRouting.signalColor(Net.Y, 0, 0, Signal.ONE),
                BoardRouting.signalColor(Net.Y, 0, 0, Signal.ZERO));
        assertNotEquals(BoardRouting.signalColor(Net.Y, 0, 0, Signal.X),
                BoardRouting.signalColor(Net.Y, 0, 0, Signal.Z));
        assertEquals(BoardRouting.color(Net.MID),
                BoardRouting.signalColor(Net.MID, 1, 1, Signal.ZERO));
        assertEquals(BoardRouting.signalColor(Net.Y, 0, 0, null),
                BoardRouting.signalColor(Net.Y, 1, 1, null));
        assertThrows(IllegalArgumentException.class,
                () -> BoardRouting.signalColor(Net.A, 2, 0, Signal.ONE));
    }
}
