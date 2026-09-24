# Windows 控制台默认是 GBK(936)，而本文件是 UTF-8：
# 先把代码页切到 65001，否则 make 打印的中文提示会显示成乱码。
ifeq ($(OS),Windows_NT)
$(shell cmd /c "chcp 65001 >nul 2>&1")
endif

# ============================================================
#  第5讲：指针 —— Makefile
# ============================================================
#  用法（Linux / macOS / Git Bash）：
#    make         编译，生成 pointer_atm（Windows 下为 .exe）
#    make run     编译并自动演示
#    make clean   清理产物
# ============================================================

CC      = gcc
CFLAGS  = -Wall -O2
TARGET  = pointer_atm
SRCS    = pointer_atm.c

ifeq ($(OS),Windows_NT)
TARGET := $(TARGET).exe
RM      = del /Q
else
RM      = rm -f
endif

all: $(TARGET)

$(TARGET): $(SRCS)
	$(CC) $(CFLAGS) -o $(TARGET) $(SRCS)
	@echo "已生成 $(TARGET)"

# 自动演示：1 查询 / 2 存款500 / 3 取款200 / 4 转账100 / 0 退出
run: $(TARGET)
	printf '1\n2\n500\n3\n200\n4\n100\n2002\n0\n' | ./$(TARGET)

clean:
	-$(RM) $(TARGET)

.PHONY: all run clean
