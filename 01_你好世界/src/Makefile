# ============================================
# 第1阶段：你好世界 - Makefile
# ============================================
# 使用 make 命令编译
# 输出：hello.exe（Windows）/ hello（Linux）
# ============================================

CC = gcc
CFLAGS = -Wall -g
TARGET = hello

# 判断操作系统
ifeq ($(OS),Windows_NT)
	TARGET := $(TARGET).exe
	RM = del /Q
else
	RM = rm -f
endif

.PHONY: all clean run

all: $(TARGET)

$(TARGET): hello.c
	$(CC) $(CFLAGS) -o $@ $<

run: $(TARGET)
	./$(TARGET)

clean:
	$(RM) $(TARGET)
