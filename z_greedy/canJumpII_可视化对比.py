"""
Jump Game II 贪心思路可视化对比
用于理解为什么选择 nums[j] 最大是错误的，而应该选择 j + nums[j] 最大
"""

def visualize_choice(nums, pos, strategy_name, strategy_func):
    """可视化在位置pos的选择过程"""
    print(f"\n{'='*60}")
    print(f"位置 {pos}, nums[{pos}] = {nums[pos]}")
    print(f"可以跳到: {list(range(pos+1, min(pos+1+nums[pos], len(nums))))}")
    print(f"策略: {strategy_name}")
    print(f"{'-'*60}")
    
    reachable = []
    for step in range(1, nums[pos] + 1):
        next_pos = pos + step
        if next_pos >= len(nums):
            break
        reachable.append(next_pos)
    
    print(f"{'位置':<6} {'nums值':<8} {'能到达最远':<12} {'选择标准':<15}")
    print(f"{'-'*60}")
    
    best_choice = None
    best_value = None
    
    for j in reachable:
        nums_val = nums[j]
        farthest_from_j = j + nums[j]
        choice_value = strategy_func(j, nums)
        
        marker = ""
        if best_choice is None or choice_value > best_value:
            best_choice = j
            best_value = choice_value
            marker = " ← 当前最优"
        elif choice_value == best_value and j == best_choice:
            marker = " ← 当前最优"
        
        print(f"{j:<6} {nums_val:<8} {farthest_from_j:<12} {choice_value:<15}{marker}")
    
    print(f"\n选择位置: {best_choice}")
    print(f"从位置 {best_choice} 能到达最远: {best_choice + nums[best_choice]}")
    return best_choice


def strategy_wrong(j, nums):
    """错误策略：选择 nums[j] 最大的位置"""
    return nums[j]


def strategy_correct(j, nums):
    """正确策略：选择 j + nums[j] 最大的位置（能到达最远）"""
    return j + nums[j]


def simulate_path(nums, strategy_name, strategy_func):
    """模拟完整路径"""
    print(f"\n{'#'*60}")
    print(f"模拟路径 - 策略: {strategy_name}")
    print(f"数组: {nums}")
    print(f"{'#'*60}")
    
    path = [0]
    jumps = 0
    pos = 0
    
    while pos < len(nums) - 1:
        if pos + nums[pos] >= len(nums) - 1:
            jumps += 1
            path.append(len(nums) - 1)
            break
        
        next_pos = visualize_choice(nums, pos, strategy_name, strategy_func)
        path.append(next_pos)
        jumps += 1
        pos = next_pos
    
    print(f"\n完整路径: {' → '.join(map(str, path))}")
    print(f"跳跃次数: {jumps}")
    return jumps


# 测试用例1: 你的思路会出错的情况
print("="*60)
print("测试用例1: [3, 2, 1, 1, 4]")
print("="*60)

nums1 = [3, 2, 1, 1, 4]
jumps_wrong = simulate_path(nums1, "选择nums[j]最大", strategy_wrong)
jumps_correct = simulate_path(nums1, "选择j+nums[j]最大", strategy_correct)

print(f"\n{'='*60}")
print(f"结果对比:")
print(f"  错误策略: {jumps_wrong} 步")
print(f"  正确策略: {jumps_correct} 步")
print(f"  最优解应该是: 2 步")
print(f"{'='*60}")

# 测试用例2: 你的思路正确的情况
print("\n\n" + "="*60)
print("测试用例2: [2, 3, 1, 1, 4]")
print("="*60)

nums2 = [2, 3, 1, 1, 4]
jumps_wrong2 = simulate_path(nums2, "选择nums[j]最大", strategy_wrong)
jumps_correct2 = simulate_path(nums2, "选择j+nums[j]最大", strategy_correct)

print(f"\n{'='*60}")
print(f"结果对比:")
print(f"  错误策略: {jumps_wrong2} 步")
print(f"  正确策略: {jumps_correct2} 步")
print(f"  最优解应该是: 2 步")
print(f"{'='*60}")

# 测试用例3: 更明显的反例
print("\n\n" + "="*60)
print("测试用例3: [1, 1, 1, 1, 1]")
print("="*60)

nums3 = [1, 1, 1, 1, 1]
jumps_wrong3 = simulate_path(nums3, "选择nums[j]最大", strategy_wrong)
jumps_correct3 = simulate_path(nums3, "选择j+nums[j]最大", strategy_correct)

print(f"\n{'='*60}")
print(f"结果对比:")
print(f"  错误策略: {jumps_wrong3} 步")
print(f"  正确策略: {jumps_correct3} 步")
print(f"  最优解应该是: 4 步（两种策略结果相同，因为nums值都相同）")
print(f"{'='*60}")











