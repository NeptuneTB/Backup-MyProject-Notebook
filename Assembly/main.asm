main:
xor t0, t0, t0
addi t0, t0 , 1

xor t1, t1, t1
addi t1, t1, 1

xor t2, t2, t2
addi t2, t2, 5

xor t3, t3, t3
addi t3, t3, 2

bne t0, t1, else
add t4, t2, t3
beq zero, zero, Exit

else:
sub t4, t2, t3

Exit: