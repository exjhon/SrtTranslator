# SrtTranslator introduce|介绍
A simple offline *.srt translator using transformers models that helps you to translate subtitles.

简单的离线字幕翻译器，使用transformers模型，助你翻译字幕。

# Feature|功能

可选自主下载的模型

自动排除序号，时间戳和空行

保存为同目录下的*_translated.srt，或者勾选备份模式，保存为原文件名并备份原文件为*_bak.srt

以进度条显示翻译进度


# How to Use it|如何使用
Download the translation model that you need from here:https://huggingface.co/models?pipeline_tag=translation

在这里下载你需要的翻译模型：https://huggingface.co/models?pipeline_tag=translation


Put the downloaded model folder in \model. For example:\model\M2M100-ja-zh

把下载好的模型放在/model文件夹下。例如：\model\M2M100-ja-zh


Install requirements and run srt_translator.py. 

安装依赖并运行srt_translator.py。
