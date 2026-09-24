# Windows 控制台默认是 GBK(936)，而本文件是 UTF-8：
# 先把代码页切到 65001，否则 make 打印的中文提示会显示成乱码。
ifeq ($(OS),Windows_NT)
$(shell cmd /c "chcp 65001 >nul 2>&1")
endif

# ============================================================
# 第11讲：运行时加载 - Linux 构建脚本
# ============================================================
#
#  产出：
#    plugins/deposit_plugin.so  存款插件
#    plugins/withdraw_plugin.so 取款插件
#    plugins/query_plugin.so    查询插件
#    plugins/broken_plugin.so   反例（缺少约定符号）
#    host                       宿主程序
#
#  关键点：
#    -fPIC          生成位置无关代码（动态库必须加）
#    -shared        生成动态库（.so）
#    -ldl           链接 libdl，才有 dlopen/dlsym/dlclose
# ============================================================

CC      = gcc
CFLAGS  = -Wall -Wextra -g
LDFLAGS = -ldl

PLUGIN_DIR = plugins

PLUGINS = $(PLUGIN_DIR)/deposit_plugin.so \
          $(PLUGIN_DIR)/withdraw_plugin.so \
          $(PLUGIN_DIR)/query_plugin.so \
          $(PLUGIN_DIR)/broken_plugin.so

TARGET = host

# 默认目标：先建目录，再编插件，最后编宿主
all: $(PLUGIN_DIR) $(PLUGINS) $(TARGET)
	@echo "============================================"
	@echo "构建完成！运行 ./$(TARGET) 体验运行时加载"
	@echo "============================================"

# ---- 目录准备（order-only 依赖，目录已存在时不重复建）----
$(PLUGIN_DIR):
	mkdir -p $(PLUGIN_DIR)

# ---- 插件：源文件 -> plugins/xxx.so ----
# -fPIC 位置无关代码；-shared 生成动态库
$(PLUGIN_DIR)/%.so: %.c plugin_api.h | $(PLUGIN_DIR)
	$(CC) $(CFLAGS) -fPIC -shared -o $@ $<

# ---- 宿主程序：需要 -ldl 才能用 dlopen/dlsym/dlclose ----
$(TARGET): host.c dynlib.h plugin_api.h
	$(CC) $(CFLAGS) -o $(TARGET) host.c $(LDFLAGS)

# ---- 查看插件导出的符号（对比：应该能看到 plugin_name / plugin_execute）----
inspect: $(PLUGINS)
	@echo "=== deposit_plugin.so 导出的符号 ==="
	nm -D --defined-only $(PLUGIN_DIR)/deposit_plugin.so | grep plugin
	@echo "=== broken_plugin.so 导出的符号（故意少了 plugin_execute）==="
	nm -D --defined-only $(PLUGIN_DIR)/broken_plugin.so | grep plugin

# ---- 运行 ----
run: all
	./$(TARGET)

clean:
	-rm -f $(TARGET) $(PLUGINS)
	-rm -f *.o
	@echo "清理完成"

.PHONY: all run inspect clean
