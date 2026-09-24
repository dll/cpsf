# Windows 控制台默认是 GBK(936)，而本文件是 UTF-8：
# 先把代码页切到 65001，否则 make 打印的中文提示会显示成乱码。
ifeq ($(OS),Windows_NT)
$(shell cmd /c "chcp 65001 >nul 2>&1")
endif

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
