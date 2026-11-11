package dev.marcosmoreira.aula.interfaz;

import javafx.scene.Group;
import javafx.scene.Node;
import javafx.scene.paint.Color;
import javafx.scene.shape.SVGPath;
import javafx.scene.shape.StrokeLineCap;
import javafx.scene.shape.StrokeLineJoin;

/** Iconos originales, vectoriales y monocromos; ninguna fuente de emoji. */
final class ToolbarIcons {
    private ToolbarIcons() { }

    static Node make(String name) {
        String geometry = switch (name) {
            case "undo" -> "M9 4 L4 9 L9 14 M4 9 H14 C18 9 20 11 20 15 C20 19 17 21 13 21 H9";
            case "remove" -> "M5 7 H19 M9 7 V4 H15 V7 M7 7 L8 21 H16 L17 7 M10 10 V18 M14 10 V18";
            case "hint" -> "M9 17 H15 M10 20 H14 M12 3 C7 3 5 7 5 11 C5 14 7 15 9 17 H15 C17 15 19 14 19 11 C19 7 17 3 12 3 Z";
            case "detail" -> "M4 3 H16 V15 H4 Z M7 6 H13 V12 H7 Z M15 15 L21 21 M17 17 L19 15";
            case "test" -> "M3 4 H21 V20 H3 Z M7 12 L11 16 L17 8";
            case "zoom-in" -> "M10 3 C6 3 3 6 3 10 C3 14 6 17 10 17 C14 17 17 14 17 10 C17 6 14 3 10 3 Z M14.5 14.5 L21 21 M6 10 H14 M10 6 V14";
            case "zoom-out" -> "M10 3 C6 3 3 6 3 10 C3 14 6 17 10 17 C14 17 17 14 17 10 C17 6 14 3 10 3 Z M14.5 14.5 L21 21 M6 10 H14";
            case "fit" -> "M3 9 V3 H9 M15 3 H21 V9 M21 15 V21 H15 M9 21 H3 V15 M7 7 H17 V17 H7 Z";
            case "orbit" -> "M12 3 L20 7 L20 16 L12 21 L4 16 L4 7 Z M4 7 L12 12 L20 7 M12 12 V21 M7 3 L4 7";
            case "component" -> "M7 5 H17 V18 H7 Z M10 18 V22 M14 18 V22 M5 9 H7 M17 9 H19";
            case "camera" -> "M3 7 H8 L10 4 H15 L17 7 H21 V20 H3 Z M12 10 C9 10 8 12 8 14 C8 16 10 18 12 18 C14 18 16 16 16 14 C16 12 14 10 12 10 Z";
            default -> throw new IllegalArgumentException("Icono desconocido: " + name);
        };
        SVGPath svg = new SVGPath();
        svg.setContent(geometry);
        svg.setFill(Color.TRANSPARENT);
        svg.setStroke(Color.web("#405b6c"));
        svg.setStrokeWidth(1.6);
        svg.setStrokeLineCap(StrokeLineCap.SQUARE);
        svg.setStrokeLineJoin(StrokeLineJoin.MITER);
        svg.setScaleX(.78);
        svg.setScaleY(.78);
        Group icon = new Group(svg);
        icon.setMouseTransparent(true);
        return icon;
    }
}
