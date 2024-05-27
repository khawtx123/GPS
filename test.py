import numpy as np
import matplotlib.pyplot as plt


def plot_difference(array1, array2):
    # Calculate the absolute difference between corresponding elements

    # Plot the differences
    plt.figure(figsize=(8, 6))
    plt.plot(array1, marker='o', linestyle='-', color='b')
    plt.plot(array2, marker='x', linestyle='-', color='r')
    # Set axis labels and title
    plt.xlabel('Index')
    plt.ylabel('Absolute Difference')
    plt.title('Difference between Arrays')

    plt.grid(True)  # Add grid lines

    plt.show()


# Example arrays
array1 = [1, 2, 3, 4, 5]
array2= [2,4,6,8,10]
plot_difference(array1, array2)
