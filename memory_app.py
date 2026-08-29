class MemoryBlock:
    def __init__(self, address, size, is_free):
        self.address = address
        self.size = size
        self.is_free = is_free

class MemoryManager:
    def __init__(self, total_memory):
        self.total_memory = total_memory
        self.memory_blocks = [MemoryBlock(0, total_memory, True)]

    def allocate(self, size):
        for block in self.memory_blocks:
            if block.is_free and block.size >= size:
                if block.size > size:
                    new_block = MemoryBlock(block.address + size, block.size - size, True)
                    self.memory_blocks.remove(block)
                    self.memory_blocks.append(block)
                    self.memory_blocks.append(new_block)
                    self.memory_blocks.sort(key=lambda x: x.address)
                    block.size = size
                    block.is_free = False
                else:
                    block.is_free = False
                return block.address
        return -1

    def deallocate(self, address):
        for block in self.memory_blocks:
            if block.address == address and not block.is_free:
                block.is_free = True
                if self.memory_blocks.index(block) > 0 and self.memory_blocks[self.memory_blocks.index(block) - 1].is_free:
                    prev_block = self.memory_blocks[self.memory_blocks.index(block) - 1]
                    prev_block.size += block.size
                    self.memory_blocks.remove(block)
                elif self.memory_blocks.index(block) < len(self.memory_blocks) - 1 and self.memory_blocks[self.memory_blocks.index(block) + 1].is_free:
                    next_block = self.memory_blocks[self.memory_blocks.index(block) + 1]
                    block.size += next_block.size
                    self.memory_blocks.remove(next_block)
                return
        return

    def print_memory(self):
        for block in self.memory_blocks:
            status = "Free" if block.is_free else "Allocated"
            print(f"Address: {block.address}, Size: {block.size}, Status: {status}")

def main():
    memory_manager = MemoryManager(100)
    print("Initial Memory State:")
    memory_manager.print_memory()

    allocated_address = memory_manager.allocate(20)
    print(f"\nAllocated {20} bytes at address {allocated_address}")
    memory_manager.print_memory()

    allocated_address = memory_manager.allocate(30)
    print(f"\nAllocated {30} bytes at address {allocated_address}")
    memory_manager.print_memory()

    memory_manager.deallocate(allocated_address)
    print("\nDeallocated memory at address", allocated_address)
    memory_manager.print_memory()

    print("\nExplanation of memory_app.py:")
    print("This script implements a basic memory management system.")
    print("It includes two classes: MemoryBlock and MemoryManager.")
    print("The MemoryBlock class represents a block of memory with an address, size, and status (free or allocated).")
    print("The MemoryManager class manages a list of MemoryBlock objects and provides methods for allocating and deallocating memory.")
    print("The allocate method searches for a free MemoryBlock that is large enough to satisfy the requested size.")
    print("If a suitable block is found, it is split into two blocks if necessary, and the requested size is marked as allocated.")
    print("The deallocate method marks a previously allocated MemoryBlock as free and merges it with adjacent free blocks if possible.")
    print("The print_memory method displays the current state of the memory, including the address, size, and status of each MemoryBlock.")

if __name__ == "__main__":
    main()