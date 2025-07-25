class RingBuffer:
    def __init__(self, capacity):
        self.capacity = capacity
        if capacity <= 0:
            raise ValueError("Capacity must be a positive integer")
        self.buffer = [None] * capacity    #Defining the empty buffer
        self.head = 0                      #Index of the oldest write element
        self.tail = 0                      #Index of the next write element
        self.size = 0                      #Current number of elements in the buffer

    def append_rb(self, item):
        self.buffer[self.tail] = item    #Adding the new element at the tail index
        self.tail = (self.tail + 1) % self.capacity  #Move tail to the next index, wrapping around if necessary
        if self.capacity > self.size:
            self.size += 1
        else:
            self.head = (self.head + 1) % self.capacity   #Head moves forward if buffer is full

    def get(self):
        if self.size == 0:                                 #base case for empty buffer
            return []
        
        if self.tail > self.head:                          #If tail is ahead of head, return the slice directly
            return self.buffer[self.head:self.tail]                     
        else:
            return self.buffer[self.head:] + self.buffer[:self.tail]
            

    def is_empty(self):
        return self.size == 0
    
    def is_full(self):
        return self.size == self.capacity
    
    def clear(self):
        self.buffer = [None] * self.capacity
        self.head = 0
        self.tail = 0
        self.size = 0

    def __len__(self):
        return self.size
    
    def __str__(self):
        return f"RingBuffer({self.get()}) with capacity {self.capacity}, size {self.size}"
    
    def __repr__(self):
        return f"RingBuffer(capacity={self.capacity}, size={self.size}, buffer={self.buffer})"
    
    def __iter__(self):
        index = self.head
        for _ in range(self.size):
            yield self.buffer[index]
            index = (index + 1) % self.capacity


# Example usage:
if __name__ == "__main__":

    rb = RingBuffer(5)
    rb.append_rb(1)
    rb.append_rb(2)
    rb.append_rb(3)
    print(rb) # Output: RingBuffer([1, 2, 3])
    rb.append_rb(4)
    rb.append_rb(5)
    print(rb.get())  # Output: [1, 2, 3, 4, 5]
    rb.append_rb(6)  # This will overwrite the oldest element (1)
    print(rb.get())  # Output: [2, 3, 4, 5, 6]
    print(rb.is_full())  # Output: True
    