package dev.marcosmoreira.aula.interfaz;

import dev.marcosmoreira.aula.circuitos.Nand2Lesson;
import dev.marcosmoreira.aula.circuitos.Nand2Lesson.MosType;
import dev.marcosmoreira.aula.circuitos.Nand2Lesson.Slot;
import javafx.scene.canvas.Canvas;
import javafx.scene.canvas.GraphicsContext;
import javafx.scene.paint.Color;
import javafx.scene.text.Font;
import javafx.scene.text.FontWeight;
import javafx.scene.text.TextAlignment;

/**
 * Corte conceptual del módulo NAND2: el propio cuerpo del chip delimita el
 * esquema, y las cinco redes externas se conducen desde sus terminales.
 * No representa una distribución de silicio ni un pinout comercial.
 */
final class NandLogicView extends Canvas {
    private static final Color SIGNAL = Color.web("#344e62");
    private static final Color GATE = Color.web("#356d8a");
    private final Nand2Lesson lesson;
    private final CanvasNavigation navigation;
    private Slot selected;
    private int inputA;
    private int inputB;
    private boolean previewEnabled;

    NandLogicView(Nand2Lesson lesson) {
        this.lesson = lesson;
        navigation = new CanvasNavigation(this, this::render);
        widthProperty().addListener((o, oldValue, newValue) -> render());
        heightProperty().addListener((o, oldValue, newValue) -> render());
    }

    void setSelected(Slot slot) { selected = slot; }
    void setPreview(int a, int b, boolean enabled) {
        inputA = a;
        inputB = b;
        previewEnabled = enabled;
        render();
    }
    void zoomBy(double factor) { navigation.zoomBy(factor); }
    void fit() { navigation.fit(); }
    int zoomPercent() { return navigation.zoomPercent(); }

