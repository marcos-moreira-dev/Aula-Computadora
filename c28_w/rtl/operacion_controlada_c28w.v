// C28-W. Control automatico de UN calculo; todavia NO es una CPU.
// Contrato: RESET sincrono solo para CONTROL; no borra los registros C28-A.
// A_IN, B_IN y OP_SEL deben permanecer estables desde START hasta DONE.
// OP_SEL es ONE-HOT en el flanco EXEC. START durante BUSY se ignora.

module secuenciador_tres_fases_c28w (
    input wire CLK, RESET, START,
    output wire LOAD_A, LOAD_B, EXECUTE,
    output wire READY, BUSY, DONE, RESULT_VALID,
    output wire [2:0] FASE
);
    localparam [2:0] IDLE = 3'd0;
    localparam [2:0] CAPTURA_A = 3'd1;
    localparam [2:0] CAPTURA_B = 3'd2;
    localparam [2:0] CALCULA = 3'd3;
    localparam [2:0] TERMINO = 3'd4;

    reg [2:0] fase_actual;
    reg resultado_valido;

    assign FASE = fase_actual;
    assign LOAD_A = (fase_actual == CAPTURA_A) && !RESET;
    assign LOAD_B = (fase_actual == CAPTURA_B) && !RESET;
    assign EXECUTE = (fase_actual == CALCULA) && !RESET;
    assign READY = (fase_actual == IDLE) || (fase_actual == TERMINO);
    assign BUSY = !READY;
    assign DONE = (fase_actual == TERMINO);
    assign RESULT_VALID = resultado_valido;

    always @(posedge CLK) begin
        if (RESET) begin
            fase_actual <= IDLE;
            resultado_valido <= 1'b0;
        end else begin
            case (fase_actual)
                IDLE: if (START) begin
                    fase_actual <= CAPTURA_A;
                    resultado_valido <= 1'b0;
                end
                CAPTURA_A: fase_actual <= CAPTURA_B;
                CAPTURA_B: fase_actual <= CALCULA;
                CALCULA: begin
                    fase_actual <= TERMINO;
                    resultado_valido <= 1'b1;
                end
                TERMINO: if (START) begin
                    fase_actual <= CAPTURA_A;
                    resultado_valido <= 1'b0;
                end
                default: begin
                    fase_actual <= IDLE;
                    resultado_valido <= 1'b0;
                end
            endcase
        end
    end
endmodule

module operacion_controlada_c28w (
    input wire CLK, RESET, START,
    input wire [7:0] A_IN, B_IN,
    input wire [5:0] OP_SEL,
    output wire [7:0] A_Q, B_Q, RESULT_Q,
    output wire N_Q, Z_Q, C_arith_Q, V_arith_Q, CV_valid_Q,
    output wire READY, BUSY, DONE, RESULT_VALID,
    output wire [2:0] FASE,
    output wire [7:0] BUS_DATA
);
    wire load_a, load_b, execute;

    secuenciador_tres_fases_c28w control (
        .CLK(CLK), .RESET(RESET), .START(START),
        .LOAD_A(load_a), .LOAD_B(load_b), .EXECUTE(execute),
        .READY(READY), .BUSY(BUSY), .DONE(DONE),
        .RESULT_VALID(RESULT_VALID), .FASE(FASE)
    );

    // Un unico puerto DATA_IN: el controlador elige su fuente.
    // El mux en esta etapa es logico/RTL, aun no una netlist NAND.
    assign BUS_DATA = load_b ? B_IN : A_IN;

    datapath_registros_alu_c28v camino (
        .CLK(CLK), .LOAD_A(load_a), .LOAD_B(load_b), .EXECUTE(execute),
        .DATA_IN(BUS_DATA), .SEL(OP_SEL),
        .A_Q(A_Q), .B_Q(B_Q), .RESULT_Q(RESULT_Q),
        .N_Q(N_Q), .Z_Q(Z_Q), .C_arith_Q(C_arith_Q),
        .V_arith_Q(V_arith_Q), .CV_valid_Q(CV_valid_Q)
    );
endmodule
