# Windows 控制台默认是 GBK(936)，而本文件是 UTF-8：
# 先把代码页切到 65001，否则 make 打印的中文提示会显示成乱码。
ifeq ($(OS),Windows_NT)
$(shell cmd /c "chcp 65001 >nul 2>&1")
endif

# ============================================================
#  第14讲：完整项目与总结展望
#  Makefile —— Linux / macOS 构建脚本
# ============================================================
#  与 Windows 的 build.bat 一一对应，只是平台细节不同：
#    · 共享库后缀   .so       （Windows 是 .dll）
#    · 位置无关代码  -fPIC     （Windows 不需要）
#    · 运行时加载    -ldl      （Windows 由 kernel32 提供）
#    · 库查找路径    -Wl,-rpath,'$$ORIGIN'（让程序在自身目录找 .so）
#
#  用法：
#    make          # 构建 atmcore 共享库 + 插件 + 主程序
#    make run      # 运行主程序
#    make clean    # 清理产物
# ============================================================

CC      := gcc
CFLAGS  := -Wall -O2 -fPIC
LDLIBS  := -ldl
RPATH   := -Wl,-rpath,'$$ORIGIN'

CORE_SRC     := account.c transaction.c
PLUGIN_NAMES := deposit withdraw query transfer
PLUGIN_SRC   := $(addprefix plugins/,$(addsuffix _plugin.c,$(PLUGIN_NAMES)))
PLUGIN_SOS   := $(addprefix plugins/,$(addsuffix _plugin.so,$(PLUGIN_NAMES)))

APP         := atm_framework
CORE_LIB    := libatmcore.so

.PHONY: all plugins run clean

all: $(CORE_LIB) plugins $(APP)

# ---- 共享账务核心（主程序与所有插件共享它的数据）----
$(CORE_LIB): $(CORE_SRC) account.h transaction.h
	$(CC) $(CFLAGS) -shared -o $@ $(CORE_SRC) -DATMCORE_BUILD

# ---- 四个插件共享库，输出到 plugins/ ----
plugins: $(CORE_LIB)
	@mkdir -p plugins
	@for p in $(PLUGIN_NAMES); do \
		echo "  编译 plugins/$$p_plugin.so ..."; \
		$(CC) $(CFLAGS) -shared -DPLUGIN_DLL -o plugins/$$p_plugin.so \
			plugins/$$p_plugin.c -I. -Iplugins -L. -latmcore $(RPATH) || exit 1; \
	done

# ---- 主程序 ----
$(APP): main.c framework.c dynamic_loader.c $(PLUGIN_SRC) $(CORE_LIB)
	$(CC) $(CFLAGS) -o $@ main.c framework.c dynamic_loader.c $(PLUGIN_SRC) \
		-I. -Iplugins -L. -latmcore $(RPATH) $(LDLIBS)

run: all
	./$(APP)

clean:
	rm -f $(APP) $(CORE_LIB) libatmcore.a *.o
	rm -rf plugins/*.so
