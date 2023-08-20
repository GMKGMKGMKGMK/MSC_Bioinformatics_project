import pandas as pd
import matplotlib.pyplot as plt
import sys

def generate_pie_chart(input_csv, output_filename=None):
    
    # Read the CSV data
    df = pd.read_csv(input_csv)

    # Filter out the "Total" row
    df = df[df["id"] != "Total"]

    # Define the colors and font properties
    colors = ['deepskyblue', 'red', 'green', 'purple']
    font_properties = {'fontsize': 10, 'fontweight': 'bold'}

    # Plot pie chart
    fig, ax = plt.subplots(figsize=(18, 9))
    ax.pie(df["percentage"], labels=df["species"], autopct='%1.1f%%', startangle=90, colors=colors, textprops=font_properties)
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.title("Percentage of Num Bases by Species", fontdict=font_properties)
    
    # Save the plot or display it
    if output_filename:
        plt.savefig(output_filename)
        print(f"Plot saved as {output_filename}")
    else:
        plt.show()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script_name.py input_csv [output_filename]")
        sys.exit(1)
        
    input_csv = sys.argv[1]
    output_filename = sys.argv[2] if len(sys.argv) > 2 else None
    generate_pie_chart(input_csv, output_filename)
