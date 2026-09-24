# Windows 控制台默认是 GBK(936)，而本文件是 UTF-8：
# 先把代码页切到 65001，否则 make 打印的中文提示会显示成乱码。
ifeq ($(OS),Windows_NT)
$(shell cmd /c "chcp 65001 >nul 2>&1")
endif

# ============================================================
#  第4讲：多文件编程 —— Makefile
# ============================================================
#  用法（Linux / macOS / Git Bash）：
#    make         编译 4 个 .c 并链接成 atm_multi
#    make run     编译并自动演示
#    make clean   清理产物
#   Windows 的 cmd 里请用 build.bat
# ============================================================
#  本讲要点：
#    .h 放声明，.c 放实现；每个 .c 单独编译成 .o，最后由链接器拼起来。
#    改一个文件，只需要重新编译那一个 —— 这就是分文件最直接的好处。
# ============================================================

CC      = gcc
CFLAGS  = -Wall -O2
TARGET  = atm_multi
SRCS    = main.c menu.c account.c utils.c
OBJS    = $(SRCS:.c=.o)
HEADERS = menu.h account.h utils.h console_utf8.h

ifeq ($(OS),Windows_NT)
TARGET := $(TARGET).exe
RM      = del /Q
else
RM      = rm -f
endif

all: $(TARGET)

# 链接：把 4 个 .o 拼成一个可执行文件
$(TARGET): $(OBJS)
	$(CC) $(CFLAGS) -o $(TARGET) $(OBJS)

# 编译：每个 .c 各自为战，头文件变了才需要重编
%.o: %.c $(HEADERS)
	$(CC) $(CFLAGS) -c $< -o $@

# 自动演示：1 查询 / 2 存款500 / 3 取款200 / 4 转账100 / 0 退出
run: $(TARGET)
	printf '1\n2\n500\n3\n200\n4\n100\n2002\n0\n' | ./$(TARGET)

clean:
	-$(RM) $(OBJS) $(TARGET)

.PHONY: all run clean
