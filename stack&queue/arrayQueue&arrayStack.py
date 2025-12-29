
'''
push
pop
peek
size
'''
class MyArrayStack:
    def __init__(self) -> None:
        self.stack = list()

    def push(self, e):
        self.stack.append(e)

    def pop(self):
        if not self.stack:
            raise IndexError("pop from empty stack")
        return self.stack.pop()
    
    def peek(self):
        if not self.stack:
            raise IndexError("peek from empty stack")
        return self.stack[-1]
    
    def size(self):
        return len(self.stack)

        
class MyArrayQueue:
    def __init__(self) -> None:
        self.queue = list()

    def enqueue(self, e):
        self.queue.append(e)

    def dequeue(self):                    # 低效 O n -- 需要shift 所有元素left
        if not self.queue: 
            raise IndexError("dequeue from empty queue")
        return self.queue.pop(0)              

    def peek(self):
        if not self.queue:
            raise IndexError("peek from empty queue")
        return self.queue[0]
    
    def size(self):
        return len(self.queue)