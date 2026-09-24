# Windows 控制台默认是 GBK(936)，而本文件是 UTF-8：
# 先把代码页切到 65001，否则 make 打印的中文提示会显示成乱码。
ifeq ($(OS),Windows_NT)
$(shell cmd /c "chcp 65001 >nul 2>&1")
endif

# ============================================================
#  第12讲：接口抽象 —— Makefile
# ============================================================
#  用法（Linux / macOS / Git Bash）：
#    make         编译，生成 plugin_atm（Windows 下为 .exe）
#    make run     编译并运行演示（无需输入）
#    make clean   清理产物
# ============================================================

CC      = gcc
CFLAGS  = -Wall -O2
TARGET  = plugin_atm
SRCS    = plugin_atm.c
HEADERS = plugin.h console_utf8.h

ifeq ($(OS),Windows_NT)
TARGET := $(TARGET).exe
RM      = del /Q
else
RM      = rm -f
endif

all: $(TARGET)

$(TARGET): $(SRCS) $(HEADERS)
	$(CC) $(CFLAGS) -o $(TARGET) $(SRCS)
	@echo "已生成 $(TARGET)"

# 本讲无需交互输入：注册插件 → 目录扫描 → 遍历 → 多态调用 → 清理
run: $(TARGET)
	./$(TARGET)

clean:
	-$(RM) $(TARGET)

.PHONY: all run clean
