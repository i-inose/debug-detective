from agent import detective

# 対話モードで起動
print("=" * 50)
print("  バグ捜査一課 -- AIデバッグ刑事（デカ）")
print("=" * 50)
print()
print("エラーログを貼り付けて Enter → 空行で Enter を押すと捜査開始。")
print("（終了するには exit と入力）")
print()

while True:
    print("-" * 50)
    print("【通報内容】")
    lines = []
    while True:
        line = input()
        if line == "":
            break
        lines.append(line)
    user_input = "\n".join(lines).strip()

    if not user_input:
        continue
    if user_input.lower() == "exit":
        print('デカ「...今日の捜査はここまでだ。また呼んでくれ。」')
        break

    print()
    response = detective(user_input)
    print()