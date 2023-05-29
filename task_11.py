import numpy as np
import matplotlib.pyplot as plt

def main():
    # Define the angle values
    theta = np.linspace(0, 2*np.pi, 1000)
    # Define the scaling factor
    a = 1
    # Calculate the radial values (r)
    r = a * (1 + np.cos(theta))

    # Convert polar coordinates to Cartesian coordinates
    x = r * np.cos(theta)
    y = r * np.sin(theta)

    # Create a figure and axes
    fig, ax = plt.subplots()

    # Plot the cardioid
    ax.plot(x, y, label='Cardioid')
    ax.set_title('Cardioid')
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_aspect('equal')
    ax.legend()
    plt.show()

if __name__ == '__main__':
    main()