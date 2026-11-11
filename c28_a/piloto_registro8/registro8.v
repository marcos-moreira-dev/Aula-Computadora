// C28-A · registro de ocho bits: comportamiento RTL a nivel logico.
// No es un esquema fisico, asignacion de pines ni certificacion electrica.
module registro8 (
    input wire CLK,
    input wire LOAD,
    input wire OE_n,
    input wire [7:0] IN,
    output wire [7:0] BUS
);
    reg [7:0] q;

    // No hay reset ni valor inicial garantizado en este contrato.
    always @(posedge CLK) begin
        if (LOAD)
            q <= IN;
    end

    // OE_n solo gobierna la salida; no destruye q ni lo vuelve a cargar.
    assign BUS = !OE_n ? q : 8'bzzzzzzzz;
endmodule
