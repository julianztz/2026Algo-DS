import heapq

def draw_tree(heap, title=''):
    '''用ASCII艺术绘制堆的树形结构'''
    if not heap:
        print('空堆')
        return
    
    print(f'\n{title}')
    print(f'数组表示: {heap}')
    print('\n树形结构:')
    
    # 计算树的深度
    depth = 0
    total = 0
    while total < len(heap):
        total += 2 ** depth
        depth += 1
    
    # 按层打印
    idx = 0
    for level in range(depth):
        # 计算当前层的节点
        level_size = min(2 ** level, len(heap) - idx)
        if level_size == 0:
            break
        
        nodes = [heap[idx + i] for i in range(level_size)]
        
        # 打印节点
        node_str = '  '.join([f'{n:2d}' for n in nodes])
        indent = ' ' * (15 - level * 2)
        print(f'{indent}{node_str}')
        
        # 打印连接线（如果不是最后一层且有下一层）
        if level < depth - 1 and idx + level_size < len(heap):
            next_level_size = min(2 ** (level + 1), len(heap) - (idx + level_size))
            if next_level_size > 0:
                # 每个父节点有左右两个连接
                lines = []
                for _ in range(len(nodes)):
                    lines.append('/\\')
                line_str = ' '.join(lines)
                indent_line = ' ' * (15 - level * 2 - 1)
                print(f'{indent_line}{line_str}')
        
        idx += level_size

# 创建初始堆
heap = []
nums = [1, 3, 2, 5, 6, 4]

print('=' * 60)
print('构建初始堆（Push操作）')
print('=' * 60)
for i, num in enumerate(nums):
    heapq.heappush(heap, num)
    print(f'\nPush {num}:')
    draw_tree(heap, f'Push {num} 之后')

# Pop操作
print('\n' + '=' * 60)
print('Pop操作：每一步的树形结构变化')
print('=' * 60)

pop_count = 0
popped_values = []
initial_heap = heap.copy()

print('\n初始堆:')
draw_tree(initial_heap, '初始状态')

while len(heap) > 2:
    min_val = heapq.heappop(heap)
    popped_values.append(min_val)
    pop_count += 1
    
    print(f'\n【Pop {pop_count}】')
    print(f'弹出值: {min_val} (当前堆中的最小值)')
    print('-' * 60)
    draw_tree(heap, f'Pop {pop_count} 之后的堆状态')

print(f'\n\n总结:')
print(f'初始堆: {initial_heap}')
print(f'最终剩余: {heap}')
print(f'已弹出顺序: {popped_values} (每次都是当前最小值)')
print(f'\n验证: 弹出顺序应该是递增的 [1, 2, 3, 4]，因为min heap每次pop最小值')


















