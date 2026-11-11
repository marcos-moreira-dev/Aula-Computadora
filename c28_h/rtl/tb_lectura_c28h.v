`timescale 1ns/1ps
// El patron y las salidas esperadas provienen del modelo Python independiente.
// Ejecutar desde la raiz de Aula-Computadora despues de c28h_piloto.py.
module tb_lectura_c28h;
    reg clk = 0;
    always #5 clk = ~clk;
    reg rst_n = 0, req = 0, fetch = 0, pc_write = 0, ready = 0;
    reg [15:0] data_addr = 0, pc_value = 0;
    reg [7:0] data_in = 0;
    wire [15:0] pc_early, mar_early, pc_late, mar_late;
    wire [7:0] mdr_early, mdr_late;
    wire rd_early, busy_early, valid_early, accepted_early, rejected_early;
    wire rd_late, busy_late, valid_late, accepted_late, rejected_late;

    lectura_c28h #(.PC_DEFERRED(0)) early_dut (
        .clk(clk), .rst_n(rst_n), .req(req), .fetch(fetch),
        .pc_write(pc_write), .data_addr(data_addr), .pc_value(pc_value),
        .ready(ready), .data_in(data_in), .pc_q(pc_early),
        .mar_q(mar_early), .mdr_q(mdr_early), .rd(rd_early),
        .busy(busy_early), .mdr_valid(valid_early),
        .accepted(accepted_early), .rejected(rejected_early)
    );
    lectura_c28h #(.PC_DEFERRED(1)) late_dut (
        .clk(clk), .rst_n(rst_n), .req(req), .fetch(fetch),
        .pc_write(pc_write), .data_addr(data_addr), .pc_value(pc_value),
        .ready(ready), .data_in(data_in), .pc_q(pc_late),
        .mar_q(mar_late), .mdr_q(mdr_late), .rd(rd_late),
        .busy(busy_late), .mdr_valid(valid_late),
        .accepted(accepted_late), .rejected(rejected_late)
    );

    // 5 bits de control, 16+16+8 de entradas, 2*45 de salida = 135 bits.
    reg [134:0] vector_in;
    reg [44:0] expected_early, expected_late;
    integer file_handle, scanned, n;
    initial begin
        $dumpfile("c28_h/piloto/c28h_trazas.vcd");
        $dumpvars(0, tb_lectura_c28h);
        file_handle = $fopen("c28_h/piloto/vectores_c28h.mem", "r");
        if (file_handle == 0)
            $fatal(1, "Falta vectores_c28h.mem; ejecutar primero el modelo Python");
        n = 0;
        while (!$feof(file_handle)) begin
            scanned = $fscanf(file_handle, "%h\n", vector_in);
            if (scanned == 1) begin
                @(negedge clk);
                {rst_n, req, fetch, pc_write, ready,
                 data_addr, pc_value, data_in,
                 expected_early, expected_late} = vector_in;
                @(posedge clk);
                #1;
                if ({pc_early, mar_early, mdr_early, rd_early, busy_early,
                     valid_early, accepted_early, rejected_early} !== expected_early)
                    $fatal(1, "C28-H PC anticipado falla en vector %0d", n);
                if ({pc_late, mar_late, mdr_late, rd_late, busy_late,
                     valid_late, accepted_late, rejected_late} !== expected_late)
                    $fatal(1, "C28-H PC diferido falla en vector %0d", n);
                n = n + 1;
            end else if (!$feof(file_handle)) begin
                $fatal(1, "Vector hexadecimal mal formado en linea %0d", n + 1);
            end
        end
        $fclose(file_handle);
        if (n < 10000)
            $fatal(1, "Se esperaban al menos 10000 vectores; hay %0d", n);
        $display("C28-H RTL SECUENCIAL: %0d vectores x DOS alternativas CORRECTOS", n);
        $display("Es simulacion digital ideal, no prueba de retardos ni de integrados.");
        $finish;
    end
endmodule
