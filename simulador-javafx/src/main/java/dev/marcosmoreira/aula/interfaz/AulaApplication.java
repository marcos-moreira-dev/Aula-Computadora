package dev.marcosmoreira.aula.interfaz;

import dev.marcosmoreira.aula.circuitos.Nand2Lesson;
import dev.marcosmoreira.aula.circuitos.Nand2Lesson.MosType;
import dev.marcosmoreira.aula.circuitos.Nand2Lesson.Slot;
import javafx.application.Application;
import javafx.application.ConditionalFeature;
import javafx.application.Platform;
import javafx.geometry.Insets;
import javafx.scene.Scene;
import javafx.scene.control.Alert;
import javafx.scene.control.Button;
import javafx.scene.control.Label;
import javafx.scene.control.Menu;
import javafx.scene.control.MenuBar;
import javafx.scene.control.MenuItem;
import javafx.scene.control.Separator;
import javafx.scene.control.SplitPane;
import javafx.scene.control.Tab;
import javafx.scene.control.TabPane;
import javafx.scene.control.TextArea;
import javafx.scene.control.ToolBar;
import javafx.scene.control.ToggleButton;
import javafx.scene.input.ClipboardContent;
import javafx.scene.input.KeyCode;
import javafx.scene.input.KeyCodeCombination;
import javafx.scene.input.TransferMode;
import javafx.scene.layout.BorderPane;
import javafx.scene.layout.HBox;
import javafx.scene.layout.Priority;
import javafx.scene.layout.StackPane;
import javafx.scene.layout.VBox;
import javafx.stage.Stage;

import javax.imageio.ImageIO;
import java.awt.Rectangle;
import java.awt.Robot;
import java.awt.image.BufferedImage;
import java.nio.file.Files;
import java.nio.file.Path;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.ArrayDeque;
import java.util.Deque;
import java.util.Map;
import java.util.Objects;
import java.util.prefs.BackingStoreException;
import java.util.prefs.Preferences;

/** Primer corte ejecutable: montaje NAND2 e inspección 2D, no CPU ni PCB. */
public final class AulaApplication extends Application {
    private final Nand2Lesson lesson = new Nand2Lesson();
    private final Deque<Map<Slot, MosType>> undoStack = new ArrayDeque<>();
    private final Preferences preferences = Preferences.userNodeForPackage(AulaApplication.class);
    private MosType activePiece;
    private Slot selectedSlot;
    private String saveState = "sin cambios";
    private NandBoardView board;
    private NandLogicView logic;
    private NandBoard3DView board3d;
    private Tab assemblyTab;
    private Tab detailTab;
    private Tab threeDTab;
    private Button pmosButton;
    private Button nmosButton;
    private Button undoButton;
    private Button removeButton;
    private Button testButton;
    private Button detailsButton;
    private MenuItem testMenuItem;
    private MenuItem removeMenuItem;
    private MenuItem undoMenuItem;
    private Label inspectorTitle;
    private Label inspectorContent;
    private Label liveOutput;
    private ToggleButton inputAButton;
    private ToggleButton inputBButton;
    private int inputA;
    private int inputB;
    private Label status;
    private Label stageLabel;
    private TextArea resultArea;
    private VBox resultDock;
    private TabPane workspaceTabs;
    private SplitPane workspaceSplit;
    private CollapsiblePanel sidebarPanel;
    private CollapsiblePanel inspectorPanel;
    private int screenshotCount;

