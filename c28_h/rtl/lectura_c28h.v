// C28-H: piloto EDUCATIVO de lectura secuencial; no es una CPU ni una SRAM real.
// PC_DEFERRED=1: PC se incrementa al aceptar FETCH (alternativa C28-G).
// PC_DEFERRED=0: PC se incrementa al solicitar FETCH (alternativa C28-F).
// No elegir una alternativa como definitiva sin aprobacion del autor.
module lectura_c28h #(
    parameter PC_DEFERRED = 1,
    parameter [15:0] PC_RESET = 16'h6000
)(
    input wire clk,
    input wire rst_n,
    input wire req,
    input wire fetch,
    input wire pc_write,
    input wire [15:0] data_addr,
    input wire [15:0] pc_value,
    input wire ready,
    input wire [7:0] data_in,
    output reg [15:0] pc_q,
    output reg [15:0] mar_q,
    output reg [7:0] mdr_q,
    output reg rd,
    output reg busy,
    output reg mdr_valid,
    output reg accepted,
    output reg rejected
);
    reg pending_fetch;

    // rd es una peticion LOGICA. READY no es un pin de chip certificado.
    // req y pc_write son pulsos sincronos. accepted/rejected duran un ciclo.
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            pc_q <= PC_RESET;
            mar_q <= 16'h0000;
            mdr_q <= 8'h00;
            rd <= 1'b0;
            busy <= 1'b0;
            mdr_valid <= 1'b0;
            accepted <= 1'b0;
            rejected <= 1'b0;
            pending_fetch <= 1'b0;
        end else begin
            accepted <= 1'b0;
            rejected <= 1'b0;
            if (!busy) begin
                if (req && pc_write) begin
                    // Ordenes simultaneas incompatibles: no mutar el estado.
                    rejected <= 1'b1;
                end else if (pc_write) begin
                    pc_q <= pc_value;
                end else if (req) begin
                    mar_q <= fetch ? pc_q : data_addr;
                    pending_fetch <= fetch;
                    rd <= 1'b1;
                    busy <= 1'b1;
                    mdr_valid <= 1'b0;
                    if (fetch && !PC_DEFERRED)
                        pc_q <= pc_q + 16'd1;
                end
            end else begin
                if (req || pc_write)
                    rejected <= 1'b1;
                if (ready) begin
                    mdr_q <= data_in;
                    mdr_valid <= 1'b1;
                    accepted <= 1'b1;
                    rd <= 1'b0;
                    busy <= 1'b0;
                    if (pending_fetch && PC_DEFERRED)
                        pc_q <= pc_q + 16'd1;
                end
            end
        end
    end
endmodule
