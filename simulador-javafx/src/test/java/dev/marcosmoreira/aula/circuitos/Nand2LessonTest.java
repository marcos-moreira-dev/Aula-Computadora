package dev.marcosmoreira.aula.circuitos;

import org.junit.jupiter.api.Test;
import java.util.Map;

import static dev.marcosmoreira.aula.circuitos.Nand2Lesson.MosType.NMOS;
import static dev.marcosmoreira.aula.circuitos.Nand2Lesson.MosType.PMOS;
import static dev.marcosmoreira.aula.circuitos.Nand2Lesson.Slot.*;
import static org.junit.jupiter.api.Assertions.*;

class Nand2LessonTest {
    @Test
    void startsWithFourGhostSlotsAndLimitedKit() {
        Nand2Lesson lesson = new Nand2Lesson();
        assertEquals(0, lesson.placedCount());
        assertEquals(2, lesson.remaining(PMOS));
        assertEquals(2, lesson.remaining(NMOS));
        assertFalse(lesson.readyToTest());
        assertThrows(IllegalStateException.class, lesson::testTruthTable);
    }

    @Test
    void correctCircuitPassesAllFourVectors() {
        Nand2Lesson lesson = correctCircuit();
        assertEquals(4, lesson.placedCount());
        assertEquals(0, lesson.remaining(PMOS));
        assertEquals(0, lesson.remaining(NMOS));
        assertEquals(4, lesson.testTruthTable().size());
        assertTrue(lesson.testTruthTable().stream().allMatch(Nand2Lesson.TruthRow::passes));
        assertEquals(java.util.List.of(
                Nand2Lesson.Signal.ONE, Nand2Lesson.Signal.ONE,
                Nand2Lesson.Signal.ONE, Nand2Lesson.Signal.ZERO),
                lesson.testTruthTable().stream().map(Nand2Lesson.TruthRow::observed).toList());
        assertEquals(Nand2Lesson.Signal.ONE, lesson.testTruthTable().get(0).observed());
        assertEquals(Nand2Lesson.Signal.ZERO, lesson.testTruthTable().get(3).observed());
    }

    @Test
    void wrongTypeCanSnapButProducesAnObservableDiscrepancy() {
        Nand2Lesson lesson = new Nand2Lesson();
        assertTrue(lesson.place(P1, NMOS));
        assertTrue(lesson.place(P2, PMOS));
        assertTrue(lesson.place(N1, PMOS));
        assertTrue(lesson.place(N2, NMOS));
        assertTrue(lesson.readyToTest());
        assertTrue(lesson.testTruthTable().stream().anyMatch(row -> !row.passes()));
        assertEquals(Nand2Lesson.Signal.ZERO, lesson.testTruthTable().get(1).observed());
    }

    @Test
    void cannotReusePieceOrOverwriteOccupiedSlot() {
        Nand2Lesson lesson = new Nand2Lesson();
        assertTrue(lesson.place(P1, PMOS));
        assertFalse(lesson.place(P1, NMOS));
        assertTrue(lesson.place(P2, PMOS));
        assertFalse(lesson.place(N1, PMOS));
        assertEquals(2, lesson.placedCount());
        assertTrue(lesson.remove(P1));
        assertEquals(1, lesson.remaining(PMOS));
    }

    @Test
    void invalidBoardsCanBeFloatingOrInContention() {
        Nand2Lesson floating = new Nand2Lesson();
        floating.place(P1, NMOS);
        floating.place(P2, PMOS);
        floating.place(N1, NMOS);
        floating.place(N2, PMOS);
        assertEquals(Nand2Lesson.Signal.Z, floating.testTruthTable().get(1).observed());

        Nand2Lesson contention = new Nand2Lesson();
        contention.place(P1, PMOS);
        contention.place(P2, NMOS);
        contention.place(N1, PMOS);
        contention.place(N2, NMOS);
        assertEquals(Nand2Lesson.Signal.X, contention.testTruthTable().get(1).observed());
    }

    @Test
    void snapshotDoesNotLeakMutableStateAndRestoreRejectsExtraInventory() {
        Nand2Lesson lesson = correctCircuit();
        Map<Nand2Lesson.Slot, Nand2Lesson.MosType> snapshot = lesson.snapshot();
        assertThrows(UnsupportedOperationException.class, () -> snapshot.clear());
        lesson.remove(P1);
        lesson.restore(snapshot);
        assertEquals(4, lesson.placedCount());
        assertThrows(IllegalArgumentException.class, () -> lesson.restore(Map.of(
                P1, PMOS, P2, PMOS, N1, PMOS)));
        assertEquals(4, lesson.placedCount());
    }

    @Test
    void liveOutputUsesTheSameSourceAsTheFourVectorTable() {
        Nand2Lesson lesson = correctCircuit();
        for (Nand2Lesson.TruthRow row : lesson.testTruthTable()) {
            assertEquals(row.observed(), lesson.observe(row.a(), row.b()));
        }
        assertTrue(lesson.isConducting(P1, 0, 0));
        assertTrue(lesson.isConducting(P2, 0, 0));
        assertFalse(lesson.isConducting(N1, 0, 0));
        assertFalse(lesson.isConducting(N2, 0, 0));
        assertFalse(lesson.isConducting(P1, 1, 1));
        assertTrue(lesson.isConducting(N1, 1, 1));
        assertTrue(lesson.isConducting(N2, 1, 1));
    }

    @Test
    void liveOutputRequiresACompleteBoardAndBinaryInputs() {
        Nand2Lesson lesson = new Nand2Lesson();
        assertThrows(IllegalStateException.class, () -> lesson.observe(0, 0));
        assertThrows(IllegalArgumentException.class, () -> lesson.observe(-1, 0));
        assertThrows(IllegalArgumentException.class, () -> lesson.observe(0, 2));
        assertThrows(IllegalArgumentException.class, () -> lesson.isConducting(P1, 1, 3));
    }

    static Nand2Lesson correctCircuit() {
        Nand2Lesson lesson = new Nand2Lesson();
        lesson.place(P1, PMOS);
        lesson.place(P2, PMOS);
        lesson.place(N1, NMOS);
        lesson.place(N2, NMOS);
        return lesson;
    }
}