    @Override
    public void start(Stage stage) {
        loadProgress();
        BorderPane root = new BorderPane();
        root.getStyleClass().add("app-root");
        root.setTop(new VBox(buildMenu(stage), buildToolbar(stage)));

        board = new NandBoardView(lesson, () -> activePiece, this::select,
                this::place, this::inspect, this::remove);
        logic = new NandLogicView(lesson);
        workspaceTabs = new TabPane();
        assemblyTab = new Tab("Montaje 2D", wrapCanvas(board));
        detailTab = new Tab("Interior NAND (2 entradas)", wrapCanvas(logic));
        if (Platform.isSupported(ConditionalFeature.SCENE3D)) {
            board3d = new NandBoard3DView(lesson, () -> activePiece,
                    this::select, this::place, this::inspect, this::remove);
            threeDTab = new Tab("Placa 3D", board3d);
        } else {
            threeDTab = new Tab("Placa 3D (no disponible)");
            threeDTab.setDisable(true);
        }
        assemblyTab.setClosable(false);
        detailTab.setClosable(false);
        threeDTab.setClosable(false);
        workspaceTabs.getTabs().addAll(threeDTab, assemblyTab, detailTab);
        workspaceTabs.getSelectionModel().select(assemblyTab);
        workspaceTabs.getSelectionModel().selectedItemProperty().addListener((o, oldTab, newTab) -> {
            if (newTab == detailTab) logic.render();
            refreshStatus();
        });
        workspaceSplit = new SplitPane(buildSidebar(), workspaceTabs, buildInspector());
        workspaceSplit.setDividerPositions(.19, .81);
        root.setCenter(workspaceSplit);

        resultDock = buildResults();
        resultDock.setVisible(false);
        resultDock.setManaged(false);
        status = new Label();
        status.getStyleClass().add("status-line");
        status.setMaxWidth(Double.MAX_VALUE);
        root.setBottom(new VBox(resultDock, status));

        Scene scene = new Scene(root, 1370, 820);
        scene.getAccelerators().put(new KeyCodeCombination(KeyCode.F12), () -> capture(stage));
        scene.getStylesheets().add(Objects.requireNonNull(
                getClass().getResource("/estilo-aula.css")).toExternalForm());
        stage.setTitle("Aula Computadora — primer taller NAND2 [prototipo]");
        stage.setMinWidth(1080);
        stage.setMinHeight(690);
        stage.setScene(scene);
        refresh();
        stage.show();
    }

    private MenuBar buildMenu(Stage stage) {
        Menu archivo = new Menu("Archivo");
        MenuItem salir = new MenuItem("Salir");
        salir.setOnAction(e -> stage.close());
        archivo.getItems().add(salir);

        Menu editar = new Menu("Editar");
        undoMenuItem = new MenuItem("Deshacer");
        undoMenuItem.setOnAction(e -> undo());
        removeMenuItem = new MenuItem("Quitar pieza seleccionada");
        removeMenuItem.setOnAction(e -> removeSelected());
        MenuItem reiniciar = new MenuItem("Restablecer ejercicio...");
        reiniciar.setOnAction(e -> confirmReset());
        editar.getItems().addAll(undoMenuItem, removeMenuItem, reiniciar);

        Menu ver = new Menu("Ver");
        MenuItem tresD = new MenuItem("Placa 3D conceptual");
        tresD.setOnAction(e -> {
            if (board3d != null) workspaceTabs.getSelectionModel().select(threeDTab);
        });
        MenuItem montaje = new MenuItem("Montaje 2D");
        montaje.setOnAction(e -> workspaceTabs.getSelectionModel().select(assemblyTab));
        MenuItem detalle = new MenuItem("Interior NAND (2 entradas)");
        detalle.setOnAction(e -> workspaceTabs.getSelectionModel().select(detailTab));
        ver.getItems().addAll(tresD, montaje, detalle);

        Menu recorrido = new Menu("Recorrido");
        MenuItem inicial = new MenuItem("Etapa 1 — NAND2 de 4 MOS");
        inicial.setDisable(true);
        recorrido.getItems().add(inicial);

        Menu simulacion = new Menu("Simulación");
        testMenuItem = new MenuItem("Probar NAND2");
        testMenuItem.setOnAction(e -> test());
        simulacion.getItems().add(testMenuItem);

        Menu ayuda = new Menu("Ayuda");
        MenuItem controles = new MenuItem("Controles de montaje");
        controles.setOnAction(e -> dialog(Alert.AlertType.INFORMATION,
                "Controles de montaje", "Cómo usar el primer taller",
                "Selecciona PMOS o NMOS y pulsa un hueco, o arrastra la pieza desde el kit. "
                        + "Clic: seleccionar. Doble clic: inspeccionar. "
                        + "Las piezas incorrectas se admiten para aprender del resultado. "
                        + "Solo se prueba un montaje de cuatro piezas.").showAndWait());
        ayuda.getItems().add(controles);

        return new MenuBar(archivo, editar, ver, recorrido, simulacion, ayuda);
    }

