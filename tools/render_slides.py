# -*- coding: utf-8 -*-
"""
render_slides.py —— 把 pptx 渲染成 PNG（用本机 PowerPoint，所见即所得）

用法：
    python tools/render_slides.py <课件.pptx> <输出目录> [宽度]

说明：
    - 用 PowerPoint COM 导出，保证与真实放映一致（含字体、行距、自动收缩）
    - 输出 slide_01.png ... 顺序编号，供视频流水线直接使用

⚠️ 坑：连着渲染多讲时，上一实例 Quit 后立刻新建实例，
      会间歇性报 com_error -2146959355「服务器运行失败」（隔一个失败一个）。
      所以这里内置了重试：失败后等待若干秒再新建实例，最多 4 次
      （PPT 进程需要一点时间真正退出）。批量渲染务必用本脚本，
      不要把 DispatchEx 写进自己的 for 循环里。
"""
import glob
import os
import shutil
import sys
import time


def _render_once(ppt_path, out_dir, width):
    import pythoncom
    import win32com.client
    pythoncom.CoInitialize()
    ppt = win32com.client.DispatchEx('PowerPoint.Application')
    paths = []
    try:
        pres = ppt.Presentations.Open(ppt_path, WithWindow=False)
        n = pres.Slides.Count
        for i in range(1, n + 1):
            p = os.path.join(out_dir, 'slide_%02d.png' % i)
            # 16:9 -> 高 = 宽 * 9/16
            pres.Slides(i).Export(p, 'PNG', int(width), int(width * 9 / 16))
            paths.append(p)
        pres.Close()
    finally:
        try:
            ppt.Quit()
        except Exception:
            pass
    return paths


def render(ppt_path, out_dir, width=1920, tries=4):
    ppt_path = os.path.abspath(ppt_path)
    out_dir = os.path.abspath(out_dir)
    # 注意：沙箱会拦截 rmtree（SAFE_DELETE_FAIL_CLOSED），忽略即可，
    # 后面的 Export 会按同名覆盖旧图。
    if os.path.isdir(out_dir):
        shutil.rmtree(out_dir, ignore_errors=True)
    os.makedirs(out_dir, exist_ok=True)

    last = None
    for k in range(tries):
        if k:
            # PPT 实例退出需要时间，等 6~10 秒再试
            time.sleep(6 + 2 * k)
        try:
            paths = _render_once(ppt_path, out_dir, width)
            got = len(glob.glob(os.path.join(out_dir, 'slide_*.png')))
            if got == 0:
                raise RuntimeError('导出 0 张')
            print('已渲染 %d 张：%s' % (got, out_dir))
            return paths
        except Exception as e:
            last = e
            print('  [重试 %d/%d] %s' % (k + 1, tries, str(e)[:90]))
    raise SystemExit('渲染失败：%s' % last)


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)
    w = int(sys.argv[3]) if len(sys.argv) > 3 else 1920
    render(sys.argv[1], sys.argv[2], w)
