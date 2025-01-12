import os
import glob
import requests
import pandas as pd

# Define the API URL
API_URL = "http://localhost:8001/asr"

# Path to mp3 files
CV_DIR = "./cv-valid-dev/*.mp3"

# Output file to store transcription results
OUTPUT_FILE = "./cv-valid-dev.csv"


def transcribe_audio(file_path):
    """
    Sends the audio file to the FastAPI transcription service and returns the transcription.
    
    Args:
        file_path (str): Path to the mp3 file.
        
    Returns:
        dict: Transcription result including text and duration.
    """
    with open(file_path, "rb") as audio_file:
        files = {
            "file": (os.path.basename(file_path), audio_file, "audio/mpeg")
        }
        try:
            # Send the file to the API
            response = requests.post(API_URL, files=files)
            if response.status_code == 200:
                return response.json()  # Return the transcription result as JSON
            else:
                print(f"Error with file {file_path}: {response.status_code}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"Request failed for file {file_path}: {e}")
            return None
        

def process_directory(cv_dir):
    """
    Processes all MP3 files in the specified directory and transcribes them.
    
    Args:
        cv_dir (str): Path to the directory containing MP3 files.
        
    Returns:
        list: A list of transcription results.
    """

    # To store results
    transcriptions = []

    # Loop through every mp3 file
    for file_path in glob.glob(cv_dir):
        print(f"Processing {file_path}...")
        transcription = transcribe_audio(file_path)
        if transcription:
            transcriptions.append({
                "file_name": file_path.split('\\')[-1],
                "generated_text": transcription["transcription"],
                "duration": transcription["duration"]
            })
    return transcriptions


def save_results(results, output_file):
    """
    Save the transcription results to a CSV file.
    
    Args:
        results (list): List of transcription results.
        output_file (str): Path to the output CSV file.
    """

    # Convert results into a DataFrame
    results_df = pd.DataFrame(results)

    # Read the original csv file
    original_df = pd.read_csv(output_file)

    # Create file_name column for merging purpose, also drop duration and generated_text columns if they exist
    original_df['file_name'] = original_df['filename'].apply(lambda x: x.split('/')[-1])
    drop_cols = ['duration','generated_text']
    for col in drop_cols:
        if col in original_df.columns:
            original_df.drop(col, axis=1, inplace=True)

    # Merge transcription results to original_df
    final_df = original_df.merge(results_df, on='file_name', how='left')
    final_df.drop('file_name', axis=1, inplace=True)
    
    # Output
    final_df.to_csv(output_file, index=False)


if __name__ == "__main__":
    # Process the files and get transcriptions
    transcriptions = process_directory(CV_DIR)
    
    # Save the transcription results
    save_results(transcriptions, OUTPUT_FILE)

    print(f"Processing complete. Transcriptions saved to {OUTPUT_FILE}.")