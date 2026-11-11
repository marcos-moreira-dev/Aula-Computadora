package dev.marcosmoreira.aula.interfaz;

import dev.marcosmoreira.aula.circuitos.Nand2Lesson;
import dev.marcosmoreira.aula.circuitos.Nand2Lesson.MosType;
import dev.marcosmoreira.aula.circuitos.Nand2Lesson.Net;
import dev.marcosmoreira.aula.circuitos.Nand2Lesson.Slot;
import dev.marcosmoreira.aula.circuitos.Nand2Lesson.Terminal;
import dev.marcosmoreira.aula.circuitos.Nand2Lesson.TerminalRef;
import javafx.geometry.Pos;
import javafx.scene.AmbientLight;
import javafx.scene.Group;
import javafx.scene.Node;
import javafx.scene.PerspectiveCamera;
import javafx.scene.PointLight;
import javafx.scene.SceneAntialiasing;
import javafx.scene.SubScene;
import javafx.scene.control.ContextMenu;
import javafx.scene.control.Label;
import javafx.scene.control.MenuItem;
import javafx.scene.input.MouseButton;
import javafx.scene.input.TransferMode;
import javafx.scene.layout.StackPane;
import javafx.scene.paint.Color;
import javafx.scene.paint.PhongMaterial;
import javafx.scene.shape.Box;
import javafx.scene.text.Font;
import javafx.scene.text.FontWeight;
import javafx.scene.text.Text;
import javafx.scene.transform.Affine;
import javafx.scene.transform.Rotate;

import java.util.function.BiConsumer;
import java.util.function.Consumer;
import java.util.function.Supplier;

/**
 * Placa 3D conceptual y manipulable. Las piezas, posiciones y cantidades
 * proceden de Nand2Lesson; la geometría no es una huella manufacturable.
 */
final class NandBoard3DView extends StackPane {
    private final Nand2Lesson lesson;
    private final Supplier<MosType> activePiece;
    private final Consumer<Slot> select;
    private final Consumer<Net> selectNet;
    private final Consumer<TerminalRef> selectTerminal;
    private final BiConsumer<Slot, MosType> drop;
    private final Consumer<Slot> inspect;
    private final Consumer<Slot> remove;
    private final Group boardGroup = new Group();
    private final SubScene subscene;
    private final PerspectiveCamera camera = new PerspectiveCamera(true);
    private final Rotate pitch = new Rotate(-43, Rotate.X_AXIS);
    private final Rotate yaw = new Rotate(-22, Rotate.Y_AXIS);
    private final Label liveSignals = new Label();
    private Slot selected;
    private Net selectedNet;
    private TerminalRef selectedTerminal;
    private int inputA;
    private int inputB;
    private double distance = 970;
    private double mouseX, mouseY;
    private boolean orbiting, panning;
    private boolean gestureMoved;

