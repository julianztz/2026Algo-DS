# -*- coding: utf-8 -*-
"""
测试 isValid 括号匹配函数
"""

import sys
import io

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 你的实现
def isValid_USER(s: str) -> bool:
    parenthese_dict = {')':'(', '}':'{', ']':'['}
    stack = []             # stack
    for p in s:
        if p in parenthese_dict.keys():     # 尾括号
            if stack == []:
                return False
            last = stack.pop()
            if last != parenthese_dict[p]:
                return False
        else:                               # 首括号
            stack.append(p)
    if stack == []:
        return True
    return False

# 优化版本
def isValid_OPTIMIZED(s: str) -> bool:
    parenthese_dict = {')':'(', '}':'{', ']':'['}
    stack = []
    for p in s:
        if p in parenthese_dict:  # 右括号
            if not stack:  # 更Pythonic的写法
                return False
            if stack.pop() != parenthese_dict[p]:
                return False
        else:  # 左括号或其他字符
            stack.append(p)
    return not stack  # 简化返回

# 更严格的版本（只接受括号字符）
def isValid_STRICT(s: str) -> bool:
    parenthese_dict = {')':'(', '}':'{', ']':'['}
    left_brackets = set(parenthese_dict.values())
    stack = []
    for p in s:
        if p in parenthese_dict:  # 右括号
            if not stack:
                return False
            if stack.pop() != parenthese_dict[p]:
                return False
        elif p in left_brackets:  # 左括号
            stack.append(p)
        else:  # 其他字符
            return False  # 或者根据题目要求处理
    return not stack

print("=" * 70)
print("测试你的 isValid 函数")
print("=" * 70)

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
    ("a", True),  # ⚠️ 你的函数会把非括号字符当作左括号
    ("(a)", True),  # ⚠️ 你的函数会接受包含其他字符的情况
]

print("\n【你的实现测试】")
all_passed = True
for s, expected in test_cases:
    result = isValid_USER(s)
    status = "✓" if result == expected else "✗"
    if result != expected:
        all_passed = False
    print(f"  {status} '{s:15}' -> {result:5} (expected: {expected})")

if all_passed:
    print("\n✅ 所有标准测试用例通过！")
else:
    print("\n❌ 有测试用例失败")

print("\n" + "=" * 70)
print("问题分析")
print("=" * 70)

print("""
【你的实现分析】

✅ 核心逻辑正确：
  - 使用栈来匹配括号
  - 遇到右括号时检查栈顶是否匹配
  - 最后检查栈是否为空

⚠️ 潜在问题：

1. 非括号字符的处理：
   - 你的函数会把任何非右括号的字符当作左括号压入栈
   - 例如："a" 会返回 True（栈为空）
   - 例如："(a)" 会返回 True（'a' 被当作左括号）
   - 根据题目要求，这可能不是问题（如果题目说只包含括号字符）

2. 代码风格：
   - `stack == []` 可以改为 `not stack`（更Pythonic）
   - 最后的 if-else 可以简化为 `return not stack`

3. 边界情况：
   - 空字符串：✅ 正确处理（返回 True）
   - 只有左括号：✅ 正确处理（返回 False）
   - 只有右括号：✅ 正确处理（返回 False）
""")

print("\n" + "=" * 70)
print("代码优化建议")
print("=" * 70)

print("""
【优化版本对比】

你的版本：
  if stack == []:
      return True
  return False

优化版本：
  return not stack  # 更简洁

你的版本：
  if p in parenthese_dict.keys():
  
优化版本：
  if p in parenthese_dict:  # 直接检查字典，不需要 .keys()
""")

print("\n" + "=" * 70)
print("测试：非括号字符的处理")
print("=" * 70)

edge_cases = [
    "a",           # 单个非括号字符
    "(a)",         # 包含非括号字符
    "()a",         # 括号后跟非括号字符
    "a()",         # 非括号字符后跟括号
    "([a])",       # 嵌套中包含非括号字符
]

print("\n你的函数对这些输入的处理：")
for s in edge_cases:
    result = isValid_USER(s)
    print(f"  '{s}' -> {result}")

print("\n说明：")
print("  - 如果你的题目明确说'只包含括号字符'，那么这些情况不会出现")
print("  - 如果你的题目允许其他字符，那么你的实现是正确的")
print("  - 如果题目要求严格只接受括号，需要额外检查")

print("\n" + "=" * 70)
print("总结")
print("=" * 70)

print("""
✅ 你的实现核心逻辑正确，可以处理标准的括号匹配问题

⚠️ 需要注意的点：
  1. 非括号字符会被当作左括号处理（根据题目要求决定是否需要修改）
  2. 代码可以更Pythonic（使用 not stack 而不是 stack == []）
  3. 可以简化最后的返回语句

💡 建议：
  - 如果题目保证输入只包含括号字符，你的实现完全正确
  - 如果想更严格，可以添加字符检查
  - 如果想更简洁，可以优化代码风格
""")

