/*
 * ============================================================
 *  第5讲：指针 —— 指针版 ATM 程序
 *  打通任督二脉：从"全局变量"到"指针传递"
 * ============================================================
 *
 *  目标：用指针替代全局变量，通过指针参数让函数修改 main 中的余额
 *
 *  第3-4讲的痛点：
 *    1. 余额用全局变量 g_balance 管理，所有函数都能随便改
 *    2. 谁改的、在哪改的、改对没有——全靠人肉排查
 *    3. 全局变量像"公共牧场"，谁都能来踩一脚，改乱了找谁？
 *    4. 带全局变量的函数不好复用——搬到别的程序还得搬变量
 *
 *  第5讲的解法：指针传参
 *    1. 余额定义在 main 中（局部变量），不再全局可见
 *    2. 哪个函数需要操作余额，就把余额的地址传给它
 *    3. 函数通过指针（地址）修改余额，修改路径清晰可追溯
 *    4. 函数不依赖全局变量，搬到哪都能用
 *
 *  核心知识点演示：
 *    - 取地址 &：获取变量的内存地址
 *    - 解引用 *：通过地址访问/修改变量的值
 *    - 指针作为函数参数：让函数能修改调用者的变量
 *    - NULL 检查：指针使用前必须检查是否为空
 */

#include <stdio.h>

/*
 * ============================================================
 *  函数声明（函数原型）
 * ============================================================
 *
 * 对比第3讲：函数参数变了！
 *
 * 第3讲（全局变量版）：
 *   void query_balance(void);       // 直接访问 g_balance
 *   void deposit(void);             // 直接修改 g_balance
 *   void withdraw(void);            // 直接修改 g_balance
 *
 * 第5讲（指针版）：
 *   void query_balance(double* p);  // 传余额的地址进来
 *   void deposit(double* p);        // 通过地址修改余额
 *   void withdraw(double* p);       // 通过地址修改余额
 *
 * 区别在哪？
 *   全局变量版：函数"偷偷"访问全局数据，调用者看不到依赖关系
 *   指针版：函数的参数列表明确声明"我需要操作余额"，一目了然
 *
 * 这就是"显式依赖优于隐式依赖"——架构设计的基本原则
 */

void show_welcome(void);                         // 显示欢迎界面（不需要操作余额，无指针参数）
void show_menu(void);                            // 显示主菜单（不需要操作余额，无指针参数）
void query_balance(const double* p_balance);     // 查询余额（只读，用 const 保护）
void deposit(double* p_balance);                 // 存款（需要修改余额，传指针）
void withdraw(double* p_balance);                // 取款（需要修改余额，传指针）
void transfer(double* p_balance);                // 转账（需要修改余额，传指针）
void print_success(const char* op, double amount, const double* p_balance);  // 打印成功信息
void print_error(const char* msg);               // 打印错误信息

/*
 * ============================================================
 *  主函数
 * ============================================================
 *
 * 关键变化：余额定义在 main 里，是局部变量！
 *
 * 第3讲：double g_balance = 1000.0;  // 全局变量，所有人可见
 * 第5讲：double balance = 1000.0;    // 局部变量，只在 main 里可见
 *
 * 好处：
 *   1. 余额的作用域缩小到 main 函数内，不会被意外修改
 *   2. 只有 main 决定把余额的地址传给谁——控制权在 main 手里
 *   3. 函数想改余额？必须通过参数明确声明，不能偷偷改
 *
 * 这就像保险箱的钥匙——
 *   全局变量：钥匙挂在走廊墙上，谁都能拿
 *   指针传参：钥匙在 main 手里，谁要用找 main 借
 */

int main(void)
{
    int choice = 0;
    int running = 1;

    /*
     * 余额定义在这里 —— 局部变量
     * 没有了 g_ 前缀，因为它不再是全局变量
     */
    double balance = 1000.0;   // 初始余额 1000 元

    /* 显示欢迎界面 */
    show_welcome();

    /* 主循环 */
    while (running)
    {
        show_menu();

        printf("请输入您的选择：");
        scanf("%d", &choice);
        printf("\n");

        /*
         * 根据选择调用不同的函数
         *
         * 注意：需要操作余额的函数，我们传 &balance（余额的地址）
         * 不需要操作余额的函数（如 show_menu），不传地址
         *
         * &balance 的含义：
         *   & 是"取地址"运算符
         *   &balance 得到 balance 变量在内存中的地址
         *   这个地址就是传给函数的"钥匙"
         */
        switch (choice)
        {
            case 1:
                query_balance(&balance);   /* 传余额地址（只读） */
                break;
            case 2:
                deposit(&balance);         /* 传余额地址（可修改） */
                break;
            case 3:
                withdraw(&balance);        /* 传余额地址（可修改） */
                break;
            case 4:
                transfer(&balance);        /* 传余额地址（可修改） */
                break;
            case 0:
                printf("感谢使用 CCIT ATM 系统，再见！\n");
                running = 0;
                break;
            default:
                print_error("无效的选择，请重新输入！");
                break;
        }
    }

    return 0;
}

