# automatically-download-TV-series

`南工在线（电视剧/番）自动下载打包脚本`

本工具使用到了`requests`，`tqdm`，`Pillow`库，需要安装的依赖已经放在了 requirements 中

只需要在终端运行

```
pip install -r requirements.txt
```

<img src="image\show_big.png" alt="UI" width="500"/>

<img src="image\show_small.png" alt="UI" width="500"/>

输入视频集数，链接，以及视频名即可，会自动打包存储在目录下文件夹内。

最下方为下载实时显示进度条。

并且加入了彩蛋，全屏有惊喜，每下载完成一集后会切换背景图。

## 补充内容

由于 UI 界面目前还处于测试阶段，如果希望有更稳定的使用体验，可以使用`all.py`文件。

需要自行输入集数，链接，视频名，最后输入`yes/no`选择是否需要压缩包。

如果需要压缩文件不能使用 UI 界面，还没有增加该功能。

## 更新 ing
