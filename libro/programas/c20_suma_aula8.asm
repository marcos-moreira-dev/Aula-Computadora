; Programa de ejemplo C20. No ejecutado sobre CPU Aula-8.
.ORG 0x6000
    LDI R0, 13
    LDI R1, 9
    ADD R0, R1
    ST [0x6F00], R0
    RET