    private ToolBar buildToolbar(Stage stage) {
        undoButton = toolButton("Deshacer", "undo");
        undoButton.setOnAction(e -> undo());
        removeButton = toolButton("Quitar", "remove");
        removeButton.setOnAction(e -> removeSelected());
        Button hint = toolButton("Pista", "hint");
        hint.setOnAction(e -> {
            inspectorTitle.setText("Pista");
            inspectorContent.setText("Los dos PMOS forman la rama en paralelo hacia VDD. "
                    + "Los dos NMOS forman la rama en serie hacia GND. ");
        });
        detailsButton = toolButton("Abrir interior", "detail");
        detailsButton.setOnAction(e -> inspect(selectedSlot));
        testButton = toolButton("Probar montaje", "test");
        testButton.getStyleClass().add("primary-action");
        testButton.setOnAction(e -> test());
        Button zoomIn = toolButton("Acercar", "zoom-in");
        zoomIn.setOnAction(e -> zoom(.85));
        Button zoomOut = toolButton("Alejar", "zoom-out");
        zoomOut.setOnAction(e -> zoom(1.15));
        Button fit = toolButton("Centrar", "fit");
        fit.setOnAction(e -> fit());
        Button camera = toolButton("Captura F12", "camera");
        camera.setOnAction(e -> capture(stage));
        return new ToolBar(undoButton, removeButton, hint, new Separator(), detailsButton,
                new Separator(), testButton, new Separator(), zoomIn, zoomOut, fit,
                new Separator(), camera);
    }

    private Button toolButton(String text, String icon) {
        Button button = new Button(text, ToolbarIcons.make(icon));
        button.getStyleClass().add("toolbar-button");
        return button;
    }

    private void zoom(double inverseFactor) {
        // Proporciones consistentes entre tabs; Zoom + disminuye distancia 3D.
        if (workspaceTabs.getSelectionModel().getSelectedItem() == threeDTab && board3d != null)
            board3d.zoomBy(1 / inverseFactor);
        else if (workspaceTabs.getSelectionModel().getSelectedItem() == detailTab)
            logic.zoomBy(1 / inverseFactor);
        else board.zoomBy(1 / inverseFactor);
        refreshStatus();
    }

    private void fit() {
        if (workspaceTabs.getSelectionModel().getSelectedItem() == threeDTab && board3d != null)
            board3d.fit();
        else if (workspaceTabs.getSelectionModel().getSelectedItem() == detailTab) logic.fit();
        else board.fit();
        refreshStatus();
    }

    private CollapsiblePanel buildSidebar() {
        stageLabel = new Label("01  ·  NAND2 CMOS");
        stageLabel.getStyleClass().add("stage-label");
        Label kitLabel = new Label("KIT DE COMPONENTES");
        kitLabel.getStyleClass().add("section-label");
        pmosButton = pieceButton(MosType.PMOS);
        nmosButton = pieceButton(MosType.NMOS);
        Label tip = new Label("Elige o arrastra una pieza.\nEl molde admite errores.");
        tip.setWrapText(true);
        tip.getStyleClass().add("muted-note");
        VBox body = new VBox(11, stageLabel, new Separator(), kitLabel,
                pmosButton, nmosButton, tip);
        body.getStyleClass().add("panel-body");
        body.setPadding(new Insets(9, 11, 12, 11));
        sidebarPanel = new CollapsiblePanel("RECORRIDO", true, 210, 170,
                this::adjustPanelDividers);
        sidebarPanel.setBody(body);
        return sidebarPanel;
    }

    private Button pieceButton(MosType type) {
        Button button = new Button();
        button.setMaxWidth(Double.MAX_VALUE);
        button.getStyleClass().add("kit-piece");
        button.setGraphic(ToolbarIcons.make("component"));
        button.setOnAction(e -> {
            activePiece = activePiece == type ? null : type;
            refresh();
        });
        button.setOnDragDetected(e -> {
            if (lesson.remaining(type) == 0) return;
            javafx.scene.input.Dragboard dragboard = button.startDragAndDrop(TransferMode.COPY);
            ClipboardContent content = new ClipboardContent();
            content.putString(type.name());
            dragboard.setContent(content);
            e.consume();
        });
        return button;
    }

