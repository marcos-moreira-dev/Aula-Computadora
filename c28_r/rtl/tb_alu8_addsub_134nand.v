`timescale 1ns/1ps
// Prueba de lógica combinacional, no de electricidad ni de CPU integrada.
// Recorre todos los 256*256 pares para ADD y SUB, con referencia aritmética
// independiente del netlist y de su generador.
module tb_alu8_addsub_134nand;
    reg [7:0] A, B;
    reg SUB;
    wire [7:0] S;
    wire Cflag, V, N, Z, Cout;
    reg [7:0] b_modificado, esperado;
    reg [8:0] total;
    reg c_esperado, v_esperado;
    integer modo, a, b, fallos;

    alu8_addsub_134nand dut (
        .A(A), .B(B), .SUB(SUB), .S(S), .Cflag(Cflag),
        .V(V), .N(N), .Z(Z), .Cout(Cout)
    );

    initial begin
        A = 0; B = 0; SUB = 0;
        fallos = 0;
        for (modo = 0; modo < 2; modo = modo + 1) begin
            for (a = 0; a < 256; a = a + 1) begin
                for (b = 0; b < 256; b = b + 1) begin
                    A = a[7:0];
                    B = b[7:0];
                    SUB = modo[0];
                    #1;
                    b_modificado = (modo == 1) ? ~B : B;
                    total = {1'b0, A} + {1'b0, b_modificado} + SUB;
                    esperado = total[7:0];
                    c_esperado = total[8] ^ SUB;
                    if (modo == 0)
                        v_esperado = (A[7] == B[7]) && (esperado[7] != A[7]);
                    else
                        v_esperado = (A[7] != B[7]) && (esperado[7] != A[7]);
                    if ({S, Cflag, V, N, Z, Cout} !==
                        {esperado, c_esperado, v_esperado,
                         esperado[7], (esperado == 8'h00), total[8]}) begin
                        if (fallos < 5)
                            $display("FALLO modo=%0d A=%02h B=%02h S=%02h esperado=%02h",
                                     modo, A, B, S, esperado);
                        fallos = fallos + 1;
                    end
                end
            end
        end
        if (fallos != 0) $fatal(1, "C28-R: %0d errores", fallos);
        $display("C28-R: PASS 131072 vectores ADD/SUB; resultado, C, V, N, Z y Cout");
        $finish;
    end
endmodule
