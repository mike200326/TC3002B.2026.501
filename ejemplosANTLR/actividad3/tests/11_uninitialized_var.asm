.data
    var_z: .word 0

.text
.globl main
main:
    # read var z
    lw   $t0, var_z
    # print (int)
    move $a0, $t0
    li   $v0, 1
    syscall
    li   $a0, 10
    li   $v0, 11
    syscall
    li   $v0, 10
    syscall
