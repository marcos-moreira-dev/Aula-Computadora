package dev.marcosmoreira.aula.interfaz;

import dev.marcosmoreira.aula.circuitos.Nand2Lesson;
import dev.marcosmoreira.aula.circuitos.Nand2Lesson.MosType;
import dev.marcosmoreira.aula.circuitos.Nand2Lesson.Net;
import dev.marcosmoreira.aula.circuitos.Nand2Lesson.Slot;
import javafx.scene.canvas.Canvas;
import javafx.scene.canvas.GraphicsContext;
import javafx.scene.control.ContextMenu;
import javafx.scene.control.MenuItem;
import javafx.scene.input.MouseButton;
import javafx.scene.input.TransferMode;
import javafx.scene.paint.Color;
import javafx.scene.text.Font;
import javafx.scene.text.FontWeight;

import java.util.function.BiConsumer;
import java.util.function.Consumer;
import java.util.function.Supplier;

/** Área de trabajo vectorial: los huecos y las piezas comparten los IDs del modelo. */
final class NandBoardView extends Canvas {
    private static final Color BG = Color.web("#e7ecea");
    private static final Color PCB = Color.web("#195344");
    private final Nand2Lesson lesson;
    private final Supplier<MosType> activePiece;
    private final Consumer<Slot> select;
    private final BiConsumer<Slot, MosType> drop;
    private final Consumer<Slot> inspect;
    private final Consumer<Slot> remove;
    private final CanvasNavigation navigation;
    private Slot selected;
    private Slot hover;
    private int inputA;
    private int inputB;

    NandBoardView(Nand2Lesson lesson, Supplier<MosType> activePiece,
                  Consumer<Slot> select, BiConsumer<Slot, MosType> drop,
                  Consumer<Slot> inspect, Consumer<Slot> remove) {
        this.lesson = lesson;
        this.activePiece = activePiece;
        this.select = select;
        this.drop = drop;
        this.inspect = inspect;
        this.remove = remove;
        navigation = new CanvasNavigation(this, this::render);
        widthProperty().addListener((o, oldValue, newValue) -> render());
        heightProperty().addListener((o, oldValue, newValue) -> render());
        setOnMouseMoved(e -> {
            Slot next = at(e.getX(), e.getY());
            if (next != hover) { hover = next; render(); }
        });
        setOnMouseExited(e -> { hover = null; render(); });
        setOnMouseClicked(e -> {
            if (navigation.suppressClick() || e.isShiftDown()) return;
            if (e.getButton() != MouseButton.PRIMARY) return;
            Slot slot = at(e.getX(), e.getY());
            if (slot == null) return;
            select.accept(slot);
            if (e.getClickCount() == 2) {
                inspect.accept(slot);
            } else if (lesson.pieceAt(slot) == null && activePiece.get() != null) {
                drop.accept(slot, activePiece.get());
            }
        });
        setOnContextMenuRequested(e -> {
            Slot slot = at(e.getX(), e.getY());
            if (slot == null) return;
            select.accept(slot);
            MenuItem detail = new MenuItem("Abrir detalle · " + slot);
            detail.setOnAction(action -> inspect.accept(slot));
            MenuItem takeOut = new MenuItem("Quitar pieza · " + slot);
            takeOut.setDisable(lesson.pieceAt(slot) == null);
            takeOut.setOnAction(action -> remove.accept(slot));
            new ContextMenu(detail, takeOut).show(this, e.getScreenX(), e.getScreenY());
            e.consume();
        });
        setOnDragOver(e -> {
            Slot slot = at(e.getX(), e.getY());
            if (slot != null && lesson.pieceAt(slot) == null
                    && e.getDragboard().hasString() && validType(e.getDragboard().getString())) {
                e.acceptTransferModes(TransferMode.COPY);
            }
            hover = slot;
            render();
            e.consume();
        });
        setOnDragDropped(e -> {
            Slot slot = at(e.getX(), e.getY());
            boolean accepted = false;
            if (slot != null && lesson.pieceAt(slot) == null
                    && e.getDragboard().hasString() && validType(e.getDragboard().getString())) {
                MosType type = MosType.valueOf(e.getDragboard().getString());
                if (lesson.remaining(type) > 0) {
                    drop.accept(slot, type);
                    accepted = true;
                }
            }
            e.setDropCompleted(accepted);
            e.consume();
        });
        setOnDragExited(e -> { hover = null; render(); });
    }