/* ============================================================
 *  函数定义
 * ============================================================ */

/*
 * ---------- show_welcome：显示欢迎界面 ----------
 *
 * 这个函数不需要操作余额，所以没有指针参数
 * 和第3讲完全一样
 */

void show_welcome(void)
{
    printf("========================================\n");
    printf("       欢迎使用 CCIT ATM 系统\n");
    printf("       （指针版 · 无全局变量）\n");
    printf("========================================\n");
    printf("\n");
}

/*
 * ---------- show_menu：显示主菜单 ----------
 *
 * 同样不需要操作余额，没有指针参数
 */

void show_menu(void)
{
    printf("\n-------- 主菜单 --------\n");
    printf("  1. 查询余额\n");
    printf("  2. 存款\n");
    printf("  3. 取款\n");
    printf("  4. 转账\n");
    printf("  0. 退出\n");
    printf("------------------------\n");
}

/*
 * ---------- query_balance：查询余额 ----------
 *
 * 第3讲（全局变量版）：
 *   void query_balance(void) {
 *       printf("余额：%.2f\n", g_balance);  // 直接读全局变量
 *   }
 *
 * 第5讲（指针版）：
 *   void query_balance(const double* p_balance) {
 *       printf("余额：%.2f\n", *p_balance);  // 通过指针读
 *   }
 *
 * 参数：const double* p_balance
 *   - double* 表示这是一个"指向 double 的指针"
 *   - const 表示"只读"——函数承诺不修改余额，只读取
 *   - p_balance 是参数名，p_ 前缀表示 pointer（指针）
 *
 * *p_balance 是什么？
 *   - * 是"解引用"运算符
 *   - *p_balance 的意思是"取出 p_balance 指向的那个变量的值"
 *   - 如果 p_balance 存的是 balance 的地址，那 *p_balance 就是 balance 的值
 *
 * 比喻：
 *   p_balance 是一张纸条，上面写着"钱在保险箱 A123"
 *   *p_balance 就是"按照纸条去找 A123，打开看里面的钱"
 */

void query_balance(const double* p_balance)
{
    /*
     * 指针使用前必须检查 NULL！
     *
     * NULL 表示"空指针"——指针不指向任何有效地址
     * 如果不检查就解引用 NULL 指针，程序会崩溃（段错误）
     *
     * 这是指针编程最重要的好习惯：
     *   "永远在使用指针前检查它是否为 NULL"
     *
     * 好比开门前先看看钥匙对不对——
     *   拿着一把空钥匙硬捅，门不但打不开，锁还会坏
     */
    if (p_balance == NULL)
    {
        print_error("内部错误：余额指针为空！");
        return;
    }

    printf("【查询余额】\n");
    printf("您当前的账户余额为：%.2f 元\n", *p_balance);  /* 解引用：取值 */
}

/*
 * ---------- deposit：存款 ----------
 *
 * 第3讲（全局变量版）：
 *   void deposit(void) {
 *       g_balance = g_balance + amount;  // 直接改全局变量
 *   }
 *
 * 第5讲（指针版）：
 *   void deposit(double* p_balance) {
 *       *p_balance = *p_balance + amount;  // 通过指针改
 *   }
 *
 * 参数：double* p_balance
 *   - 注意这里没有 const！因为存款需要修改余额
 *   - 没有 const 意味着"函数可以修改 p_balance 指向的变量"
 *
 * *p_balance = *p_balance + amount 的执行过程：
 *   1. 右边 *p_balance：取出 p_balance 指向的变量（balance）的当前值
 *   2. 加上 amount
 *   3. 左边 *p_balance = ...：把结果写回 p_balance 指向的变量（balance）
 *
 * 效果：balance 的值被修改了！
 *   虽然 deposit 函数看不到 balance 这个名字，
 *   但它通过地址找到了 balance，并修改了它。
 *
 * 这就是指针的魔力：
 *   "不需要知道你的名字，只要知道你的地址，就能找到你、改变你"
 */

void deposit(double* p_balance)
{
    double amount = 0.0;

    /* 指针检查：使用前先确认指针有效 */
    if (p_balance == NULL)
    {
        print_error("内部错误：余额指针为空！");
        return;
    }

    printf("【存款业务】\n");
    printf("请输入存款金额：");
    scanf("%lf", &amount);

    if (amount <= 0)
    {
        print_error("存款金额必须大于0！");
        return;
    }

    /*
     * 通过指针修改余额
     *
     * *p_balance 就是 balance（通过地址访问）
     * 所以这行代码等价于 balance = balance + amount
     * 但 deposit 函数并不知道 balance 这个名字，它只知道地址
     */
    *p_balance = *p_balance + amount;

    print_success("存入", amount, p_balance);
}

/*
 * ---------- withdraw：取款 ----------
 *
 * 取款逻辑和存款类似，多了一个余额检查
 *
 * 对比第3讲：
 *   if (amount > g_balance)        → 直接用全局变量
 *   if (amount > *p_balance)       → 通过指针读取
 */

