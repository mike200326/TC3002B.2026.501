.data

.text
.globl main
main:
    # based literal [FF:16] = 255
    li   $t0, 255
    # print (int)
    move $a0, $t0
    li   $v0, 1
    syscall
    li   $a0, 10
    li   $v0, 11
    syscall
    # int literal 255
    li   $t1, 255
    # print (int)
    move $a0, $t1
    li   $v0, 1
    syscall
    li   $a0, 10
    li   $v0, 11
    syscall
    li   $v0, 10
    syscall