    NandBoard3DView(Nand2Lesson lesson, Supplier<MosType> activePiece,
                    Consumer<Slot> select, BiConsumer<Slot, MosType> drop,
                    Consumer<Slot> inspect, Consumer<Slot> remove,
                    Consumer<Net> selectNet,
                    Consumer<TerminalRef> selectTerminal) {
        this.lesson = lesson;
        this.activePiece = activePiece;
        this.select = select;
        this.selectNet = selectNet;
        this.selectTerminal = selectTerminal;
        this.drop = drop;
        this.inspect = inspect;
        this.remove = remove;

        boardGroup.getTransforms().addAll(yaw, pitch);
        Group world = new Group(boardGroup);
        world.getChildren().add(new AmbientLight(Color.web("#dce9e7")));
        PointLight light = new PointLight(Color.web("#f9fbff"));
        light.setTranslateX(-320);
        light.setTranslateY(-500);
        light.setTranslateZ(-550);
        world.getChildren().add(light);

        camera.setNearClip(1);
        camera.setFarClip(5000);
        camera.setTranslateZ(-distance);
        subscene = new SubScene(world, 800, 510, true, SceneAntialiasing.BALANCED);
        subscene.setFill(Color.web("#e8ecef"));
        subscene.setCamera(camera);
        subscene.widthProperty().bind(widthProperty());
        subscene.heightProperty().bind(heightProperty());
        getChildren().add(subscene);

        Label title = new Label("PLACA 3D  ·  VISTA CONCEPTUAL");
        title.getStyleClass().add("view-3d-title");
        title.setMouseTransparent(true);
        StackPane.setAlignment(title, Pos.TOP_LEFT);
        Label help = new Label("Clic en pista: sonda  ·  Arrastrar fondo: orbitar  ·  Shift: paneo  ·  Rueda: zoom");
        help.getStyleClass().add("view-3d-help");
        help.setMouseTransparent(true);
        StackPane.setAlignment(help, Pos.BOTTOM_LEFT);
        liveSignals.getStyleClass().add("view-3d-signals");
        liveSignals.setMouseTransparent(true);
        StackPane.setAlignment(liveSignals, Pos.TOP_RIGHT);
        getChildren().addAll(title, help, liveSignals);

        subscene.setOnMousePressed(e -> {
            mouseX = e.getSceneX();
            mouseY = e.getSceneY();
            gestureMoved = false;
            Slot hit = pickedSlot(e.getPickResult().getIntersectedNode());
            Net hitNet = pickedNet(e.getPickResult().getIntersectedNode());
            TerminalRef hitTerminal = pickedTerminal(e.getPickResult().getIntersectedNode());
            panning = e.getButton() == MouseButton.MIDDLE || e.isShiftDown();
            orbiting = e.getButton() == MouseButton.PRIMARY && hit == null
                    && hitNet == null && hitTerminal == null && !panning;
        });
        subscene.setOnMouseDragged(e -> {
            double dx = e.getSceneX() - mouseX;
            double dy = e.getSceneY() - mouseY;
            mouseX = e.getSceneX();
            mouseY = e.getSceneY();
            if (Math.abs(dx) + Math.abs(dy) > 1) gestureMoved = true;
            if (orbiting) {
                yaw.setAngle(yaw.getAngle() + dx * .45);
                pitch.setAngle(Math.max(-82, Math.min(-8, pitch.getAngle() - dy * .4)));
                e.consume();
            } else if (panning) {
                boardGroup.setTranslateX(boardGroup.getTranslateX() + dx);
                boardGroup.setTranslateY(boardGroup.getTranslateY() + dy);
                e.consume();
            }
        });
        subscene.setOnMouseReleased(e -> { orbiting = false; panning = false; });
        subscene.setOnScroll(e -> {
            zoomBy(e.getDeltaY() >= 0 ? 1.12 : 1 / 1.12);
            e.consume();
        });
        subscene.setOnDragOver(e -> {
            Slot slot = pickedSlot(e.getPickResult().getIntersectedNode());
            if (slot != null && lesson.pieceAt(slot) == null
                    && e.getDragboard().hasString() && known(e.getDragboard().getString())) {
                MosType kind = MosType.valueOf(e.getDragboard().getString());
                if (lesson.remaining(kind) > 0) e.acceptTransferModes(TransferMode.COPY);
            }
            e.consume();
        });
        subscene.setOnDragDropped(e -> {
            Slot slot = pickedSlot(e.getPickResult().getIntersectedNode());
            boolean valid = slot != null && lesson.pieceAt(slot) == null
                    && e.getDragboard().hasString() && known(e.getDragboard().getString())
                    && lesson.remaining(MosType.valueOf(e.getDragboard().getString())) > 0;
            if (valid) drop.accept(slot, MosType.valueOf(e.getDragboard().getString()));
            e.setDropCompleted(valid);
            e.consume();
        });
        subscene.setOnContextMenuRequested(e -> {
            TerminalRef terminal = pickedTerminal(e.getPickResult().getIntersectedNode());
            if (terminal != null) { selectTerminal.accept(terminal); e.consume(); return; }
            Slot slot = pickedSlot(e.getPickResult().getIntersectedNode());
            if (slot == null) {
                Net net = pickedNet(e.getPickResult().getIntersectedNode());
                if (net != null) { selectNet.accept(net); e.consume(); }
                return;
            }
            select.accept(slot);
            MenuItem detail = new MenuItem("Abrir interior · " + slot);
            detail.setOnAction(action -> inspect.accept(slot));
            MenuItem takeOut = new MenuItem("Quitar pieza · " + slot);
            takeOut.setDisable(lesson.pieceAt(slot) == null);
            takeOut.setOnAction(action -> remove.accept(slot));
            new ContextMenu(detail, takeOut).show(this, e.getScreenX(), e.getScreenY());
            e.consume();
        });
        render();
    }

    private static boolean known(String name) { return "PMOS".equals(name) || "NMOS".equals(name); }

    private static Slot pickedSlot(Node node) {
        if (node == null || !(node.getUserData() instanceof Slot slot)) return null;
        return slot;
    }

    private static TerminalRef pickedTerminal(Node node) {
        return node != null && node.getUserData() instanceof TerminalRef terminal
                ? terminal : null;
    }

