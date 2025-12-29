from typing import List

'''
差分数组 -- 核心模板

快速对区间进行修改
### 核心判断标准：
1. ✅ **区间更新**：对区间 [i, j] 统一操作
2. ✅ **多次操作**：有多个区间更新操作
3. ✅ **最终查询**：只需要最终结果，不需要中间状态
4. ✅ **一维数组**：问题可以转化为一维数组
'''
class Difference:
    # 差分数组
    def __init__(self, nums: List[int]):
        assert len(nums) > 0
        self.diff = [0] * len(nums)
        # 构造差分数组
        self.diff[0] = nums[0]
        for i in range(1, len(nums)):
            self.diff[i] = nums[i] - nums[i - 1]

    # 差分步骤 -- 给闭区间 [i, j] 增加 val（可以是负数）
    def increment(self, i: int, j: int, val: int):
        # 差分数组 i + val
        self.diff[i] += val
        # j+1 位置 - val 还原
        if j + 1 < len(self.diff):
            self.diff[j + 1] -= val

    # 构造结果数组 -- 根据差分数组
    def result(self) -> List[int]:
        res = [0] * len(self.diff)
        res[0] = self.diff[0]
        for i in range(1, len(self.diff)):
            res[i] = res[i - 1] + self.diff[i]
        return res


# 利用差分数组example
def getModifiedArray(length: int, updates: List[List[int]]) -> List[int]:
    # nums 初始化为全 0
    nums = [0] * length
    # 构造差分解法
    df = Difference(nums)
    for update in updates:
        i = update[0]
        j = update[1]
        val = update[2]
        df.increment(i, j, val)
    return df.result()


# lc 1109 跟上面example完全相同
'''
You are given an array of flight bookings bookings, where bookings[i] = [firsti, lasti, seatsi] represents a booking for flights 
firsti through lasti (inclusive) with seatsi seats reserved for each flight in the range.
Return an array answer of length n, where answer[i] is the total number of seats reserved for flight i.
'''
def corpFlightBookings(bookings: List[List[int]], n: int) -> List[int]:
    nums = [0] * n
    df = Difference(nums)
    for book in bookings:
        i = book[0] - 1    # flight label 从1开始，match差分数组需要-1 从0开始
        j = book[1] - 1
        val = book[2]
        df.increment(i,j,val)
    return df.result()


# lc 1094 拼车
'''
There is a car with capacity empty seats. The vehicle only drives east (i.e., it cannot turn around and drive west).

You are given the integer capacity and an array trips where trips[i] = [numPassengersi, fromi, toi] indicates that 
the ith trip has numPassengersi passengers and the locations to pick them up and drop them off are fromi and toi respectively. 
The locations are given as the number of kilometers due east from the car's initial location.

Return true if it is possible to pick up and drop off all passengers for all the given trips, or false otherwise.
思路： 差分数组
    车站[cap,cap,cap,cap...]
'''
def carPooling(trips: List[List[int]], capacity: int) -> bool:
    stop = [0] * 10           # using max stop 1000， test with 10
    df = Difference(stop)
    # print(df.diff)      

    for trip in trips:                    # [2,1,5]   2ppl, 0上车， 4下车
        ppl = trip[0]
        on_stop = trip[1]                  # ！！！先下车再上车；否则同一站可能超载！！！
        off_stop = trip[2] - 1             # exclusive -- 算（前一站）已经下车
        df.increment(on_stop, off_stop, ppl)
    res = df.result()
    print(res)

    # 检查原数组是否超载
    for p in res:
        if p > capacity:
            return False
    return True

    

    
 


if __name__ == "__main__":
    bookings = [[1,2,10],[2,3,20],[2,5,25]]
    n = 5
    print(corpFlightBookings(bookings, n))

    trips = [[2,1,5],[3,5,7]]
    trips2 = [[9,0,1],[3,5,7]]
    cap = 4
    carPooling(trips2, cap)
