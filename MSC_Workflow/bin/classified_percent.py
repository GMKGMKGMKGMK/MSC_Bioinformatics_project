import os
import sys
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def full_script_with_args():
    # Check and get command-line arguments
    if len(sys.argv) != 3:
        print("Usage: python combined_plot.py <input_directory> <output_directory>")
        sys.exit(1)
    
    input_directory = sys.argv[1]
    output_directory = sys.argv[2]

    def get_classified_percentage(filepath):
        df = pd.read_csv(filepath)
        total_reads = df['Num_Reads'].sum()
        classified_reads = df[df['Bacterium'] != 'unclassified']['Num_Reads'].sum()
        return (classified_reads / total_reads) * 100

    def plot_combined_data(data, output_folder, filename):
        # Convert the nested dictionary to a DataFrame
        df = pd.DataFrame(data).transpose().reset_index()
        df = df.melt(id_vars=["index"], var_name="Condition", value_name="Percentage")
        df.columns = ["Species", "Condition", "Percentage"]
        
        plt.figure(figsize=(12, 18))
        sns.set_style("white")
        plt.gca().set_facecolor('#F2F2F2')
        
        ax = sns.barplot(data=df, y="Species", x="Percentage", hue="Condition", dodge=True, edgecolor="black", linewidth=1.2)
        
        plt.xlabel('Percentage of Classified Reads')
        plt.title('Percentage of Classified Reads for All Species')
        plt.xlim(0, 110)
        
        # Annotating the bars
        for p in ax.patches:
            ax.annotate('{:.2f}%'.format(p.get_width()), 
                        (p.get_width() + 2, p.get_y() + p.get_height() / 2.),
                        va='center', fontweight='bold', color='black', size=9)
        
        plt.legend(title="Basecallers", bbox_to_anchor=(1, 1))
        plt.grid(axis='x', linestyle='-', linewidth=0.7, alpha=0.7)
        
        # Set x-axis ticks from 1 to 100 in steps of 5
        plt.xticks(range(0, 105, 5))
        
        plt.tight_layout()
        plt.savefig(os.path.join(output_folder, filename + '.png'), bbox_inches='tight')  # Save with tight bounding box
        plt.close()

    def main_combined(input_folder, output_folder):
        # Get all CSV files in the directory
        files = [f for f in os.listdir(input_folder) if f.endswith('.csv')]
        
        # Categorizing files based on species names
        species_categories = ['Ecoli', 'MRSA', 'Pa01', 'Kpneu']
        
        # Color mapping for conditions
        condition_colors = {
            'r9HAC': '#FF5733',  # Red
            'r9SUP': '#3498DB',  # Blue
            'r10DOR': '#27AE60',  # Green
            'r10DUP': '#1ABC9C',  # Turquoise
            'r10SUP': '#9B59B6',  # Purple
            'simulated': '#E74C3C'  # Alt/Red
        }
        
        # Desired order for conditions
        desired_order = ['r9HAC', 'r9SUP', 'r10SUP', 'r10DUP', 'r10DOR','simulated']
        
        combined_data = {}
        
        for species in species_categories:
            species_files = [f for f in files if species in f]
            species_data = {}
            for file in species_files:
                condition = file.split('_')[3].split('.')[0]
                species_data[condition] = get_classified_percentage(os.path.join(input_folder, file))
            
            # Sorting the dictionary based on the desired order
            ordered_species_data = {condition: species_data[condition] for condition in desired_order if condition in species_data}
            
            combined_data[species] = ordered_species_data
        
        plot_combined_data(combined_data, output_folder, "combined")
    
    # Executing the main function
    main_combined(input_directory, output_directory)

# Call the main function
full_script_with_args()
