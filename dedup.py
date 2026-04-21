import difflib
import os
import re
import shutil
import time


def clean_text_for_comparison(text):
    """
    清洗文本，用于底层比对（不影响原文显示）
    1. 去除开头的 @用户: 或 @用户：
    2. 去除所有空白字符（空格、换行等）
    3. 去除常见标点符号
    """
    # 尝试匹配并去除开头的 @xxx: 或 @xxx：
    cleaned = re.sub(r"^@.*?[：:]", "", text, flags=re.MULTILINE).strip()
    # 去除所有非字母数字和汉字的字符（保留核心纯文本）
    cleaned = re.sub(r"[^\w\u4e00-\u9fa5]", "", cleaned)
    return cleaned


def is_similar(text1, text2, threshold=0.95):
    """判断两段纯文本是否达到相似度阈值"""
    # 长度过滤：如果两段文字长度差异超过 10%，直接判定为不相似，跳过复杂计算
    len1, len2 = len(text1), len(text2)
    if len1 == 0 or len2 == 0:
        return False

    if abs(len1 - len2) / max(len1, len2) > (1 - threshold):
        return False

    # 计算文本相似度
    ratio = difflib.SequenceMatcher(None, text1, text2).quick_ratio()
    return ratio >= threshold


def deduplicate_jokes_smart(file_path):
    backup_path = file_path + "_bak"
    log_path = "dedup_log.txt"

    if not os.path.exists(file_path):
        print(f"错误：找不到文件 {file_path}")
        return

    print("正在备份原文件...")
    if os.path.exists(backup_path):
        os.remove(backup_path)
    shutil.copy(file_path, backup_path)

    print("正在读取并解析段子...")
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    blocks = []
    current_block_lines = []
    start_line = 1

    for i, line in enumerate(lines):
        if line.strip():
            if not current_block_lines:
                start_line = i + 1
            current_block_lines.append(line)
        else:
            if current_block_lines:
                content = "".join(current_block_lines)
                blocks.append(
                    {
                        "content": content,
                        "clean_key": clean_text_for_comparison(content),
                        "start_line": start_line,
                        "end_line": i,
                        "original_index": len(blocks),
                    }
                )
                current_block_lines = []

    if current_block_lines:
        content = "".join(current_block_lines)
        blocks.append(
            {
                "content": content,
                "clean_key": clean_text_for_comparison(content),
                "start_line": start_line,
                "end_line": len(lines),
                "original_index": len(blocks),
            }
        )

    print(
        f"共提取到 {len(blocks)} 个段子块。开始进行高精度相似度比对 (这可能需要几十秒)..."
    )
    start_time = time.time()

    # 按从下往上的顺序处理（保留最底部的）
    # 使用 reverse 遍历，越先加入 unique_groups 的段子越靠下
    reversed_blocks = list(reversed(blocks))
    unique_groups = []  # 存储结构: [{'kept': block, 'deleted': [block1, block2]}]

    for i, block in enumerate(reversed_blocks):
        found_group = False
        current_clean = block["clean_key"]

        # 和已存在的不重复组进行比对
        for group in unique_groups:
            kept_clean = group["kept"]["clean_key"]

            # 优先尝试绝对相等（极速）
            if current_clean == kept_clean:
                group["deleted"].append(block)
                found_group = True
                break

            # 如果不绝对相等，再尝试相似度计算
            if is_similar(current_clean, kept_clean, threshold=0.95):
                group["deleted"].append(block)
                found_group = True
                break

        if not found_group:
            unique_groups.append({"kept": block, "deleted": []})

        # 打印进度条
        if i % 500 == 0 and i > 0:
            print(f"已处理 {i} 个段子...")

    # 准备写入的数据
    to_keep = [group["kept"] for group in unique_groups]
    to_keep.sort(key=lambda x: x["original_index"])  # 还原原有顺序

    log_entries = []
    total_deleted_count = 0

    for group in unique_groups:
        if group["deleted"]:
            total_deleted_count += len(group["deleted"])
            kept = group["kept"]
            dels = group["deleted"]

            total_times = len(dels) + 1
            kept_position = f"行 {kept['start_line']}-{kept['end_line']}"
            deleted_positions = ", ".join(
                [f"行 {b['start_line']}-{b['end_line']}" for b in dels]
            )

            log_entries.append(
                f"【发现重复段子】 重复 {total_times} 次\n"
                f"-> [保留] (最底部) {kept_position}:\n{kept['content'].strip()}\n\n"
                f"-> [删除] 位置: {deleted_positions}\n"
            )

    print("正在写入文件...")
    with open(file_path, "w", encoding="utf-8") as f:
        for block in to_keep:
            f.write(block["content"])
            f.write("\n")

    with open(log_path, "w", encoding="utf-8") as f:
        f.write("=== 相似度去重任务报告 ===\n")
        f.write(f"耗时: {time.time() - start_time:.2f} 秒\n")
        f.write(f"原始段子总数: {len(blocks)} 个\n")
        f.write(f"保留独立段子: {len(to_keep)} 个\n")
        f.write(f"累计删除重复: {total_deleted_count} 处\n")
        f.write("=" * 50 + "\n\n")

        for entry in log_entries:
            f.write(entry)
            f.write("-" * 50 + "\n\n")

    print(f"处理完成！耗时: {time.time() - start_time:.2f} 秒")
    print(f"详细情况已保存至: {log_path}")


if __name__ == "__main__":
    target_file = "jokes.txt"  # 修改为你的实际文件名
    deduplicate_jokes_smart(target_file)
