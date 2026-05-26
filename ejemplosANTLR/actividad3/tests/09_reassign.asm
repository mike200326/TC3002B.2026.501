.data
    var_var_x: .word 0

.text
.globl main
main:
    # int literal 100
    li   $t0, 100
    # assign var_x <-- $t0
    sw   $t0, var_var_x
    # read var var_x
    lw   $t1, var_var_x
    # print (int)
    move $a0, $t1
    li   $v0, 1
    syscall
    li   $a0, 10
    li   $v0, 11
    syscall
    # int literal 200
    li   $t2, 200
    # assign var_x <-- $t2
    sw   $t2, var_var_x
    # read var var_x
    lw   $t3, var_var_x
    # print (int)
    move $a0, $t3
    li   $v0, 1
    syscall
    li   $a0, 10
    li   $v0, 11
    syscall
    li   $v0, 10
    syscall
