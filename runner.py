from calculator import Calculator

# Create an instance of the Calculator class
calculator = Calculator()

# Calculate and print the result of 5 + 3
result_add = calculator.add(5, 3)
print(f"5 + 3 = {result_add}")

# Calculate and print the result of 10 / 2
result_divide = calculator.divide(10, 2)
print(f"10 / 2 = {result_divide}")

# Test division by zero (optional, but good for demonstration)
result_zero_divide = calculator.divide(10, 0)
print(f"10 / 0 = {result_zero_divide}")