    private static boolean validType(String text) {
        return "PMOS".equals(text) || "NMOS".equals(text);
    }

    void setSelected(Slot slot) { selected = slot; }

    void setPreview(int a, int b) {
        inputA = a;
        inputB = b;
        render();
    }

    private double[] point(Slot slot) {
        double w = getWidth(), h = getHeight();
        BoardRouting.Point point = BoardRouting.slot(slot);
        return new double[]{w * (.075 + .85 * point.x()),
                h * (.11 + .79 * point.y())};
    }

    private Slot at(double x, double y) {
        x = navigation.worldX(x);
        y = navigation.worldY(y);
        double halfWidth = Math.min(67, getWidth() * 0.105);
        for (Slot slot : Slot.values()) {
            double[] p = point(slot);
            if (Math.abs(p[0] - x) <= halfWidth && Math.abs(p[1] - y) <= 43) return slot;
        }
        return null;
    }

    void render() {
        double w = getWidth(), h = getHeight();
        if (w <= 0 || h <= 0) return;
        GraphicsContext g = getGraphicsContext2D();
        g.setFill(BG);
        g.fillRect(0, 0, w, h);

        g.save();
        navigation.apply(g);

        double x0 = w * .075, y0 = h * .11, bw = w * .85, bh = h * .79;
        g.setFill(Color.web("#153d34"));
        g.fillRect(x0 + 2, y0 + 2, bw, bh);
        g.setFill(PCB);
        g.fillRect(x0, y0, bw, bh);
        g.setStroke(Color.web("#3a806f"));
        g.setLineWidth(2);
        g.strokeRect(x0 + 12, y0 + 12, bw - 24, bh - 24);

        // Orificios de sujeción de la placa conceptual, no huellas eléctricas.
        for (double xx : new double[]{x0 + 30, x0 + bw - 30}) {
            for (double yy : new double[]{y0 + 83, y0 + bh - 49}) {
                g.setFill(Color.web("#93b6a7"));
                g.fillOval(xx - 9, yy - 9, 18, 18);
                g.setFill(Color.web("#173f35"));
                g.fillOval(xx - 5, yy - 5, 10, 10);
            }
        }

        drawRouting(g, x0, y0, bw, bh);

        g.setFont(Font.font("Segoe UI", FontWeight.BOLD, 19));
        g.setFill(Color.web("#e3f0e7"));
        g.fillText("NAND2  ·  MOLDE DE MONTAJE", x0 + 25, y0 + 39);
        g.setFont(Font.font("Segoe UI", 12));
        g.setFill(Color.web("#b7d5cb"));
        g.fillText("Redes de un bit · trazado conceptual, no PCB fabricable", x0 + 25, y0 + 59);
        g.setFill(Color.web("#e3f0e7"));
        g.setFont(Font.font("Consolas", FontWeight.BOLD, 13));
        String outputText = lesson.readyToTest() ? switch (lesson.observe(inputA, inputB)) {
            case ZERO -> "0";
            case ONE -> "1";
            case X -> "X";
            case Z -> "Z";
        } : "—";
        g.fillText("A=" + inputA + "   B=" + inputB + "   Y=" + outputText,
                x0 + bw - 193, y0 + 83);

        for (Slot slot : Slot.values()) drawSocket(g, slot, w);
        g.setFill(Color.web("#dbece5"));
        g.setFont(Font.font("Segoe UI", 12));
        g.fillText("VDD / A / B / Y / MID / GND · redes compartidas con el modelo", x0 + 25, y0 + bh - 21);
        g.restore();
        g.setFill(Color.web("#4f615c"));
        g.fillText("Rueda: zoom  ·  Shift + arrastrar o botón central: paneo  ·  Doble clic: detalle", 20, h - 17);
    }

