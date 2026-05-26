.data
    var_x: .word 0
    var_y: .word 0

.text
.globl main
main:
    # int literal 10
    li   $t0, 10
    # assign x <-- $t0
    sw   $t0, var_x
    # int literal 3
    li   $t1, 3
    # assign y <-- $t1
    sw   $t1, var_y
    # read var x
    lw   $t2, var_x
    # print (int)
    move $a0, $t2
    li   $v0, 1
    syscall
    li   $a0, 10
    li   $v0, 11
    syscall
    # read var y
    lw   $t3, var_y
    # print (int)
    move $a0, $t3
    li   $v0, 1
    syscall
    li   $a0, 10
    li   $v0, 11
    syscall
    li   $v0, 10
    syscall
