package dev.marcosmoreira.aula.interfaz;

import javafx.css.PseudoClass;
import javafx.geometry.Pos;
import javafx.scene.Node;
import javafx.scene.control.Button;
import javafx.scene.control.Label;
import javafx.scene.layout.HBox;
import javafx.scene.layout.Priority;
import javafx.scene.layout.Region;
import javafx.scene.layout.VBox;
import javafx.scene.paint.Color;
import javafx.scene.shape.Polygon;

/** Dock lateral: conserva su sitio en SplitPane y libera ancho al contraerse. */
final class CollapsiblePanel extends VBox {
    private static final PseudoClass COLLAPSED = PseudoClass.getPseudoClass("collapsed");
    private final Label title;
    private final Button toggle;
    private final Polygon arrow;
    private final boolean leftSide;
    private final double preferredWidth;
    private final double minimumWidth;
    private final Runnable onToggle;
    private Node body;
    private boolean expanded = true;

    CollapsiblePanel(String heading, boolean leftSide,
                     double preferredWidth, double minimumWidth, Runnable onToggle) {
        super(0);
        this.leftSide = leftSide;
        this.preferredWidth = preferredWidth;
        this.minimumWidth = minimumWidth;
        this.onToggle = onToggle;
        getStyleClass().addAll("collapsible-panel", leftSide ? "sidebar" : "inspector");
        title = new Label(heading);
        title.getStyleClass().add("panel-title");
        Region space = new Region();
        HBox.setHgrow(space, Priority.ALWAYS);
        arrow = new Polygon(0, 0, 8, 5, 0, 10);
        arrow.setFill(Color.web("#f3f6f8"));
        toggle = new Button();
        toggle.getStyleClass().add("panel-toggle");
        toggle.setGraphic(arrow);
        toggle.setOnAction(e -> setExpanded(!expanded));
        HBox header = new HBox(4, title, space, toggle);
        header.setAlignment(Pos.CENTER_LEFT);
        header.getStyleClass().add("panel-heading");
        getChildren().add(header);
        setExpanded(true);
    }

    void setBody(Node body) {
        this.body = body;
        getChildren().add(body);
        body.setVisible(expanded);
        body.setManaged(expanded);
    }

    boolean isExpanded() { return expanded; }

    private void setExpanded(boolean value) {
        boolean changed = expanded != value;
        expanded = value;
        title.setVisible(value);
        title.setManaged(value);
        if (body != null) { body.setVisible(value); body.setManaged(value); }
        setMinWidth(value ? minimumWidth : 34);
        setPrefWidth(value ? preferredWidth : 34);
        setMaxWidth(value ? Double.MAX_VALUE : 34);
        arrow.setRotate(leftSide ? (value ? 180 : 0) : (value ? 0 : 180));
        toggle.setAccessibleText((value ? "Contraer " : "Expandir ") + title.getText());
        pseudoClassStateChanged(COLLAPSED, !value);
        if (changed) onToggle.run();
    }
}
