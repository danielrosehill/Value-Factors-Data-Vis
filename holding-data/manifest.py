import pandas as pd
import os

def generate_markdown_manifest_for_all_csvs():
    # Get the current working directory
    current_dir = os.getcwd()
    
    # Create a folder called 'params' within the current directory to store the markdown manifests
    output_folder = os.path.join(current_dir, 'params')
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Get a list of all CSV files in the current directory
    csv_files = [f for f in os.listdir(current_dir) if f.endswith('.csv')]
    
    if not csv_files:
        print("No CSV files found in the current directory.")
        return

    # Loop through each CSV file and generate a manifest in markdown format
    for csv_file in csv_files:
        try:
            # Load CSV file into a pandas DataFrame
            csv_path = os.path.join(current_dir, csv_file)
            df = pd.read_csv(csv_path)

            # Prepare the manifest content
            markdown_content = f"# Manifest for {csv_file}\n\n"
            markdown_content += f"## Column Overview\n\n"

            for col in df.columns:
                # Skip the "Value" column
                if col == "Value":
                    continue

                unique_values = df[col].dropna().unique()
                markdown_content += f"### {col}\n\n"
                markdown_content += "Parameters:\n\n"
                for val in unique_values:
                    markdown_content += f"- {val}\n"
                markdown_content += "\n"

            # Generate the output filename for the markdown manifest
            output_file = os.path.join(output_folder, f"{os.path.splitext(csv_file)[0]}_manifest.md")
            
            # Write the markdown content to the file
            with open(output_file, 'w') as f:
                f.write(markdown_content)

            print(f"Manifest for {csv_file} saved to {output_file}")

        except Exception as e:
            print(f"Error processing {csv_file}: {e}")

# Run the function
generate_markdown_manifest_for_all_csvs()
