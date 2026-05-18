.data
    str_0: .asciiz "hola mundo"

.text
.globl main
main:
    # print (str)
    la   $a0, str_0
    li   $v0, 4
    syscall
    li   $a0, 10
    li   $v0, 11
    syscall
    li   $v0, 10
    syscall
