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
print("Problem 1094: Car Pooling - Understanding the difference")
print("=" * 70)
print()
print("Trip: [2, 1, 5] means:")
print("  - 2 passengers get ON at location 1")
print("  - They get OFF at location 5")
print("  - So passengers are in car at locations: 1, 2, 3, 4")
print("  - They are NOT in car at location 5 (they got off)")
print()

# Current implementation (from user's code)
print("Current implementation:")
print("  on_stop = trip[1] - 1 = 1 - 1 = 0")
print("  off_stop = trip[2] - 1 = 5 - 1 = 4")
print("  increment(0, 4, 2)")
print()

stop = [0] * 10
df_current = Difference(stop)
df_current.increment(0, 4, 2)
result_current = df_current.result()
print(f"Result: {result_current}")
print(f"  Location 1 (index 0): {result_current[0]} passengers")
print(f"  Location 2 (index 1): {result_current[1]} passengers")
print(f"  Location 3 (index 2): {result_current[2]} passengers")
print(f"  Location 4 (index 3): {result_current[3]} passengers")
print(f"  Location 5 (index 4): {result_current[4]} passengers <- PROBLEM!")
print()
print("Problem: Location 5 (index 4) has 2 passengers, but they got off at location 5!")
print()

# Correct implementation
print("=" * 70)
print("Correct implementation:")
print("  Since toi is EXCLUSIVE (passengers get off at toi),")
print("  we need: off_stop = trip[2] - 1 - 1 = trip[2] - 2")
print("  OR: off_stop = trip[2] - 1, then use increment(0, 3, 2)")
print("  This affects indices [0, 3] = locations [1, 2, 3, 4]")
print()

stop2 = [0] * 10
df_correct = Difference(stop2)
df_correct.increment(0, 3, 2)  # off_stop should be 3, not 4
result_correct = df_correct.result()
print(f"Result: {result_correct}")
print(f"  Location 1 (index 0): {result_correct[0]} passengers")
print(f"  Location 2 (index 1): {result_correct[1]} passengers")
print(f"  Location 3 (index 2): {result_correct[2]} passengers")
print(f"  Location 4 (index 3): {result_correct[3]} passengers")
print(f"  Location 5 (index 4): {result_correct[4]} passengers <- CORRECT!")
print()

print("=" * 70)
print("Comparison with 1109:")
print("=" * 70)
print("1109: firsti to lasti are BOTH INCLUSIVE")
print("  booking = [1, 3, 10] means flights 1, 2, 3 all have 10 seats")
print("  So we use: increment(0, 2, 10) -> affects indices [0, 2]")
print()
print("1094: fromi is INCLUSIVE, toi is EXCLUSIVE")
print("  trip = [2, 1, 5] means passengers at locations 1, 2, 3, 4")
print("  So we use: increment(0, 3, 2) -> affects indices [0, 3]")
print("  NOT increment(0, 4, 2) because location 5 is EXCLUSIVE")
print()

print("=" * 70)
print("Answer to your question:")
print("=" * 70)
print("You asked: '上车站不用-1 就像corpFlightBookings 1109一样？'")
print()
print("The answer is:")
print("  - Both need -1 to convert from 1-based to 0-based indexing")
print("  - But 1094 needs EXTRA -1 for off_stop because toi is EXCLUSIVE")
print("  - So: off_stop = trip[2] - 1 - 1 = trip[2] - 2")
print("  - OR: off_stop = trip[2] - 1, then use increment(on_stop, off_stop-1, ppl)")

