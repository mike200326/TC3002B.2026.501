.data
    var_x: .word 0

.text
.globl main
main:
    # int literal 42
    li   $t0, 42
    # assign x <-- $t0
    sw   $t0, var_x
    # read var x
    lw   $t1, var_x
    # print (int)
    move $a0, $t1
    li   $v0, 1
    syscall
    li   $a0, 10
    li   $v0, 11
    syscall
    li   $v0, 10
    syscall
