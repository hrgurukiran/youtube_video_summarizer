import requests
import json
import os
from youtube_transcript_api import YouTubeTranscriptApi
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Function to extract video transcript from YouTube using the video ID
def get_youtube_transcript(video_id):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        full_text = " ".join([entry['text'] for entry in transcript])
        return full_text
    except Exception as e:
        print(f"Error fetching transcript: {e}")
        return None

# Function to process text with Gemini API based on custom prompt
def process_with_gemini(text, api_key, user_prompt=None):
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
    headers = {
        "Content-Type": "application/json"
    }

    # Default to generating key points with examples if user provides no prompt
    if user_prompt:
        prompt = f"{user_prompt}\n\n{text}"
    else:
        prompt = f"Generate key bullet points from the following text and explain each point with a simple example for better understanding:\n\n{text}"

    payload = {
        "contents": [{
            "parts": [{"text": prompt}]
        }]
    }
    params = {
        "key": api_key
    }

    response = requests.post(url, headers=headers, params=params, data=json.dumps(payload))

    if response.status_code == 200:
        result = response.json()
        try:
            return result['candidates'][0]['content']['parts'][0]['text']
        except:
            return "Failed to extract output from response."
    else:
        return f"Request failed with status code {response.status_code}: {response.text}"

if __name__ == "__main__":
    # Ask the user to enter the YouTube video link
    video_url = input("Enter the YouTube video URL: ").strip()

    # Extract the video ID from the URL
    if "v=" in video_url:
        video_id = video_url.split("v=")[-1].split("&")[0]
    else:
        print("Invalid YouTube video URL.")
        exit(1)

    # Load Gemini API key from .env file
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY not found in .env file.")
        exit(1)

    # Fetch transcript
    transcript = get_youtube_transcript(video_id)
    if not transcript:
        print("Transcript not available.")
        exit(1)

    # Prompt the user for custom input
    print("\nWhat would you like to do with the transcript?")
    user_prompt = input("Enter your prompt or press Enter to auto-generate key points with examples: ").strip()
    user_prompt = user_prompt if user_prompt else None

    # Process transcript using Gemini
    output = process_with_gemini(transcript, api_key, user_prompt)

    # Save the output to a .txt file
    output_filename = f"{video_id}_summary.txt"
    with open(output_filename, "w", encoding="utf-8") as f:
        f.write(output)

    print(f"\nOutput saved to {output_filename}\n")
