from collections import deque

'''
push
pop
peek
size
'''
class MyLinkedStack:                 # FILO， 同一端插入删除
    
    def __init__(self) -> None:
        self.stack = deque()

    def pop(self):
        if not self.stack:
            raise IndexError("pop from empty stack")
        return self.stack.pop()

    def push(self, e):
        self.stack.append(e)

    def peek(self):
        return self.stack[-1]

    def size(self):
        return len(self.stack)


'''
enqueue
dequeue
size
'''
class MyLinkedQueue:               # FIFO, 一端插入，另一端删除

    def __init__(self) -> None:
        self.queue = deque()

    def enqueue(self, e):
        self.queue.append(e)

    def dequeue(self):
        if not self.queue:
            raise IndexError("dequeue from empty queue")
        return self.queue.popleft()

    def peek(self):
        return self.queue[0]

    def size(self):
        return len(self.queue)
