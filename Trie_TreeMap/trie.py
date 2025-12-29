'''
字典树
Trie 树用「树枝」存储字符串（key），用「节点」存储字符串（key）对应的数据（value）
'''

class TrieNode:
    def __init__(self) -> None:
        self.children = {}      # 子节点
        self.is_end = False     # 完整单词


class Trie:
    def __init__(self) -> None:
        self.root = TrieNode()

    def insert(self, word) -> None:
        node = self.root
        for ch in word:
            if ch not in node.children:
                node.children[ch] = TrieNode()   # 加入新的node
            node = node.children[ch]
        node.is_end = True

    def search(self, word) -> bool:
        node = self.root
        for ch in word:
            if ch not in node.children:
                return False
            node = node.children[ch]
        return node.is_end
    
    def startsWith(self, prefix) -> bool:
        node = self.root
        for ch in prefix:
            if ch not in node.children:
                return False
            node = node.children[ch]
        return True


# ============================================================================
# LeetCode 211: Design Add and Search Words Data Structure
# 支持通配符 '.' 的单词搜索（高频面试题）
# ============================================================================

class WordDictionary:
    """
    LeetCode 211: 支持通配符搜索的单词字典
    
    特点：
    - addWord(word): 添加单词
    - search(word): 搜索单词，支持 '.' 通配符（匹配任意一个字符）
    
    实现要点：
    1. 基础 Trie 结构（TrieNode + children + is_end）
    2. search 使用 DFS 递归处理通配符
    3. 遇到 '.' 时尝试所有子节点（回溯思想）
    4. 终止条件必须检查 is_end（区分完整单词和前缀）
    """
    
    def __init__(self):
        self.root = TrieNode()
    
    def addWord(self, word: str) -> None:
        """添加单词到字典树"""
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end = True  # ✅ 关键：标记单词结尾
    
    def search(self, word: str) -> bool:
        """
        搜索单词，支持通配符 '.'
        
        核心思路：
        - 使用 DFS 递归遍历
        - 遇到 '.' 时尝试所有子节点
        - 终止时检查 is_end（确保是完整单词）
        """
        def dfs(node: TrieNode, idx: int) -> bool:
            # 终止条件：遍历完所有字符
            if idx == len(word):
                return node.is_end  # ✅ 必须检查是否为完整单词
            
            char = word[idx]
            
            # 处理通配符 '.'
            if char == '.':
                # 尝试所有子节点（回溯思想）
                for child in node.children.values():
                    if dfs(child, idx + 1):
                        return True
                return False
            
            # 处理普通字符
            else:
                if char not in node.children:
                    return False
                return dfs(node.children[char], idx + 1)
        
        return dfs(self.root, 0)


# ============================================================================
# 辅助函数：prefixCheck（如果需要单独的前缀检查功能）
# ============================================================================

def prefixCheck(trie: Trie, prefix: str) -> bool:
    """
    检查 Trie 中是否存在以 prefix 开头的单词
    
    注意：这是普通的 prefix check（不支持通配符）
    如果需要在 WordDictionary 中支持通配符的前缀检查，需要类似的 DFS 实现
    """
    node = trie.root
    for char in prefix:
        if char not in node.children:
            return False
        node = node.children[char]
    return True  # ✅ 前缀存在（不需要检查 is_end）


# ============================================================================
# 测试用例
# ============================================================================

if __name__ == "__main__":
    # 测试 LC211
    print("=== LeetCode 211 测试 ===")
    wd = WordDictionary()
    wd.addWord("bad")
    wd.addWord("dad")
    wd.addWord("mad")
    
    print(f"search('pad'): {wd.search('pad')}")    # False
    print(f"search('bad'): {wd.search('bad')}")    # True
    print(f"search('.ad'): {wd.search('.ad')}")    # True (匹配 "bad" 或 "dad")
    print(f"search('b..'): {wd.search('b..')}")    # True (匹配 "bad")
    
    # 测试 prefixCheck
    print("\n=== Prefix Check 测试 ===")
    trie = Trie()
    trie.insert("apple")
    trie.insert("app")
    print(f"prefixCheck('app'): {prefixCheck(trie, 'app')}")  # True
    print(f"trie.search('app'): {trie.search('app')}")        # True (因为插入了 "app")
    print(f"trie.startsWith('app'): {trie.startsWith('app')}") # True