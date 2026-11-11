package dev.marcosmoreira.aula.interfaz;

import javafx.scene.canvas.Canvas;
import javafx.scene.canvas.GraphicsContext;
import javafx.scene.input.MouseButton;
import javafx.scene.input.MouseEvent;

/** Paneo y zoom 2D independientes de las coordenadas del circuito. */
final class CanvasNavigation {
    private final Canvas canvas;
    private final Runnable redraw;
    private double zoom = 1.0;
    private double panX;
    private double panY;
    private double lastX;
    private double lastY;
    private boolean panning;
    private boolean dragged;

    CanvasNavigation(Canvas canvas, Runnable redraw) {
        this.canvas = canvas;
        this.redraw = redraw;
        canvas.addEventFilter(MouseEvent.MOUSE_PRESSED, e -> {
            if (e.getButton() == MouseButton.MIDDLE
                    || (e.getButton() == MouseButton.PRIMARY && e.isShiftDown())) {
                panning = true;
                dragged = false;
                lastX = e.getX();
                lastY = e.getY();
                e.consume();
            }
        });
        canvas.addEventFilter(MouseEvent.MOUSE_DRAGGED, e -> {
            if (!panning) return;
            double dx = e.getX() - lastX, dy = e.getY() - lastY;
            if (Math.abs(dx) + Math.abs(dy) > 1) dragged = true;
            panX += dx;
            panY += dy;
            lastX = e.getX();
            lastY = e.getY();
            redraw.run();
            e.consume();
        });
        canvas.addEventFilter(MouseEvent.MOUSE_RELEASED, e -> {
            if (panning) { panning = false; e.consume(); }
        });
        canvas.setOnScroll(e -> {
            zoomBy(e.getDeltaY() >= 0 ? 1.12 : 1 / 1.12, e.getX(), e.getY());
            e.consume();
        });
    }

    boolean suppressClick() {
        boolean result = dragged;
        dragged = false;
        return result;
    }

    double worldX(double localX) {
        return canvas.getWidth() / 2 + (localX - panX - canvas.getWidth() / 2) / zoom;
    }

    double worldY(double localY) {
        return canvas.getHeight() / 2 + (localY - panY - canvas.getHeight() / 2) / zoom;
    }

    void apply(GraphicsContext g) {
        double cx = canvas.getWidth() / 2, cy = canvas.getHeight() / 2;
        g.translate(cx + panX, cy + panY);
        g.scale(zoom, zoom);
        g.translate(-cx, -cy);
    }

    void zoomBy(double factor) {
        zoomBy(factor, canvas.getWidth() / 2, canvas.getHeight() / 2);
    }

    private void zoomBy(double factor, double x, double y) {
        double desired = Math.max(.55, Math.min(3.0, zoom * factor));
        double ratio = desired / zoom;
        panX = ratio * panX + (1 - ratio) * (x - canvas.getWidth() / 2);
        panY = ratio * panY + (1 - ratio) * (y - canvas.getHeight() / 2);
        zoom = desired;
        redraw.run();
    }

    void fit() {
        zoom = 1;
        panX = 0;
        panY = 0;
        redraw.run();
    }

    int zoomPercent() { return (int) Math.round(zoom * 100); }
}
