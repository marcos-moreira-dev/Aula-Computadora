// Ejecutar con Icarus Verilog. No verificado en esta edición.
module tb_pc_mar_c28f;
  reg [15:0] pc_q, target, data_addr;
  reg z, jmp, jnz, fetch;
  wire [15:0] pc_inc, pc_d, mar_d;
  wire take;
  integer k;
  reg expected_take;
  pc_mar_c28f dut(
    .pc_q(pc_q), .target(target), .data_addr(data_addr),
    .z(z), .jmp(jmp), .jnz(jnz), .fetch(fetch),
    .pc_inc(pc_inc), .pc_d(pc_d), .mar_d(mar_d), .take(take)
  );
  task check;
    begin
      expected_take = jmp | (jnz & ~z);
      #1;
      if (pc_inc !== ((pc_q + 16'd1) & 16'hffff))
        $fatal(1, "Incremento incorrecto PC=%h", pc_q);
      if (take !== expected_take)
        $fatal(1, "Selector TAKE incorrecto");
      if (pc_d !== (expected_take ? target : (pc_q + 16'd1)))
        $fatal(1, "PC_D incorrecto");
      if (mar_d !== (fetch ? pc_q : data_addr))
        $fatal(1, "MAR_D incorrecto");
    end
  endtask
  initial begin
    pc_q=0; target=0; data_addr=0; z=0; jmp=0; jnz=0; fetch=1;
    for (k=0; k<65536; k=k+1) begin
      pc_q=k; check();
    end
    pc_q=16'h60ff; target=16'h6009; data_addr=16'h6f00;
    for (k=0; k<8000; k=k+1) begin
      pc_q=$random; target=$random; data_addr=$random;
      z=k%2; jmp=(k/2)%2; jnz=(k/4)%2;
      if (jmp && jnz) jnz=0;
      fetch=(k/8)%2;
      check();
    end
    $display("C28-F HDL combinacional: comprobaciones correctas");
    $finish;
  end
endmodule