    private static Net pickedNet(Node node) {
        if (node == null || !(node.getUserData() instanceof Net net)) return null;
        return net;
    }

    private void handleClick(Slot slot, int count) {
        if (gestureMoved) { gestureMoved = false; return; }
        select.accept(slot);
        if (count >= 2) inspect.accept(slot);
        else if (lesson.pieceAt(slot) == null && activePiece.get() != null)
            drop.accept(slot, activePiece.get());
    }

    void setSelected(Slot slot) { selected = slot; }
    void setSelectedNet(Net net) { selectedNet = net; }
    void setSelectedTerminal(TerminalRef ref) { selectedTerminal = ref; }

    void setPreview(int a, int b) {
        inputA = a;
        inputB = b;
        render();
    }

    void zoomBy(double factor) {
        distance = Math.max(470, Math.min(1800, distance / factor));
        camera.setTranslateZ(-distance);
    }

    int zoomPercent() { return (int) Math.round(100 * 970 / distance); }

    void fit() {
        distance = 970;
        camera.setTranslateZ(-distance);
        pitch.setAngle(-43);
        yaw.setAngle(-22);
        boardGroup.setTranslateX(0);
        boardGroup.setTranslateY(0);
    }

    void render() {
        Nand2Lesson.Signal output = lesson.readyToTest()
                ? lesson.observe(inputA, inputB) : null;
        String outputText = output == null ? "—" : switch (output) {
            case ZERO -> "0";
            case ONE -> "1";
            case X -> "X";
            case Z -> "Z";
        };
        liveSignals.setText("A = " + inputA + "    B = " + inputB + "    Y = " + outputText);
        boardGroup.getChildren().clear();
        Box plate = new Box(720, 16, 410);
        plate.setMaterial(material("#1c5447"));
        boardGroup.getChildren().add(plate);
        // Contornos por cuatro segmentos: Box en modo LINE exponía las
        // diagonales de triangulación de la malla y parecía un artefacto.
        outline(boardGroup, 685, 373, 0, -9.1, 0, "#6da99c", null);

        // Mismas rutas que en el montaje 2D, proyectadas sobre el plano XZ.
        // No son un cálculo de pistas/anchos para una PCB manufacturable.
        for (BoardRouting.Segment segment : BoardRouting.SEGMENTS) {
            double x1 = (segment.a().x() - .5) * 720;
            double x2 = (segment.b().x() - .5) * 720;
            double z1 = (segment.a().y() - .5) * 410;
            double z2 = (segment.b().y() - .5) * 410;
            Box trace = new Box(Math.max(4, Math.abs(x2 - x1)), 1.8,
                    Math.max(4, Math.abs(z2 - z1)));
            trace.setTranslateX((x1 + x2) / 2);
            trace.setTranslateY(-10);
            trace.setTranslateZ((z1 + z2) / 2);
            trace.setMaterial(material(BoardRouting.signalColor(
                    segment.net(), inputA, inputB, output)));
            if (segment.net() == selectedNet) {
                trace.setMaterial(material("#ffd37c"));
            }
            trace.setUserData(segment.net());
            trace.setOnMouseClicked(e -> {
                if (e.getButton() == MouseButton.PRIMARY && !gestureMoved) {
                    selectNet.accept(segment.net());
                }
                e.consume();
            });
            boardGroup.getChildren().add(trace);
        }

        for (double x : new double[]{-318, 318}) {
            for (double z : new double[]{-166, 166}) {
                javafx.scene.shape.Cylinder washer = new javafx.scene.shape.Cylinder(9, 2);
                washer.setMaterial(material("#a8b7bb"));
                washer.setTranslateX(x);
                washer.setTranslateY(-10);
                washer.setTranslateZ(z);
                boardGroup.getChildren().add(washer);
            }
        }

        for (Slot slot : Slot.values()) {
            BoardRouting.Point pos = BoardRouting.slot(slot);
            double x = (pos.x() - .5) * 720;
            double z = (pos.y() - .5) * 410;
            MosType actual = lesson.pieceAt(slot);

            String edge = selected == slot ? "#f3c16b"
                    : actualActive(slot) ? "#9de7bf" : "#91bbaf";
            outline(boardGroup, 130, 80, x, -10.9, z, edge, slot);

            Box body = new Box(119, 30, 61);
            body.setTranslateX(x);
            body.setTranslateY(-27);
            body.setTranslateZ(z);
            String color = actual == null ? "#d7efe8"
                    : actual == slot.expected() ? "#273138" : "#b48246";
            body.setMaterial(actual == null
                    ? new PhongMaterial(Color.web(color, .20)) : material(color));
            body.setUserData(slot);
            configurePieceClick(body, slot);
            boardGroup.getChildren().add(body);

            // Tres terminales en metal con pie horizontal y codo hacia el
            // cuerpo (fuente, drenador y compuerta). Un bloque oscuro sin
            // estas patas parecía una caja sin función electrónica.
            double sign = slot == Slot.P2 || slot == Slot.N2 ? 1 : -1;
            for (int end : new int[]{-1, 1}) {
                Terminal terminal = end < 0 ? Terminal.UPPER : Terminal.LOWER;
                addLead(slot, terminal, x, -10.4, z + end * 44, 11, 2.8, 26);
                addLead(slot, terminal, x, -19.1, z + end * 32, 11, 15, 5);
            }
            addLead(slot, Terminal.GATE, x + sign * 71, -10.4, z, 31, 2.8, 11);
            addLead(slot, Terminal.GATE, x + sign * 61, -19.1, z, 5, 15, 11);

            if (actual != null) {
                Box topSurface = new Box(109, 1.4, 54);
                topSurface.setTranslateX(x);
                topSurface.setTranslateY(-42.7);
                topSurface.setTranslateZ(z);
                topSurface.setMaterial(material("#374b55"));
                topSurface.setUserData(slot);
                configurePieceClick(topSurface, slot);
                boardGroup.getChildren().add(topSurface);
            }

            Text label = new Text(slot + "  " + (actual == null ? slot.expected() : actual));
            label.setFont(Font.font("Consolas", FontWeight.BOLD, 18));
            label.setFill(actual == null ? Color.web("#d7f0e5") : Color.WHITE);
            label.setTranslateX(x + 52);
            label.setTranslateY(-44.1);
            label.setTranslateZ(z + 12);
            // Orientación compuesta: 180° en el plano de la inscripción,
            // seguida de -90° en X. La cara frontal apunta hacia arriba
            // y las letras quedan erguidas. Con solo +90° se veía desde
            // atrás (espejadas); con solo -90°, cabeza abajo.
            label.getTransforms().add(new Affine(
                    -1, 0, 0, 0,
                     0, 0, 1, 0,
                     0, 1, 0, 0));
            label.setUserData(slot);
            configurePieceClick(label, slot);
            boardGroup.getChildren().add(label);
        }
    }