    private CollapsiblePanel buildInspector() {
        inspectorTitle = new Label("NAND2");
        inspectorTitle.getStyleClass().add("inspector-title");
        inspectorContent = new Label();
        inspectorContent.setWrapText(true);
        inspectorContent.getStyleClass().add("inspector-copy");
        Label warning = new Label("Modelo digital ideal.\nSin pinout ni verificación física.");
        warning.getStyleClass().add("muted-note");
        warning.setWrapText(true);
        Label liveTitle = new Label("SIMULACIÓN EN VIVO");
        liveTitle.getStyleClass().add("section-label");
        inputAButton = new ToggleButton("A = 0");
        inputBButton = new ToggleButton("B = 0");
        inputAButton.getStyleClass().add("input-bit");
        inputBButton.getStyleClass().add("input-bit");
        inputAButton.setMaxWidth(Double.MAX_VALUE);
        inputBButton.setMaxWidth(Double.MAX_VALUE);
        HBox liveInputs = new HBox(8, inputAButton, inputBButton);
        HBox.setHgrow(inputAButton, Priority.ALWAYS);
        HBox.setHgrow(inputBButton, Priority.ALWAYS);
        inputAButton.setOnAction(e -> {
            inputA = inputAButton.isSelected() ? 1 : 0;
            refreshLiveOutput();
        });
        inputBButton.setOnAction(e -> {
            inputB = inputBButton.isSelected() ? 1 : 0;
            refreshLiveOutput();
        });
        liveOutput = new Label();
        liveOutput.getStyleClass().add("live-output");
        liveOutput.setWrapText(true);
        VBox body = new VBox(12, inspectorTitle, inspectorContent,
                new Separator(), liveTitle, liveInputs, liveOutput,
                new Separator(), warning);
        body.getStyleClass().add("panel-body");
        body.setPadding(new Insets(9, 12, 12, 12));
        inspectorPanel = new CollapsiblePanel("INSPECTOR", false, 265, 205,
                this::adjustPanelDividers);
        inspectorPanel.setBody(body);
        return inspectorPanel;
    }

    private void adjustPanelDividers() {
        if (workspaceSplit == null || sidebarPanel == null || inspectorPanel == null) return;
        Platform.runLater(() -> {
            double width = Math.max(1080, workspaceSplit.getWidth());
            double first = sidebarPanel.isExpanded() ? .19 : 36 / width;
            double second = inspectorPanel.isExpanded() ? .81 : 1 - 36 / width;
            workspaceSplit.setDividerPositions(first, second);
        });
    }

    private VBox buildResults() {
        VBox dock = new VBox(3);
        dock.getStyleClass().add("results-dock");
        Label title = new Label("PRUEBAS  ·  NAND2");
        title.getStyleClass().add("panel-heading");
        resultArea = new TextArea();
        resultArea.setEditable(false);
        resultArea.setFocusTraversable(false);
        resultArea.setPrefRowCount(5);
        resultArea.getStyleClass().add("result-text");
        VBox.setVgrow(resultArea, Priority.ALWAYS);
        dock.getChildren().addAll(title, resultArea);
        dock.setPrefHeight(160);
        dock.setMaxHeight(190);
        return dock;
    }

    private StackPane wrapCanvas(javafx.scene.canvas.Canvas canvas) {
        StackPane pane = new StackPane(canvas);
        pane.getStyleClass().add("canvas-container");
        pane.setMinHeight(350);
        canvas.widthProperty().bind(pane.widthProperty());
        canvas.heightProperty().bind(pane.heightProperty());
        return pane;
    }

    private void select(Slot slot) {
        selectedSlot = slot;
        refresh();
    }

    private void inspect(Slot slot) {
        if (slot == null) return;
        selectedSlot = slot;
        workspaceTabs.getSelectionModel().select(detailTab);
        refresh();
    }

    private void place(Slot slot, MosType type) {
        Map<Slot, MosType> before = lesson.snapshot();
        if (lesson.place(slot, type)) {
            undoStack.push(before);
            selectedSlot = slot;
            activePiece = lesson.remaining(type) == 0 ? null : activePiece;
            closeStaleResults();
            saveProgress();
        }
        refresh();
    }

    private void removeSelected() {
        remove(selectedSlot);
    }

    private void remove(Slot slot) {
        if (slot == null || lesson.pieceAt(slot) == null) return;
        Map<Slot, MosType> before = lesson.snapshot();
        if (lesson.remove(slot)) {
            undoStack.push(before);
            selectedSlot = slot;
            closeStaleResults();
            saveProgress();
        }
        refresh();
    }

    private void undo() {
        if (undoStack.isEmpty()) return;
        lesson.restore(undoStack.pop());
        closeStaleResults();
        saveProgress();
        refresh();
    }

