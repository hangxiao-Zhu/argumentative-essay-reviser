# 上海高考议论文批改与升格

面向已有中文议论文的 Agent Skill：检查审题、概念、论证和语言，保留成立的主线，提供关键修改对照及完整修订稿。

默认清晰思辨、适度文采，全文850—950汉字，不自动评分。支持文本、Word和手写稿；手写关键字不清时先确认。它是供模型执行的修改指导，不是训练后的独立评分模型。

## 使用

将 `skills/shanghai-essay-revise` 安装到客户端的 skills 目录，下一轮调用：

> 使用 $shanghai-essay-revise 修改这篇上海高考议论文。题目：…… 原文：……

入口及公开参考是自包含的，不依赖其他写作技能。没有个人配置也可以在对话中使用。

## 本地资料与保存

可以在安装目录内创建被Git忽略的 `private/profile.json`，以 `guidance` 指向私人方法索引、`output_dir` 指向已存在的本地Markdown保存目录；两者使用本机绝对路径。方法索引只路由与当前作文相关的资料。

公共仓库不包含训练原件、OCR、课程范文摘录、私人素材索引、学生原稿、批改记录或个人机器路径。不要把这些内容放入公开 skill/reference 文件。

## 检查

```text
python -m unittest discover -s tests -v
python scripts/audit_public.py
```

提交前逐项核对 `PUBLIC_FILES.txt`，仅暂存允许发布的文件，再运行审计。审计检查暂存内容，不是对所有隐私的自动识别保证，仍须人工审阅 diff。首次发布不携带训练数据历史。

行为测试见 `evals/scenarios.md`。测试成功不等于已证明高考提分；评分须有有效上海卷量表，不能用全国卷分数换算。

## 设计参考

参考 [Essay Writer & Editor](https://github.com/shimellism-eng/essay-writer-editor) 的分层修改与证据保真思路，本项目为独立编写的窄领域技能，未打包其代码或资料。私人课程内容仅在使用者本地读取，不随本项目发布。
