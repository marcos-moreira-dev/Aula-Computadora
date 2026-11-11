// Tabla de flancos generada desde el mismo calendario Python.
module tb_pc16_c28e;
  reg clk, load, clr_test;
  reg [15:0] next_pc;
  wire [15:0] q;
  pc16_c28e dut (.clk(clk), .load(load), .clr_test(clr_test),
                  .next_pc(next_pc), .q(q));
  initial begin
    clk=0; load=0; clr_test=0; next_pc=16'h1111;
    #1;
    // Paso 0: Encender: Q desconocido
    load=1'b0; clr_test=1'b0; next_pc=16'h1111;
    #4;
    clk=1'b0; #1;
    if (q !== 16'hxxxx) $fatal(1, "Fallo paso 0");
    // Paso 1: HOLD en flanco: sigue X
    load=1'b0; clr_test=1'b0; next_pc=16'h1111;
    #4;
    clk=1'b1; #1;
    if (q !== 16'hxxxx) $fatal(1, "Fallo paso 1");
    // Paso 2: LOAD sin nuevo flanco: sigue X
    load=1'b1; clr_test=1'b0; next_pc=16'h6000;
    #4;
    clk=1'b1; #1;
    if (q !== 16'hxxxx) $fatal(1, "Fallo paso 2");
    // Paso 3: CLK baja: sigue X
    load=1'b1; clr_test=1'b0; next_pc=16'h6000;
    #4;
    clk=1'b0; #1;
    if (q !== 16'hxxxx) $fatal(1, "Fallo paso 3");
    // Paso 4: Flanco: cargar 6000
    load=1'b1; clr_test=1'b0; next_pc=16'h6000;
    #4;
    clk=1'b1; #1;
    if (q !== 16'h6000) $fatal(1, "Fallo paso 4");
    // Paso 5: Dato cambia; Q no
    load=1'b0; clr_test=1'b0; next_pc=16'h6003;
    #4;
    clk=1'b0; #1;
    if (q !== 16'h6000) $fatal(1, "Fallo paso 5");
    // Paso 6: HOLD en flanco
    load=1'b0; clr_test=1'b0; next_pc=16'h6003;
    #4;
    clk=1'b1; #1;
    if (q !== 16'h6000) $fatal(1, "Fallo paso 6");
    // Paso 7: Preparar destino JNZ
    load=1'b1; clr_test=1'b0; next_pc=16'h6009;
    #4;
    clk=1'b0; #1;
    if (q !== 16'h6000) $fatal(1, "Fallo paso 7");
    // Paso 8: Flanco: cargar 6009
    load=1'b1; clr_test=1'b0; next_pc=16'h6009;
    #4;
    clk=1'b1; #1;
    if (q !== 16'h6009) $fatal(1, "Fallo paso 8");
    // Paso 9: CLEAR con CLK alto; esperar
    load=1'b1; clr_test=1'b1; next_pc=16'h7777;
    #4;
    clk=1'b1; #1;
    if (q !== 16'h6009) $fatal(1, "Fallo paso 9");
    // Paso 10: CLK baja: Q no cambia
    load=1'b1; clr_test=1'b1; next_pc=16'h7777;
    #4;
    clk=1'b0; #1;
    if (q !== 16'h6009) $fatal(1, "Fallo paso 10");
    // Paso 11: CLEAR gana ante LOAD
    load=1'b1; clr_test=1'b1; next_pc=16'h7777;
    #4;
    clk=1'b1; #1;
    if (q !== 16'h0000) $fatal(1, "Fallo paso 11");
    $display("PC16 C28-E: trazas HDL correctas");
    $finish;
  end
endmodule
