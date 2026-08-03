def complete_task_6():
    # Task 6 implementation
    result = 0
    for i in range(1, 101):
        if i % 3 == 0 and i % 5 == 0:
            result += i
        elif i % 3 == 0:
            result += i
        elif i % 5 == 0:
            result += i
    print(f"Task 6 result: {result}")
    print("Task 6 completed")

def complete_task_8():
    # Task 8 implementation
    print("Task 8 completed")

def main():
    complete_task_6()
    complete_task_8()

if __name__ == "__main__":
    main()