import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Generate simple data
x = np.linspace(0, 10, 50)
y = np.sin(x)

# Store in DataFrame
df = pd.DataFrame({"x": x, "y": y})
print("Data summary:")
print(df.head())

# Plot
plt.plot(df["x"], df["y"])
plt.title("Example Plot: y = sin(x)")
plt.xlabel("x")
plt.ylabel("y")
plt.grid(True)

plt.savefig("example_plot.png")
print("Plot saved to example_plot.png")
