from typing import List

class Difference:
    def __init__(self, nums: List[int]):
        assert len(nums) > 0
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
print("Problem 1109: Corp Flight Bookings")
print("=" * 70)
print("Definition: bookings[i] = [firsti, lasti, seatsi]")
print("Meaning: Flights from firsti to lasti (INCLUSIVE) have seatsi seats")
print()
print("Example: booking = [1, 3, 10]")
print("  - This means flights 1, 2, 3 all have 10 seats")
print("  - Array indices: [0, 1, 2] (need to -1)")
print()

bookings_1109 = [[1, 3, 10]]
n = 5
nums_1109 = [0] * n
df_1109 = Difference(nums_1109)
for book in bookings_1109:
    i = book[0] - 1  # flight 1 -> index 0
    j = book[1] - 1  # flight 3 -> index 2
    val = book[2]
    print(f"Booking {book}:")
    print(f"  firsti={book[0]}, lasti={book[1]} (both inclusive)")
    print(f"  Convert to indices: i={i}, j={j}")
    print(f"  This affects indices [{i}, {j}] (inclusive)")
    df_1109.increment(i, j, val)
result_1109 = df_1109.result()
print(f"Result: {result_1109}")
print(f"  Flight 1 (index 0): {result_1109[0]} seats")
print(f"  Flight 2 (index 1): {result_1109[1]} seats")
print(f"  Flight 3 (index 2): {result_1109[2]} seats")
print(f"  Flight 4 (index 3): {result_1109[3]} seats")
print()

print("=" * 70)
print("Problem 1094: Car Pooling")
print("=" * 70)
print("Definition: trips[i] = [numPassengersi, fromi, toi]")
print("Meaning: Pick up at fromi, drop off at toi")
print("  - fromi: INCLUSIVE (passengers get on here)")
print("  - toi: EXCLUSIVE (passengers get off here, so they're NOT in the car at toi)")
print()
print("Example: trip = [2, 1, 5]")
print("  - 2 passengers get on at location 1")
print("  - They get off at location 5")
print("  - So passengers are in the car at locations 1, 2, 3, 4 (NOT at 5)")
print("  - Array indices: [0, 1, 2, 3] (need to -1 for fromi, and toi-1 for off_stop)")
print()

trips_1094 = [[2, 1, 5]]
capacity = 10
stop = [0] * 10
df_1094 = Difference(stop)

for trip in trips_1094:
    ppl = trip[0]
    on_stop = trip[1]  # location 1
    off_stop = trip[2]  # location 5
    print(f"Trip {trip}:")
    print(f"  fromi={on_stop}, toi={off_stop}")
    print(f"  Passengers are in car from location {on_stop} to {off_stop-1} (inclusive)")
    print(f"  They get OFF at location {off_stop}, so location {off_stop} should NOT have these passengers")
    print()
    print(f"  For difference array:")
    print(f"    on_stop = {on_stop} -> index {on_stop - 1} (passengers get on)")
    print(f"    off_stop = {off_stop} -> index {off_stop - 1} (passengers get off)")
    print(f"    But we need to use off_stop - 1 because:")
    print(f"      - At location {off_stop-1}, passengers are still in car")
    print(f"      - At location {off_stop}, passengers are NOT in car")
    print(f"      - So we increment [on_stop-1, off_stop-2] (inclusive)")
    print(f"      - Which means: on_stop-1 to off_stop-2, both inclusive")
    print()
    
    # Current code
    on_stop_idx = on_stop - 1
    off_stop_idx = off_stop - 1
    print(f"  Current code: on_stop_idx={on_stop_idx}, off_stop_idx={off_stop_idx}")
    print(f"  This increments indices [{on_stop_idx}, {off_stop_idx}] (inclusive)")
    print(f"  But this is WRONG! Location {off_stop} (index {off_stop_idx}) should NOT have passengers")
    print()
    
    # Correct code
    on_stop_idx_correct = on_stop - 1
    off_stop_idx_correct = off_stop - 2  # -2 because toi is exclusive
    print(f"  Correct code: on_stop_idx={on_stop_idx_correct}, off_stop_idx={off_stop_idx_correct}")
    print(f"  This increments indices [{on_stop_idx_correct}, {off_stop_idx_correct}] (inclusive)")
    print(f"  This correctly excludes location {off_stop} (index {off_stop-1})")
    print()
    
    # Test both
    print("Testing current code (WRONG):")
    df_wrong = Difference(stop)
    df_wrong.increment(on_stop_idx, off_stop_idx, ppl)
    result_wrong = df_wrong.result()
    print(f"  Result: {result_wrong}")
    print(f"  Location 4 (index 4): {result_wrong[4]} passengers")
    print(f"  Location 5 (index 5): {result_wrong[5]} passengers <- WRONG! Should be 0")
    print()
    
    print("Testing correct code:")
    df_correct = Difference(stop)
    df_correct.increment(on_stop_idx_correct, off_stop_idx_correct, ppl)
    result_correct = df_correct.result()
    print(f"  Result: {result_correct}")
    print(f"  Location 4 (index 4): {result_correct[4]} passengers")
    print(f"  Location 5 (index 5): {result_correct[5]} passengers <- CORRECT! Should be 0")

