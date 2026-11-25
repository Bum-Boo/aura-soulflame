# Aura Soulflame

[English](../README.md) · [한국어](README.ko.md) · **简体中文** · [日本語](README.ja.md)

以深梅紫色为底色、粉色为选中高亮、薄荷绿为火焰点缀的桌面主题。可以按需安装 Plasma 效果和 Kitty 配色，也可以导入自己的壁纸、光标和 Codex 宠物。

![登录后，Plasma 启动画面先显示中央的薄荷绿火焰，再依次点亮周围的小火焰](media/splash.gif)

**启动画面**（`plasma-splash`）会在登录后、Plasma 正在启动时播放。[查看静态预览](splash.png)

## 各个组件有什么用？

### KDE Plasma 6

| 系统配色 | 夜间锁屏壁纸 |
| --- | --- |
| <img src="media/colors.png" width="380" alt="Plasma 配色设置中的 Aura Soulflame，采用梅紫色背景和粉色选中高亮"> | <img src="media/night.png" width="380" alt="梅紫色渐变背景右侧有一簇薄荷绿火焰的锁屏壁纸"> |
| `plasma-colors` 设置窗口、文字、焦点和选区的颜色。在系统设置的**颜色**中选择 **Aura Soulflame (Portable)**。 | `plasma-lock` 添加带火焰的锁屏壁纸。打开**锁屏 → 外观 → 壁纸类型**，选择 **Aura Soulflame Night**。 |

| 漂浮火星 | 面板部件 |
| --- | --- |
| <img src="media/drift.gif" width="380" alt="薄荷绿和橙色的小火星沿着深色壁纸两边缓缓升起"> | <img src="media/panel.gif" width="258" alt="点击后会变亮的薄荷绿火焰面板部件"> |
| `plasma-drift` 让火星在渐变背景或自选图片上漂浮。在桌面或锁屏的壁纸设置中选择 **Aura Soulflame Drift**。也可以在壁纸设置里关闭动画。 | `plasma-panel` 可以在面板或桌面放置一簇小火焰。在**编辑模式 → 添加部件**中选择 **Aura Soulflame Panel**，点击火焰即可点亮它。 |

在系统设置的**启动画面**中选择 **Aura Soulflame Splash** 即可启用登录动画。

### Kitty 终端

![Kitty 中的梅紫色背景、薄荷绿光标、粉色高亮文字和两行 ANSI 色板](media/kitty.png)

`kitty` 提供背景、文字、光标、选区、标签页和 16 色 ANSI 配色。先用 `kitty --config <aura-soulflame.conf 的路径>` 在新窗口里预览。要长期使用，在 `kitty.conf` 的其他配色预设后加入 `include aura-soulflame.conf`。如果 Kitty 使用其他配置目录，安装时将 `KITTY_CONFIG_DIRECTORY` 指向该目录。

### 导入自己的素材

| 组件 | 需要准备的文件 | 应用位置 |
| --- | --- | --- |
| `cursor` | 含 `index.theme` 和 `cursors/` 的 Xcursor 主题目录 | Linux 桌面环境或合成器的光标设置 |
| `wallpapers` | PNG、JPEG 或 WebP 壁纸 | 操作系统的壁纸选择器 |
| `codex-pet` | `pet.json` 及其中引用的精灵图表 | Codex 宠物选择器。使用兼容终端时，执行 `/pets` 后按清单中的 ID 搜索。 |
| Plasma 角色图 | 对应组件所需姿势的透明 PNG | 在启动画面、夜间壁纸或面板中替换默认火焰 |

[素材目录格式](assets.md)列出了文件名和 `--assets` 用法。要在其他终端或桌面环境中使用配色，可以参考[共享色板](../resources/palette.json)中的颜色用途和 16 色 ANSI 色值，填入目标应用的主题配置。

## 安装并应用

在仓库根目录使用 **Python 3.9 或更新版本**运行命令。下面的 Kitty 示例适用于 Linux 和 macOS。Plasma 组件需要 Linux 上的 KDE Plasma 6。在 Windows 上导入壁纸或 Codex 宠物时，使用 `py -3 aura.py`。

```sh
python3 aura.py list
python3 aura.py plan --modules kitty
python3 aura.py install --modules kitty
python3 aura.py status --modules kitty
```

在 Linux 上同时安装 Plasma 配色和启动画面时，把相同流程中的模块改为 `--modules plasma-colors plasma-splash`。先用 `plan` 检查实际安装路径，安装后再按上表中的方法，在对应应用里启用组件。

恢复时，先切回原主题或移除 Kitty 中的 `include` 行，再对已安装的模块运行 `python3 aura.py uninstall --modules kitty`。安装后修改过的文件会标记为 `modified` 并保留。

## 让 AI 助手帮忙应用

> 请阅读 `AGENTS.md`，识别我的操作系统、桌面环境和目标应用。先展示我选定的 Aura Soulflame 组件的安装计划，再保留现有设置并应用它们。请在应用中验证效果，并说明如何恢复。可选素材包的路径是 `<路径>`。

[AI 应用指南](apply-with-ai.md) · [组件清单](../modules.json) · [素材来源与致谢](credits.md)

预览是在隔离的 Linux 环境中实际运行 KDE Plasma 6 和 Kitty 后录制的。使用 `python3 -m unittest discover -s tests -v` 可以检查安装工具的行为。