    void zoomBy(double factor) { navigation.zoomBy(factor); }

    void fit() { navigation.fit(); }

    int zoomPercent() { return navigation.zoomPercent(); }

    /** Trazos definidos una sola vez para las proyecciones 2D y 3D. */
    private void drawRouting(GraphicsContext g, double x, double y, double w, double h) {
        g.setLineWidth(3.5);
        Nand2Lesson.Signal output = lesson.readyToTest()
                ? lesson.observe(inputA, inputB) : null;
        for (BoardRouting.Segment segment : BoardRouting.SEGMENTS) {
            g.setStroke(Color.web(BoardRouting.signalColor(segment.net(), inputA, inputB, output)));
            double x1 = x + w * segment.a().x(), y1 = y + h * segment.a().y();
            double x2 = x + w * segment.b().x(), y2 = y + h * segment.b().y();
            g.strokeLine(x1, y1, x2, y2);
        }
        for (Net net : new Net[]{Net.VDD, Net.A, Net.B, Net.Y, Net.MID, Net.GND}) {
            double nx = switch (net) {
                case VDD, A, GND -> .10;
                case B, Y -> .89;
                case MID -> .49;
            };
            double ny = switch (net) {
                case VDD -> .21;
                case A, B -> .36;
                case Y -> .50;
                case MID -> .84;
                case GND -> .90;
            };
            g.setFont(Font.font("Consolas", FontWeight.BOLD, 12));
            g.setFill(Color.web("#eef6f0"));
            g.fillText(net.name(), x + w * nx, y + h * ny - 8);
        }
    }

    private void drawSocket(GraphicsContext g, Slot slot, double width) {
        double[] p = point(slot);
        double hw = Math.min(67, width * .105), x = p[0] - hw, y = p[1] - 37;
        MosType installed = lesson.pieceAt(slot);
        boolean active = hover == slot || selected == slot;
        // Contactos metálicos visibles alrededor del cuerpo. El taller usa
        // tres terminales eléctricos por MOS, no un DIP inventado de 8 pines.
        double sign = slot == Slot.P2 || slot == Slot.N2 ? 1 : -1;
        g.setFill(installed == null ? Color.web("#95bbae") : Color.web("#b9c8cf"));
        g.fillRect(p[0] - 6, y - 19, 12, 28);
        g.fillRect(p[0] - 6, y + 65, 12, 28);
        double gateX = sign < 0 ? x - 22 : x + 2 * hw - 7;
        g.fillRect(gateX, p[1] - 7, 29, 14);
        g.setLineWidth(active ? 3 : 1.5);
        if (installed == null) {
            g.setFill(Color.web("#d7e9df", .17));
            g.fillRect(x, y, 2 * hw, 74);
            g.setStroke(active ? Color.web("#ffd37c") : Color.web("#97c7b6"));
            g.setLineDashes(7, 5);
            g.strokeRect(x, y, 2 * hw, 74);
            g.setLineDashes();
        } else {
            g.setFill(Color.web("#26323a"));
            g.fillRect(x, y, 2 * hw, 74);
            g.setStroke(active ? Color.web("#ffd37c")
                    : installed != slot.expected() ? Color.web("#d4a454")
                    : lesson.isConducting(slot, inputA, inputB)
                    ? Color.web("#a1e4c5") : Color.web("#c9dbd6"));
            g.strokeRect(x, y, 2 * hw, 74);
        }
        g.setFont(Font.font("Consolas", FontWeight.BOLD, 19));
        g.setFill(installed == null ? Color.web("#deede3") : Color.WHITE);
        g.fillText(slot.name(), p[0] - 14, p[1] - 8);
        g.setFont(Font.font("Segoe UI", 12));
        g.setFill(installed == null ? Color.web("#beddd0") : Color.web("#d7e4e8"));
        String type = installed == null ? slot.expected() + " · vacío" : installed.toString();
        g.fillText(type, p[0] - hw + 16, p[1] + 16);
        // Orientación ilustrativa, no huella ni patillaje comercial.
    }
}