    private boolean actualActive(Slot slot) {
        return lesson.pieceAt(slot) == slot.expected()
                && lesson.isConducting(slot, inputA, inputB);
    }

    private void addLead(Slot slot, Terminal contact, double x, double y, double z,
                         double width, double height, double depth) {
        TerminalRef ref = new TerminalRef(slot, contact);
        Box metal = new Box(width, height, depth);
        metal.setTranslateX(x);
        metal.setTranslateY(y);
        metal.setTranslateZ(z);
        metal.setMaterial(material(ref.equals(selectedTerminal) ? "#ffcd69" : "#bac9d1"));
        metal.setUserData(ref);
        metal.setOnMouseClicked(e -> {
            if (e.getButton() == MouseButton.PRIMARY && !gestureMoved)
                selectTerminal.accept(ref);
            e.consume();
        });
        boardGroup.getChildren().add(metal);
    }

    private void outline(Group group, double width, double depth,
                         double centerX, double centerY, double centerZ,
                         String color, Slot slot) {
        for (int side : new int[]{-1, 1}) {
            Box horizontal = new Box(width, 1.6, 2.0);
            horizontal.setTranslateX(centerX);
            horizontal.setTranslateY(centerY);
            horizontal.setTranslateZ(centerZ + side * depth / 2);
            horizontal.setMaterial(material(color));
            if (slot != null) { horizontal.setUserData(slot); configurePieceClick(horizontal, slot); }
            group.getChildren().add(horizontal);
            Box vertical = new Box(2.0, 1.6, depth);
            vertical.setTranslateX(centerX + side * width / 2);
            vertical.setTranslateY(centerY);
            vertical.setTranslateZ(centerZ);
            vertical.setMaterial(material(color));
            if (slot != null) { vertical.setUserData(slot); configurePieceClick(vertical, slot); }
            group.getChildren().add(vertical);
        }
    }

    private void configurePieceClick(Node node, Slot slot) {
        node.setOnMouseClicked(e -> {
            if (e.getButton() == MouseButton.PRIMARY) handleClick(slot, e.getClickCount());
            e.consume();
        });
    }

    private static PhongMaterial material(String hex) {
        return new PhongMaterial(Color.web(hex));
    }
}
