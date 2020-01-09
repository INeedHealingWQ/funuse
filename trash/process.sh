#!/bin/bash

arm-linux-gnueabi-gcc -c ./test10.c
arm-linux-gnueabi-gcc -c ./test20.c
arm-linux-gnueabi-objdump -D ./test10.o > ./test10.dump
arm-linux-gnueabi-objdump -D ./test20.o > ./test20.dump
arm-linux-gnueabi-ld -o ./test10.out ./test10.o
arm-linux-gnueabi-ld -o ./test20.out ./test20.o
arm-linux-gnueabi-objdump -D ./test10.out > ./test10.final.dump
arm-linux-gnueabi-objdump -D ./test20.out > ./test20.final.dump