    private void confirmReset() {
        Alert alert = dialog(Alert.AlertType.CONFIRMATION,
                "Restablecer etapa", "Confirmar restablecimiento",
                "¿Vaciar las cuatro posiciones del ejercicio? Puedes usar Deshacer después.");
        alert.showAndWait().ifPresent(choice -> {
            if (choice == javafx.scene.control.ButtonType.OK) {
                undoStack.push(lesson.snapshot());
                lesson.restore(Map.of());
                activePiece = null;
                selectedSlot = null;
                closeStaleResults();
                saveProgress();
                refresh();
            }
        });
    }

    private Alert dialog(Alert.AlertType type, String title, String header, String message) {
        Alert alert = new Alert(type);
        alert.setTitle(title);
        alert.setHeaderText(header);
        Label content = new Label(message);
        content.setWrapText(true);
        content.setPrefWidth(520);
        content.setMaxWidth(Double.MAX_VALUE);
        alert.getDialogPane().setContent(content);
        alert.getDialogPane().setMinWidth(590);
        alert.getDialogPane().getStylesheets().add(Objects.requireNonNull(
                getClass().getResource("/estilo-aula.css")).toExternalForm());
        return alert;
    }

    private void test() {
        if (!lesson.readyToTest()) return;
        StringBuilder text = new StringBuilder("A  B  Esperado  Observado  Resultado\n");
        int ok = 0;
        for (Nand2Lesson.TruthRow row : lesson.testTruthTable()) {
            if (row.passes()) ok++;
            String value = switch (row.observed()) {
                case ZERO -> "0";
                case ONE -> "1";
                case X -> "X (contención ideal)";
                case Z -> "Z (flotante ideal)";
            };
            text.append(row.a()).append("  ").append(row.b()).append("       ")
                    .append(row.expected()).append("         ")
                    .append(value).append("       ")
                    .append(row.passes() ? "OK" : "DIFIERE").append('\n');
        }
        text.append("\n").append(ok).append("/4 vectores coinciden. ")
                .append(ok == 4 ? "NAND2 ideal comprobada." : "Inspecciona las salidas discrepantes.")
                .append("\nNo constituye validación eléctrica o física.");
        resultArea.setText(text.toString());
        resultDock.setManaged(true);
        resultDock.setVisible(true);
    }

    private void closeStaleResults() {
        resultDock.setVisible(false);
        resultDock.setManaged(false);
        resultArea.clear();
    }

    private void refresh() {
        pmosButton.setText("PMOS  ·  " + lesson.remaining(MosType.PMOS) + " disponibles");
        nmosButton.setText("NMOS  ·  " + lesson.remaining(MosType.NMOS) + " disponibles");
        pmosButton.setDisable(lesson.remaining(MosType.PMOS) == 0);
        nmosButton.setDisable(lesson.remaining(MosType.NMOS) == 0);
        pmosButton.pseudoClassStateChanged(javafx.css.PseudoClass.getPseudoClass("picked"),
                activePiece == MosType.PMOS);
        nmosButton.pseudoClassStateChanged(javafx.css.PseudoClass.getPseudoClass("picked"),
                activePiece == MosType.NMOS);
        stageLabel.setText("01  ·  NAND2 CMOS\nMontaje: " + lesson.placedCount() + "/4");
        testButton.setDisable(!lesson.readyToTest());
        undoButton.setDisable(undoStack.isEmpty());
        removeButton.setDisable(selectedSlot == null || lesson.pieceAt(selectedSlot) == null);
        testMenuItem.setDisable(!lesson.readyToTest());
        undoMenuItem.setDisable(undoStack.isEmpty());
        removeMenuItem.setDisable(selectedSlot == null || lesson.pieceAt(selectedSlot) == null);
        detailsButton.setDisable(selectedSlot == null);
        if (selectedSlot != null) {
            MosType actual = lesson.pieceAt(selectedSlot);
            inspectorTitle.setText(selectedSlot.name() + "  ·  "
                    + (actual == null ? "hueco" : actual.toString()));
            inspectorContent.setText("Esperado: " + selectedSlot.expected() + "\n"
                    + "Puerta: " + selectedSlot.gate() + "\n"
                    + "Red conceptual: " + selectedSlot.nets() + "\n"
                    + "Montado: " + (actual == null ? "no" : "sí"));
        } else {
            inspectorTitle.setText("Módulo NAND2");
            inspectorContent.setText("Cuatro posiciones. El molde empieza vacío. "
                    + "Selecciona un componente para ver sus datos.");
        }
        if (board != null) { board.setSelected(selectedSlot); board.render(); }
        if (logic != null) { logic.setSelected(selectedSlot); logic.render(); }
        if (board3d != null) board3d.setSelected(selectedSlot);
        refreshLiveOutput();
        refreshStatus();
    }

