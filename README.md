# Smart-Joke-Deduplicator (智能段子去重工具)

-----

## 🇬🇧 English Version

### 🚀 Introduction

A high-performance, intelligent Python tool designed to deduplicate large text files (30,000+ lines) of social media "jokes" or "snippets." Unlike standard deduplicators, this tool understands the nuances of social media content.

**Born from a Collaboration:** This project was co-created by a human curator and **Google Gemini**, blending human intuition with AI's logical precision.

### ✨ Key Features

  * **Intelligent Similarity (95% Threshold):** Uses fuzzy matching to identify duplicates even if they have different punctuation, spaces, or user IDs.
  * **ID-Stripping Logic:** Automatically ignores headers like `@Username:` during comparison to find the core content.
  * **Bottom-Up Preservation:** Intelligently keeps the *latest* (most recent) version of a snippet while removing older duplicates.
  * **Comprehensive Logging:** Generates a detailed `dedup_log.txt` showing exactly what was deleted, where it was, and the full text of the duplicates.
  * **Safety First:** Automatic backup (`_bak`) creation before every run.

### 🛠️ How to Use

1.  Ensure you have **Python 3.x** installed.
2.  Place your text file (e.g., `jokes.txt`) in the same directory as `dedup.py`.
3.  Run the script:
    ```bash
    python dedup.py
    ```
4.  Check `dedup_log.txt` for the result report.

-----

## 🇨🇳 中文版

### 🚀 项目简介

这是一个专为处理海量（3万行+）微博、短视频段子设计的智能去重工具。它不仅能处理完全一致的文本，还能识别那些“换汤不换药”的重复内容。

**特别说明：** 本项目由人类作者提供创意与业务逻辑，由 **Google Gemini** 协助编写并深度优化算法。这是人机协作、共同进化的产物。

### ✨ 核心功能

  * **95% 智能相似度：** 采用模糊匹配算法。即使标点符号不同、空格多少不一，只要正文内容一致，就能精准识别。
  * **自动脱敏比对：** 在比对时会自动忽略开头的 `@用户名：` 等干扰项，直击段子灵魂。
  * **保留最新版本：** 采用“从下往上”扫描逻辑，保留文件最底部（通常是最新的）段子，删除上方陈旧的重复项。
  * **详尽日志：** 自动生成 `dedup_log.txt`，详细记录每个重复段子的位置、重复次数、删除行号以及完整原文。
  * **自动备份：** 每次运行前自动删除旧备份并建立新的 `_bak` 文件，确保数据万无一失。

### 🛠️ 使用方法

1.  确保电脑已安装 **Python 3.x**。
2.  将你的段子文件（如 `段子.txt`）放在代码同级目录下。
3.  在终端运行：
    ```bash
    python dedup.py
    ```
4.  完成后查看 `dedup_log.txt` 即可看到去重详情。

-----

### 🤝 Contributing / 贡献

Welcome to submit Issues or Pull Requests\! Let's make internet content cleaner together.

欢迎提交 Issue 或 Pull Request！让我们一起净化互联网内容。

-----