    void render() {
        double w = getWidth(), h = getHeight();
        if (w <= 0 || h <= 0) return;
        GraphicsContext g = getGraphicsContext2D();
        g.setFill(Color.web("#e8ecef"));
        g.fillRect(0, 0, w, h);
        g.save();
        navigation.apply(g);

        double x = Math.max(83, w * .10), top = 83;
        double cw = w - 2 * x, ch = h - 168;
        if (ch < 260) ch = 260;

        label(g, "NAND DE DOS ENTRADAS  /  INTERIOR", x, 44,
                Color.web("#314d61"), 18, true);
        if (previewEnabled) {
            String yValue = switch (lesson.observe(inputA, inputB)) {
                case ZERO -> "0";
                case ONE -> "1";
                case X -> "X";
                case Z -> "Z";
            };
            label(g, "A=" + inputA + "   B=" + inputB + "   Y=" + yValue,
                    x + 10, 67, Color.web("#2e6b57"), 13, true);
        }
        // 6 terminales por lado, a modo de cucarachita esquemática; solo 5
        // redes con identidad técnica conocida. Los demás no reciben pinout.
        g.setFill(Color.web("#242a30"));
        g.fillRect(x - 5, top - 5, cw + 10, ch + 10);
        g.setFill(Color.WHITE);
        g.fillRect(x + 2, top + 2, cw - 4, ch - 4);
        g.setStroke(Color.web("#808a90"));
        g.setLineWidth(1);
        g.strokeRect(x + 11, top + 11, cw - 22, ch - 22);

        double[] rows = new double[6];
        for (int i = 0; i < rows.length; i++) {
            rows[i] = top + (i + 1) * ch / 7;
            contact(g, x, rows[i], false, i == 0 || i == 1 || i == 5);
            contact(g, x + cw, rows[i], true, i == 1 || i == 3);
        }

        double vddY = rows[0], aY = rows[1], bY = rows[1];
        double yY = rows[3], groundY = rows[5];
        double pY = top + ch * .29;
        double n1Y = top + ch * .61;
        double n2Y = top + ch * .755;
        double xp1 = x + cw * .47, xp2 = x + cw * .70;
        double xn = x + cw * .585;
        double laneA = x + cw * .175, laneB = x + cw * .85;
        double outputJunction = top + ch * .48;

        // Cables de alimentación, salida y cadena de NMOS. P1/P2 hacen
        // pull-up paralelo; N1 y N2, pull-down serie. Cada conexión usa una
        // red con identidad independiente de la geometría del lienzo.
        wire(g, SIGNAL, x, vddY, xp2, vddY);
        wire(g, SIGNAL, xp1, vddY, xp1, pY - 23);
        wire(g, SIGNAL, xp2, vddY, xp2, pY - 23);
        wire(g, SIGNAL, xp1, pY + 23, xp1, outputJunction);
        wire(g, SIGNAL, xp2, pY + 23, xp2, outputJunction);
        wire(g, SIGNAL, xp1, outputJunction, x + cw - 30, outputJunction);
        wire(g, SIGNAL, x + cw - 30, outputJunction, x + cw - 30, yY);
        wire(g, SIGNAL, x + cw - 30, yY, x + cw, yY);
        wire(g, SIGNAL, xn, outputJunction, xn, n1Y - 23);
        wire(g, SIGNAL, xn, n1Y + 23, xn, n2Y - 23);
        wire(g, SIGNAL, xn, n2Y + 23, xn, groundY);
        wire(g, SIGNAL, x, groundY, xn, groundY);

        // Entrada A alimenta las compuertas de P1 y N1 desde el pin izquierdo.
        wire(g, GATE, x, aY, laneA, aY);
        wire(g, GATE, laneA, aY, laneA, n1Y);
        wire(g, GATE, laneA, pY, xp1 - 32, pY);
        wire(g, GATE, laneA, n1Y, xn - 32, n1Y);

        // B llega desde el pin derecho a las compuertas de P2 y N2. En
        // los cruces de líneas de distinta red NO hay punto de unión.
        wire(g, GATE, x + cw, bY, laneB, bY);
        wire(g, GATE, laneB, pY, laneB, outputJunction - 8);
        wire(g, GATE, laneB, outputJunction + 8, laneB, n2Y);
        wire(g, GATE, xp2 + 32, pY, laneB, pY);
        wire(g, GATE, xn + 32, n2Y, laneB, n2Y);

        // Dibujamos los dispositivos sobre sus caminos conductores. No se
        // presupone una geometría de transistor en silicio real.
        component(g, Slot.P1, xp1, pY);
        component(g, Slot.P2, xp2, pY);
        component(g, Slot.N1, xn, n1Y);
        component(g, Slot.N2, xn, n2Y);

        junction(g, xp1, vddY); junction(g, xp2, vddY);
        junction(g, xp1, outputJunction); junction(g, xp2, outputJunction);
        junction(g, xn, outputJunction);

        outsideLabel(g, "VDD", x - 37, vddY + 5, false);
        outsideLabel(g, "A", x - 37, aY + 5, false);
        outsideLabel(g, "B", x + cw + 36, bY + 5, true);
        outsideLabel(g, "Y", x + cw + 36, yY + 5, true);
        outsideLabel(g, "GND", x - 37, groundY + 5, false);
        label(g, "CMOS  ·  representación funcional ideal", x + 27, top + ch - 22,
                Color.web("#7b838a"), 12, false);
        g.restore();

        label(g, "Rueda: zoom  ·  Shift + arrastrar: paneo  ·  Escala y pinout no físicos",
                15, h - 14, Color.web("#5d717d"), 12, false);
    }

    private static void contact(GraphicsContext g, double x, double y,
                                boolean right, boolean used) {
        double xx = right ? x : x - 25;
        g.setFill(used ? Color.web("#a4b1bc") : Color.web("#c8d0d6"));
        g.fillRect(xx, y - 6, 25, 12);
        g.setStroke(Color.web("#5c6c79"));
        g.setLineWidth(1);
        g.strokeRect(xx, y - 6, 25, 12);
    }

