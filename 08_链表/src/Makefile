# Windows 控制台默认是 GBK(936)，而本文件是 UTF-8：
# 先把代码页切到 65001，否则 make 打印的中文提示会显示成乱码。
ifeq ($(OS),Windows_NT)
$(shell cmd /c "chcp 65001 >nul 2>&1")
endif

# ============================================================
#  第8讲：链表 —— Makefile
# ============================================================
#  用法（Linux / macOS / Git Bash）：
#    make         编译，生成 linked_atm（Windows 下为 .exe）
#    make run     编译并自动演示（先选账户 1001）
#    make clean   清理产物
# ============================================================

CC      = gcc
CFLAGS  = -Wall -O2
TARGET  = linked_atm
SRCS    = linked_atm.c

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

# 自动演示：账户1001 / 1 查询 / 2 存款500 / 3 取款200 / 5 流水 / 7 链表管理 / 0 退出
run: $(TARGET)
	printf '1001\n1\n2\n500\n3\n200\n5\n7\n0\n' | ./$(TARGET)

clean:
	-$(RM) $(TARGET)

.PHONY: all run clean
