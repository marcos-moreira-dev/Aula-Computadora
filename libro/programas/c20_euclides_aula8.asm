; Algoritmo por restas para a=48, b=18, ambos positivos.
; R0 y R1 van convergiendo hasta mcd=6; RET regresa al monitor.
; La CPU Aula-8 todavía NO existe como ejecución validada.
.ORG 0x6000
    LDI R0, 48
    LDI R1, 18
BUCLE:
    CMP R0, R1
    JZ FIN
    JNC RESTAR_A
    SUB R1, R0
    JMP BUCLE
RESTAR_A:
    SUB R0, R1
    JMP BUCLE
FIN:
    ST [0x6F00], R0
    RET
