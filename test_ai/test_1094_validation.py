from typing import List

class Difference:
    def __init__(self, nums: List[int]):
        self.diff = [0] * len(nums)
        self.diff[0] = nums[0]
        for i in range(1, len(nums)):
            self.diff[i] = nums[i] - nums[i - 1]

    def increment(self, i: int, j: int, val: int):
        self.diff[i] += val
        if j + 1 < len(self.diff):
            self.diff[j + 1] -= val

    def result(self) -> List[int]:
        res = [0] * len(self.diff)
        res[0] = self.diff[0]
        for i in range(1, len(self.diff)):
            res[i] = res[i - 1] + self.diff[i]
        return res

print("=" * 70)
print("Testing LeetCode 1094: Car Pooling")
print("=" * 70)
print()

# Test case from user: [[9,0,1],[3,5,7]]
print("Test case: [[9,0,1],[3,5,7]]")
print()

# Trip 1: [9, 0, 1]
print("Trip 1: [9, 0, 1]")
print("  - 9 passengers get ON at location 0")
print("  - They get OFF at location 1")
print()

# If toi is INCLUSIVE (passengers still in car at location 1):
print("If toi is INCLUSIVE (passengers still in car at location 1):")
print("  - Passengers are in car at locations: 0, 1")
print("  - on_stop = 0, off_stop = 1")
print("  - increment(0, 1, 9)")
stop1 = [0] * 10
df1 = Difference(stop1)
df1.increment(0, 1, 9)
result1 = df1.result()
print(f"  Result: {result1}")
print(f"  Location 0: {result1[0]} passengers")
print(f"  Location 1: {result1[1]} passengers")
print()

# If toi is EXCLUSIVE (passengers NOT in car at location 1):
print("If toi is EXCLUSIVE (passengers NOT in car at location 1):")
print("  - Passengers are in car at locations: 0 only")
print("  - on_stop = 0, off_stop = 0 (because 1-1=0)")
print("  - increment(0, 0, 9)")
stop2 = [0] * 10
df2 = Difference(stop2)
df2.increment(0, 0, 9)
result2 = df2.result()
print(f"  Result: {result2}")
print(f"  Location 0: {result2[0]} passengers")
print(f"  Location 1: {result2[1]} passengers")
print()

# Trip 2: [3, 5, 7]
print("Trip 2: [3, 5, 7]")
print("  - 3 passengers get ON at location 5")
print("  - They get OFF at location 7")
print()

# If toi is INCLUSIVE:
print("If toi is INCLUSIVE:")
print("  - Passengers are in car at locations: 5, 6, 7")
print("  - on_stop = 5, off_stop = 7")
print("  - increment(5, 7, 3)")
stop3 = [0] * 10
df3 = Difference(stop3)
df3.increment(5, 7, 3)
result3 = df3.result()
print(f"  Result: {result3}")
print(f"  Location 5: {result3[5]} passengers")
print(f"  Location 6: {result3[6]} passengers")
print(f"  Location 7: {result3[7]} passengers")
print(f"  Location 8: {result3[8]} passengers")
print()

# If toi is EXCLUSIVE:
print("If toi is EXCLUSIVE:")
print("  - Passengers are in car at locations: 5, 6 (NOT 7)")
print("  - on_stop = 5, off_stop = 6 (because 7-1=6)")
print("  - increment(5, 6, 3)")
stop4 = [0] * 10
df4 = Difference(stop4)
df4.increment(5, 6, 3)
result4 = df4.result()
print(f"  Result: {result4}")
print(f"  Location 5: {result4[5]} passengers")
print(f"  Location 6: {result4[6]} passengers")
print(f"  Location 7: {result4[7]} passengers")
print()

print("=" * 70)
print("User's current code:")
print("  on_stop = trip[1]        # No -1, because 0-based")
print("  off_stop = trip[2] - 1    # -1 because toi is exclusive")
print()
print("For trip [9, 0, 1]:")
print("  on_stop = 0")
print("  off_stop = 1 - 1 = 0")
print("  increment(0, 0, 9) -> affects location 0 only")
print("  This means: passengers are in car at location 0, NOT at location 1")
print("  So toi is EXCLUSIVE!")
print()
print("For trip [3, 5, 7]:")
print("  on_stop = 5")
print("  off_stop = 7 - 1 = 6")
print("  increment(5, 6, 3) -> affects locations 5, 6")
print("  This means: passengers are in car at locations 5, 6, NOT at location 7")
print("  So toi is EXCLUSIVE!")
print()
print("=" * 70)
print("Conclusion:")
print("  - Positions are 0-based (fromi can be 0)")
print("  - fromi is INCLUSIVE (passengers get on)")
print("  - toi is EXCLUSIVE (passengers get off, so NOT in car at toi)")
print("  - So: on_stop = fromi, off_stop = toi - 1")
print("  - This matches: increment(on_stop, off_stop, ppl)")
print("=" * 70)

