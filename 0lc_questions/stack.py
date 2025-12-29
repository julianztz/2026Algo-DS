# 71 simplify path
'''
A single period '.' represents the current directory.
A double period '..' represents the previous/parent directory.
Multiple consecutive slashes such as '//' and '///' are treated as a single slash '/'.

Any sequence of periods that does not match the rules above should be treated as a valid directory or file name. 
For example, '...' and '....' are valid directory or file names.

思路：遍历list 看成stack
遇到'..' pop()
合法路径 push()
'''


def simplifyPath(path: str) -> str:
    res = []                       # simulate stack
    path_ls = path.split("/")

    for dir in path_ls:
        if dir == "." or dir == "":  # 跳过 "." 和空字符串
            continue
        elif dir == "..":
            if res: 
                res.pop()         # pop
        else:
            res.append(dir)       # push
    
    res_str = '/' + '/'.join(res)

    print(res_str)
    return res_str


# 20 valid parentheses
'''
Given a string s containing just the characters 
'(', ')', '{', '}', '[' and ']', determine if the input string is valid.
括号成对出现，可以包含不可以混插 -- xml tag规则一致

思路：
dict ')': '(', ']': '['  记录match 括号组合

'''
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






if __name__ == '__main__':
    # 71 测试用例
    test_paths = [
        "/home//foo/",                      # 应该返回 "/home/foo"
        "/home/user/Documents/../Pictures", # 应该返回 "/home/user/Pictures"
        "/.../a/../b/c/../d/./",            # 应该返回 "/.../b/d"
        "/../",                              # 应该返回 "/" (关键测试：空栈)
        "/home/../../",                      # 应该返回 "/" (关键测试：空栈)
        "/../a",                             # 应该返回 "/a" (关键测试：空栈)
        "/",                                 # 应该返回 "/"
        "/a/./b/../../c/",                  # 应该返回 "/c"
    ]

    # for path in test_paths:
    #     result = simplifyPath(path)
    #     print(f"Input: {path:40} -> Output: {result}")


    # 20 testcase
    s = "()[]{}"
    s2 = "[(){}]"
    isValid(s2)