`timescale 1ns/1ps
// Prueba para Icarus Verilog: iverilog -g2012 -o registro8_tb registro8.v tb_registro8.v
// Ejecucion: vvp registro8_tb
module tb_registro8;
    reg CLK = 0;
    reg LOAD = 0;
    reg OE_n = 1;
    reg [7:0] IN = 0;
    wire [7:0] BUS;
    integer valor;
    integer errores = 0;

    registro8 dut (.CLK(CLK), .LOAD(LOAD), .OE_n(OE_n), .IN(IN), .BUS(BUS));

    task pulso;
        begin
            #1 CLK = 1;
            #1 CLK = 0;
            #1;
        end
    endtask

    task comprobar;
        input [7:0] esperado;
        begin
            if (BUS !== esperado) begin
                $display("FALLO: esperado=%h, obtenido=%h, t=%0t", esperado, BUS, $time);
                errores = errores + 1;
            end
        end
    endtask

    initial begin
        // Con salida inhabilitada, no se asume contenido conocido en q.
        #1;
        if (BUS !== 8'bzzzzzzzz) begin
            $display("FALLO: se esperaba bus en alta impedancia");
            errores = errores + 1;
        end
        LOAD = 1; IN = 8'h3C; pulso();
        OE_n = 0; #1; comprobar(8'h3C);
        // Una variacion de IN sin flanco NO debe cambiar Q.
        IN = 8'hF0; #1; comprobar(8'h3C);
        // Al no cargar, ni siquiera un flanco debe reemplazar Q.
        LOAD = 0; pulso(); comprobar(8'h3C);
        // OE_n solo coloca Z en el bus, conservando Q.
        OE_n = 1; #1;
        if (BUS !== 8'bzzzzzzzz) errores = errores + 1;
        OE_n = 0; #1; comprobar(8'h3C);
        // Recorrer todo byte posible para comprobar la captura.
        for (valor = 0; valor < 256; valor = valor + 1) begin
            LOAD = 1; IN = valor; pulso(); comprobar(valor[7:0]);
            LOAD = 0; IN = ~valor; pulso(); comprobar(valor[7:0]);
        end
        if (errores != 0) begin
            $display("C28-A: %0d fallos", errores);
            $fatal(1);
        end
        $display("C28-A REGISTRO8: PASS, 256 valores + controles temporales");
        $finish;
    end
endmodule