void withdraw(double* p_balance)
{
    double amount = 0.0;

    if (p_balance == NULL)
    {
        print_error("内部错误：余额指针为空！");
        return;
    }

    printf("【取款业务】\n");
    printf("请输入取款金额：");
    scanf("%lf", &amount);

    if (amount <= 0)
    {
        print_error("取款金额必须大于0！");
        return;
    }

    /* 通过指针读取余额，判断是否充足 */
    if (amount > *p_balance)
    {
        print_error("余额不足！");
        return;
    }

    /* 通过指针修改余额 */
    *p_balance = *p_balance - amount;

    print_success("取出", amount, p_balance);
}

/*
 * ---------- transfer：转账 ----------
 *
 * 转账逻辑：先检查金额，再输入对方账号，最后通过指针扣款
 */

void transfer(double* p_balance)
{
    double amount = 0.0;
    int target_account = 0;

    if (p_balance == NULL)
    {
        print_error("内部错误：余额指针为空！");
        return;
    }

    printf("【转账业务】\n");
    printf("请输入转账金额：");
    scanf("%lf", &amount);

    if (amount <= 0)
    {
        print_error("转账金额必须大于0！");
        return;
    }

    if (amount > *p_balance)
    {
        print_error("余额不足，无法转账！");
        return;
    }

    printf("请输入对方账号：");
    scanf("%d", &target_account);

    /* 通过指针修改余额 */
    *p_balance = *p_balance - amount;

    printf("✅ 转账成功！向账号 %d 转出 %.2f 元\n", target_account, amount);
    printf("当前余额：%.2f 元\n", *p_balance);
}

/*
 * ---------- print_success：打印成功信息 ----------
 *
 * 第3讲：
 *   void print_success(char* op, double amount) {
 *       printf("余额：%.2f\n", g_balance);  // 读全局变量
 *   }
 *
 * 第5讲：
 *   void print_success(const char* op, double amount, const double* p_balance) {
 *       printf("余额：%.2f\n", *p_balance);  // 通过指针读
 *   }
 *
 * 注意：p_balance 用了 const，因为打印信息只需要读取余额，不需要修改
 * 这是好习惯：只读的指针参数加 const，防止函数内意外修改
 */

void print_success(const char* op, double amount, const double* p_balance)
{
    if (p_balance == NULL) return;  /* 防御性检查 */

    printf("✅ 操作成功！%s %.2f 元\n", op, amount);
    printf("当前余额：%.2f 元\n", *p_balance);
}

/*
 * ---------- print_error：打印错误信息 ----------
 *
 * 这个函数不涉及余额操作，和第3讲一样
 */

void print_error(const char* msg)
{
    printf("❌ %s\n", msg);
}

/*
 * ============================================================
 *  对比第3讲，我们收获了什么？
 * ============================================================
 *
 *  ✅ 1. 消灭了全局变量
 *     原来：g_balance 是全局变量，谁都能改
 *     现在：balance 是 main 的局部变量，只有 main 能直接访问
 *     好处：修改路径清晰，出了问题好排查
 *
 *  ✅ 2. 显式依赖
 *     原来：函数参数列表是 void，看不出它用了什么数据
 *     现在：函数参数列表写着 double* p_balance，一看就知道要操作余额
 *     好处：函数的依赖一目了然，接口即文档
 *
 *  ✅ 3. 更好的可复用性
 *     原来：带全局变量的函数搬到别的程序，还得搬全局变量
 *     现在：函数只依赖参数，搬到哪都能用——只要传个地址进来
 *
 *  ✅ 4. const 保护
 *     原来：无法限制函数只读不写
 *     现在：query_balance 用 const double*，编译器保证不修改
 *     好处：编译时就能发现"不该写却写了"的错误
 *
 *  ✅ 5. NULL 检查的防御性编程
 *     原来：全局变量不会为 NULL，但也没法防御
 *     现在：每个函数都检查指针是否为 NULL
 *     好处：程序更健壮，不会因为空指针而崩溃
 *
 * ============================================================
 *  思考：还有问题吗？
 * ============================================================
 *
 *  指针解决了全局变量问题，但新的问题也来了：
 *
 *  ❓ 1. 参数越来越多
 *     现在只传了余额一个指针。如果要操作余额、密码、交易记录...
 *     函数参数列表会越来越长。怎么办？
 *     （第7讲：结构体——把相关数据打包在一起）
 *
 *  ❓ 2. 指针是危险的
 *     指针指错了地方，程序就崩了。指针用完了不释放，内存就漏了。
 *     （后续：动态内存管理、内存安全）
 *
 *  ❓ 3. 功能扩展还是要改 switch
 *     加一个功能还是要在 switch 里加 case。
 *     能不能新增功能不改主程序？
 *     （第12-13讲：函数指针 + 插件框架——这才是系列的终极目标！）
 *
 *  💡 函数指针是通往插件框架的钥匙！
 *     今天学的是数据指针（指向变量的地址）
 *     后面要学的是函数指针（指向函数的地址）
 *     函数指针让我们能"把函数当参数传"——这是插件框架的基础
 *
 * ============================================================
 */
