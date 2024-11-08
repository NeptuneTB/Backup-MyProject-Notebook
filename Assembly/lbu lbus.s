main:
xor t0, t0, t0
addi t0, t0, 255

xor t1, t1, t1
addi t1, t1, 0x0128

sb t0, 4(t1)

lbu t2, 4(t1)
lb t2, 4(t1)