.data
    var_add: .word 0
    var_div: .word 0
    var_sub: .word 0

.text
.globl main
main:
    # int literal 50
    li   $t0, 50
    # assign add <-- $t0
    sw   $t0, var_add
    # int literal 20
    li   $t1, 20
    # assign sub <-- $t1
    sw   $t1, var_sub
    # int literal 10
    li   $t2, 10
    # assign div <-- $t2
    sw   $t2, var_div
    # read var add
    lw   $t3, var_add
    # print (int)
    move $a0, $t3
    li   $v0, 1
    syscall
    li   $a0, 10
    li   $v0, 11
    syscall
    # read var sub
    lw   $t4, var_sub
    # print (int)
    move $a0, $t4
    li   $v0, 1
    syscall
    li   $a0, 10
    li   $v0, 11
    syscall
    # read var div
    lw   $t5, var_div
    # print (int)
    move $a0, $t5
    li   $v0, 1
    syscall
    li   $a0, 10
    li   $v0, 11
    syscall
    li   $v0, 10
    syscall
