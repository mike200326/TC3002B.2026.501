.data

.text
.globl main
main:
    # int literal 5
    li   $t0, 5
    # print (int)
    move $a0, $t0
    li   $v0, 1
    syscall
    li   $a0, 10
    li   $v0, 11
    syscall
    li   $v0, 10
    syscall
