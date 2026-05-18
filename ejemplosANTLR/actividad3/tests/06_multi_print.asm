.data
    str_0: .asciiz "hola mundo"

.text
.globl main
main:
    # int literal 42
    li   $t0, 42
    # print (int)
    move $a0, $t0
    li   $v0, 1
    syscall
    li   $a0, 10
    li   $v0, 11
    syscall
    # based literal [FF:16] = 255
    li   $t1, 255
    # print (int)
    move $a0, $t1
    li   $v0, 1
    syscall
    li   $a0, 10
    li   $v0, 11
    syscall
    # based literal [1010:2] = 10
    li   $t2, 10
    # print (int)
    move $a0, $t2
    li   $v0, 1
    syscall
    li   $a0, 10
    li   $v0, 11
    syscall
    # print (str)
    la   $a0, str_0
    li   $v0, 4
    syscall
    li   $a0, 10
    li   $v0, 11
    syscall
    li   $v0, 10
    syscall
