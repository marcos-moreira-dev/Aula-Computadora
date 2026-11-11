package dev.marcosmoreira.aula.circuitos;

import java.util.ArrayList;
import java.util.EnumMap;
import java.util.List;
import java.util.Map;
import java.util.Objects;

/**
 * Un único estado de montaje para las vistas de placa y de esquema.
 * La topología P1/P2 paralelos y N1/N2 en serie procede del recurso C28-AC.
 * No modela tensiones, pines físicos, retardo ni semiconductores analógicos.
 */
public final class Nand2Lesson {

    public enum MosType { PMOS, NMOS }

    /** Redes del único módulo NAND2 ideal, compartidas por vistas y modelo. */
    public enum Net { VDD, A, B, Y, MID, GND }

    /** Contactos geométricos del molde, sin patillaje comercial. */
    public enum Terminal { GATE, UPPER, LOWER }

    public record TerminalRef(Slot slot, Terminal terminal) {
        public TerminalRef {
            Objects.requireNonNull(slot);
            Objects.requireNonNull(terminal);
        }
        public Net net() { return slot.netFor(terminal); }
    }

    public enum Slot {
        P1(MosType.PMOS, 'A', Net.VDD, Net.Y),
        P2(MosType.PMOS, 'B', Net.VDD, Net.Y),
        N1(MosType.NMOS, 'A', Net.Y, Net.MID),
        N2(MosType.NMOS, 'B', Net.MID, Net.GND);

        private final MosType expected;
        private final char gate;
        private final Net sourceNet;
        private final Net drainNet;

        Slot(MosType expected, char gate, Net sourceNet, Net drainNet) {
            this.expected = expected;
            this.gate = gate;
            this.sourceNet = sourceNet;
            this.drainNet = drainNet;
        }

        public MosType expected() { return expected; }
        public char gate() { return gate; }
        public Net sourceNet() { return sourceNet; }
        public Net drainNet() { return drainNet; }
        public String nets() { return sourceNet + "-" + drainNet; }
        /** UPPER/LOWER son contactos en la vista, no pines físicos. */
        public Net netFor(Terminal terminal) {
            Objects.requireNonNull(terminal);
            return switch (terminal) {
                case GATE -> gate == 'A' ? Net.A : Net.B;
                case UPPER -> sourceNet;
                case LOWER -> drainNet;
            };
        }
    }

    public enum Signal { ZERO, ONE, X, Z }

    public record TruthRow(int a, int b, int expected, Signal observed) {
        public boolean passes() {
            return (expected == 0 && observed == Signal.ZERO)
                    || (expected == 1 && observed == Signal.ONE);
        }
    }

    private final EnumMap<Slot, MosType> placed = new EnumMap<>(Slot.class);

    public boolean place(Slot slot, MosType type) {
        Objects.requireNonNull(slot);
        Objects.requireNonNull(type);
        if (placed.containsKey(slot) || remaining(type) == 0) {
            return false;
        }
        // Un encaje geométricamente admitido NO implica un montaje correcto.
        placed.put(slot, type);
        return true;
    }

    public boolean remove(Slot slot) {
        return placed.remove(Objects.requireNonNull(slot)) != null;
    }

    public MosType pieceAt(Slot slot) {
        return placed.get(Objects.requireNonNull(slot));
    }

    public int remaining(MosType type) {
        int installed = (int) placed.values().stream().filter(type::equals).count();
        return 2 - installed;
    }

    public int placedCount() { return placed.size(); }

    public boolean readyToTest() { return placed.size() == Slot.values().length; }

    public Map<Slot, MosType> snapshot() { return Map.copyOf(placed); }

    public void restore(Map<Slot, MosType> snapshot) {
        Objects.requireNonNull(snapshot);
        Nand2Lesson candidate = new Nand2Lesson();
        for (Slot slot : Slot.values()) {
            MosType type = snapshot.get(slot);
            if (type != null && !candidate.place(slot, type)) {
                throw new IllegalArgumentException("Inventario incompatible en " + slot);
            }
        }
        if (candidate.placedCount() != snapshot.size()) {
            throw new IllegalArgumentException("Hay posiciones no reconocidas");
        }
        placed.clear();
        placed.putAll(candidate.placed);
    }

    public List<TruthRow> testTruthTable() {
        if (!readyToTest()) {
            throw new IllegalStateException("Faltan componentes; no puede probarse el montaje");
        }
        List<TruthRow> rows = new ArrayList<>();
        for (int a = 0; a <= 1; a++) {
            for (int b = 0; b <= 1; b++) {
                rows.add(new TruthRow(a, b, 1 - (a & b), observe(a, b)));
            }
        }
        return List.copyOf(rows);
    }

    /** Salida observable para dos entradas binarias y montaje completo. */
    public Signal observe(int a, int b) {
        requireBit(a);
        requireBit(b);
        if (!readyToTest()) {
            throw new IllegalStateException("La salida requiere montar las cuatro piezas");
        }
        return evaluate(a, b);
    }

    /** Verdadero si el MOS instalado conduce idealmente con las entradas. */
    public boolean isConducting(Slot slot, int a, int b) {
        Objects.requireNonNull(slot);
        requireBit(a);
        requireBit(b);
        return conducts(slot, slot.gate() == 'A' ? a : b);
    }

    private static void requireBit(int bit) {
        if (bit != 0 && bit != 1) {
            throw new IllegalArgumentException("La entrada digital debe ser 0 o 1: " + bit);
        }
    }

    private Signal evaluate(int a, int b) {
        // Conducción ideal: PMOS activo con puerta 0, NMOS activo con 1.
        // P1/P2 hacen pull-up EN PARALELO; N1/N2 pull-down EN SERIE.
        boolean pullUp = conducts(Slot.P1, a) || conducts(Slot.P2, b);
        boolean pullDown = conducts(Slot.N1, a) && conducts(Slot.N2, b);
        if (pullUp && pullDown) return Signal.X; // contención en modelo lógico
        if (pullUp) return Signal.ONE;
        if (pullDown) return Signal.ZERO;
        return Signal.Z; // ninguna ruta conductora (nodo flotante)
    }

    private boolean conducts(Slot slot, int value) {
        MosType type = placed.get(slot);
        return type == MosType.PMOS && value == 0
                || type == MosType.NMOS && value == 1;
    }
}
