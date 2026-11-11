// C28-V: piloto SIN CPU. Registros de operandos, ALU NAND y resultado.
// Reutiliza registro8 C28-A sin reset ni valor inicial garantizado.
// CONTRATO: no activar LOAD_A, LOAD_B y EXECUTE simultaneamente;
// durante EXECUTE exactamente un bit de SEL debe ser 1 (ONE-HOT).
module datapath_registros_alu_c28v (
    input wire CLK,
    input wire LOAD_A, LOAD_B, EXECUTE,
    input wire [7:0] DATA_IN,
    input wire [5:0] SEL,
    output wire [7:0] A_Q, B_Q, RESULT_Q,
    output reg N_Q, Z_Q, C_arith_Q, V_arith_Q, CV_valid_Q
);
    wire [7:0] alu_data;
    wire n_now, z_now, c_now, v_now, cv_valid_now;

    // Se mantienen los tres registros del piloto C28-A: no se usa
    // un segundo modelo de flip-flop con semantica divergente.
    registro8 reg_a (.CLK(CLK), .LOAD(LOAD_A), .OE_n(1'b0),
                     .IN(DATA_IN), .BUS(A_Q));
    registro8 reg_b (.CLK(CLK), .LOAD(LOAD_B), .OE_n(1'b0),
                     .IN(DATA_IN), .BUS(B_Q));
    registro8 reg_result (.CLK(CLK), .LOAD(EXECUTE), .OE_n(1'b0),
                          .IN(alu_data), .BUS(RESULT_Q));

    alu8_seis_rutas_359nand alu (
        .A(A_Q), .B(B_Q), .SEL(SEL), .S(alu_data),
        .N(n_now), .Z(z_now), .C_arith(c_now),
        .V_arith(v_now), .CV_valid(cv_valid_now)
    );

    // Captura sincronizada de indicadores del resultado elegido.
    // C/V no deben interpretarse si CV_valid_Q vale 0. No se fija
    // la politica de FLAGS de futuras instrucciones logicas.
    always @(posedge CLK) begin
        if (EXECUTE) begin
            N_Q <= n_now;
            Z_Q <= z_now;
            C_arith_Q <= c_now;
            V_arith_Q <= v_now;
            CV_valid_Q <= cv_valid_now;
        end
    end
endmodule