    private void refreshLiveOutput() {
        if (inputAButton == null || inputBButton == null || liveOutput == null) return;
        inputAButton.setText("A = " + inputA);
        inputBButton.setText("B = " + inputB);
        if (lesson.readyToTest()) {
            Nand2Lesson.Signal observed = lesson.observe(inputA, inputB);
            String value = switch (observed) {
                case ZERO -> "0";
                case ONE -> "1";
                case X -> "X · contención";
                case Z -> "Z · flotante";
            };
            liveOutput.setText("Y = " + value);
        } else {
            liveOutput.setText("Y = — · monta las cuatro piezas");
        }
        if (logic != null) logic.setPreview(inputA, inputB, lesson.readyToTest());
    }

    private void refreshStatus() {
        if (status == null || workspaceTabs == null) return;
        Tab tab = workspaceTabs.getSelectionModel().getSelectedItem();
        int zoomPercent = tab == threeDTab && board3d != null ? board3d.zoomPercent()
                : tab == detailTab ? logic.zoomPercent() : board.zoomPercent();
        status.setText("Aula-8  |  Etapa 01  |  " + lesson.placedCount()
                + "/4 piezas  |  CPU: no implementada  |  Guardado: " + saveState
                + "  |  " + tab.getText() + "  |  Zoom: " + zoomPercent + "%");
    }

    private void capture(Stage stage) {
        try {
            Path folder = Path.of(System.getProperty("user.dir"), "capturas");
            Files.createDirectories(folder);
            Rectangle bounds = new Rectangle((int) Math.round(stage.getX()),
                    (int) Math.round(stage.getY()), (int) Math.round(stage.getWidth()),
                    (int) Math.round(stage.getHeight()));
            if (bounds.width < 100 || bounds.height < 100) {
                throw new IllegalStateException("La ventana no tiene dimensiones válidas");
            }
            BufferedImage pixels = new Robot().createScreenCapture(bounds);
            String timestamp = LocalDateTime.now().format(
                    DateTimeFormatter.ofPattern("yyyyMMdd_HHmmss_SSS"));
            Path png = folder.resolve(String.format("AULA_%02d_%s.png", ++screenshotCount, timestamp));
            if (!ImageIO.write(pixels, "png", png.toFile())) {
                throw new IllegalStateException("No hay codificador PNG disponible");
            }
            status.setText("Captura guardada: " + png.getFileName()
                    + "  |  Cierra la app para terminar la retroalimentación");
        } catch (Exception ex) {
            status.setText("No se pudo capturar la ventana: " + ex.getMessage());
        }
    }

    private void loadProgress() {
        String encoded = preferences.get("nand2.slots.v1", "");
        Nand2Lesson candidate = new Nand2Lesson();
        try {
            if (!encoded.isBlank()) {
                for (String item : encoded.split(",")) {
                    String[] pair = item.split("=");
                    if (pair.length != 2 || !candidate.place(Slot.valueOf(pair[0]),
                            MosType.valueOf(pair[1]))) {
                        throw new IllegalArgumentException("Estado no válido");
                    }
                }
            }
            lesson.restore(candidate.snapshot());
            saveState = "recuperado";
        } catch (IllegalArgumentException ex) {
            // Un guardado corrupto no debe crear componentes ni simular éxito.
            saveState = "no recuperable";
        }
    }

    private void saveProgress() {
        StringBuilder encoded = new StringBuilder();
        for (Slot slot : Slot.values()) {
            MosType type = lesson.pieceAt(slot);
            if (type == null) continue;
            if (encoded.length() != 0) encoded.append(',');
            encoded.append(slot).append('=').append(type);
        }
        try {
            preferences.put("nand2.slots.v1", encoded.toString());
            preferences.flush();
            saveState = "correcto";
        } catch (BackingStoreException | SecurityException ex) {
            saveState = "ERROR";
        }
    }

    public static void main(String[] args) { launch(args); }
}