    private void component(GraphicsContext g, Slot slot, double x, double y) {
        MosType actual = lesson.pieceAt(slot);
        boolean matches = actual == slot.expected();
        boolean isPmos = (actual == null ? slot.expected() : actual) == MosType.PMOS;
        boolean gateFromRight = slot == Slot.P2 || slot == Slot.N2;

        // El símbolo MOS sustituye a los antiguos rectángulos con microcopy.
        // La caja tenue representa un alojamiento y permite señalar la selección.
        Color housing = Color.web("#f7fafb");
        if (actual != null && !matches) {
            housing = Color.web("#fff0d6");
        } else if (actual != null && previewEnabled) {
            housing = lesson.isConducting(slot, inputA, inputB)
                    ? Color.web("#c4e9d1") : Color.web("#e5eaee");
        } else if (actual != null) {
            housing = Color.web("#e4f1ea");
        }
        g.setFill(housing);
        g.fillRect(x - 31, y - 22, 62, 44);
        g.setStroke(selected == slot ? Color.web("#c38a2e") : Color.web("#c2cdd2"));
        g.setLineWidth(selected == slot ? 2.7 : 1.1);
        g.setLineDashes(actual == null ? new double[]{4, 3} : new double[]{});
        g.strokeRect(x - 31, y - 22, 62, 44);
        g.setLineDashes();

        Color symbol = actual == null ? Color.web("#7b929d") : Color.web("#233d4d");
        g.setStroke(symbol);
        g.setLineWidth(2.2);
        // Fuente/drenador, canal y terminal de compuerta; solo topología ideal.
        g.strokeLine(x, y - 22, x, y - 14);
        g.strokeLine(x - 9, y - 14, x + 9, y - 14);
        g.strokeLine(x, y - 14, x, y + 14);
        g.strokeLine(x - 9, y + 14, x + 9, y + 14);
        g.strokeLine(x, y + 14, x, y + 22);
        double sign = gateFromRight ? 1 : -1;
        double gateX = x + sign * 13;
        g.strokeLine(gateX, y - 12, gateX, y + 12);
        g.strokeLine(x + sign * 31, y, x + sign * (isPmos ? 21 : 13), y);
        if (isPmos) {
            g.setFill(Color.WHITE);
            g.fillOval(x + sign * 21 - 3.4, y - 3.4, 6.8, 6.8);
            g.strokeOval(x + sign * 21 - 3.4, y - 3.4, 6.8, 6.8);
            g.strokeLine(x + sign * 17.6, y, gateX, y);
        }
        // Identificador breve de cada transistor, no una leyenda dentro del símbolo.
        label(g, slot.toString(), x + (gateFromRight ? -27 : 16), y - 6,
                Color.web("#385565"), 10, true);
    }

    private static void wire(GraphicsContext g, Color color,
                             double x1, double y1, double x2, double y2) {
        g.setStroke(color);
        g.setLineWidth(2);
        g.strokeLine(x1, y1, x2, y2);
    }

    private static void junction(GraphicsContext g, double x, double y) {
        g.setFill(SIGNAL);
        g.fillOval(x - 3.2, y - 3.2, 6.4, 6.4);
    }

    private static void outsideLabel(GraphicsContext g, String text,
                                     double x, double y, boolean right) {
        g.setTextAlign(right ? TextAlignment.LEFT : TextAlignment.RIGHT);
        label(g, text, x, y, Color.web("#294a62"), 13, true);
        g.setTextAlign(TextAlignment.LEFT);
    }

    private static void label(GraphicsContext g, String text, double x, double y,
                              Color color, int size, boolean bold) {
        g.setFill(color);
        g.setFont(Font.font("Segoe UI", bold ? FontWeight.BOLD : FontWeight.NORMAL, size));
        g.fillText(text, x, y);
    }
}
