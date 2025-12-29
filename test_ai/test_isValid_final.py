# -*- coding: utf-8 -*-
"""
测试简化后的 isValid 函数
"""

import sys
import io

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 你的简化版本
def isValid(s: str) -> bool:
    parenthese_dict = {')':'(', '}':'{', ']':'['}
    stack = []             # stack
    for p in s:
        if p in parenthese_dict.keys():     # 尾括号
            if stack == []:                         # 只有尾巴括号 错
                return False
            if stack.pop() != parenthese_dict[p]:   # 首尾不匹配 错
                return False
        else:                               # 首括号
            stack.append(p)                         
    return stack == []

print("=" * 70)
print("测试简化后的 isValid 函数")
print("=" * 70)

# LeetCode 20 标准测试用例
test_cases = [
    ("()", True),
    ("()[]{}", True),
    ("(]", False),
    ("([)]", False),
    ("{[]}", True),
    ("", True),  # 空字符串
    ("(((", False),  # 只有左括号
    (")))", False),  # 只有右括号
    ("()()", True),
    ("([{}])", True),
    ("([)]", False),
    ("((()))", True),
    ("((())", False),
    ("(())", True),
    ("[", False),
    ("]", False),
    ("([])", True),
    ("([{}])", True),
]

print("\n【标准测试用例】")
all_passed = True
for s, expected in test_cases:
    result = isValid(s)
    status = "✓" if result == expected else "✗"
    if result != expected:
        all_passed = False
        print(f"  {status} '{s:15}' -> {result:5} (expected: {expected}) ❌")
    else:
        print(f"  {status} '{s:15}' -> {result:5}")

if all_passed:
    print("\n✅ 所有测试用例通过！")
else:
    print("\n❌ 有测试用例失败")

print("\n" + "=" * 70)
print("代码分析")
print("=" * 70)

print("""
【你的实现分析】

✅ 逻辑清晰：
  1. 遇到右括号 → 检查栈是否为空 → 检查是否匹配
  2. 遇到左括号 → 压入栈
  3. 最后检查栈是否为空

✅ 代码结构：
  - 分步检查，思路清晰
  - 注释明确（"只有尾巴括号 错"、"首尾不匹配 错"）
  - 没有过度优化，可读性好

✅ 正确性：
  - 所有标准测试用例都通过
  - 边界情况处理正确（空字符串、只有左括号、只有右括号）

【小优化建议（可选）】

1. 字典检查可以简化：
   if p in parenthese_dict.keys():  # 当前
   if p in parenthese_dict:         # 更简洁（但你的版本也完全正确）

2. 空栈检查可以更Pythonic：
   if stack == []:  # 当前（完全正确）
   if not stack:   # 更Pythonic（但你的版本更明确）

注意：这些都是风格问题，不是功能问题。你的代码逻辑清晰，完全正确！
""")

print("\n" + "=" * 70)
print("总结")
print("=" * 70)

print("""
✅ 你的代码完全正确，没有功能性问题

✅ 代码风格：
  - 逻辑清晰，分步检查
  - 注释明确
  - 可读性好

✅ 对于 LeetCode 20 题，你的实现：
  - 时间复杂度：O(n)
  - 空间复杂度：O(n)
  - 逻辑正确，能通过所有测试用例

💡 建议：
  - 保持当前的代码风格（清晰 > 简洁）
  - 如果追求更Pythonic，可以做一些小优化
  - 但当前的实现已经很好，不需要强制优化
""")

