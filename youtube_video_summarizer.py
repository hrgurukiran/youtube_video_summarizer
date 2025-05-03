import requests
import json
import os
import re
from youtube_transcript_api import YouTubeTranscriptApi
from dotenv import load_dotenv
from urllib.parse import urlparse, parse_qs

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

# Function to get video title using YouTube oEmbed API (no auth needed)
def get_youtube_title(video_url):
    try:
        oembed_url = f"https://www.youtube.com/oembed?url={video_url}&format=json"
        response = requests.get(oembed_url)
        if response.status_code == 200:
            return response.json().get("title", None)
    except Exception as e:
        print(f"Error fetching title: {e}")
    return None

# Function to process text with Gemini API based on custom prompt
def process_with_gemini(text, api_key, user_prompt=None):
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
    headers = {
        "Content-Type": "application/json"
    }

    # Default prompt to generate key points and examples if user doesn't specify one
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

# Function to sanitize filename (remove illegal characters)
def sanitize_filename(name):
    return re.sub(r'[\\/*?"<>|]', "_", name)

if __name__ == "__main__":
    # Ask the user to enter the YouTube video URL
    video_url = input("Enter the YouTube video URL: ").strip()

    # Extract video ID from URL
    parsed_url = urlparse(video_url)
    query_params = parse_qs(parsed_url.query)
    video_id = query_params.get("v", [None])[0]

    if not video_id:
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

    # Attempt to fetch video title
    video_title = get_youtube_title(video_url)

    # If fetching title fails, generate one using Gemini based on the transcript
    if not video_title:
        print("\nCould not fetch video title. Using Gemini to generate one...")
        title_prompt = "Generate an appropriate and descriptive title for this YouTube video based on the transcript:\n" + transcript
        video_title = process_with_gemini(transcript, api_key, user_prompt=title_prompt)
        video_title = video_title.strip().split("\n")[0]  # Use first line as title

    # Sanitize title for filename usage
    output_filename = sanitize_filename(video_title) + ".txt"

    # Prompt the user for custom instructions
    print("\nWhat would you like to do with the transcript?")
    user_prompt = input("Enter your prompt or press Enter to auto-generate key points with examples: ").strip()
    user_prompt = user_prompt if user_prompt else None

    # Process transcript using Gemini
    output = process_with_gemini(transcript, api_key, user_prompt)

    # Save output to a .txt file
    with open(output_filename, "w", encoding="utf-8") as f:
        f.write(output)

    print(f"\nOutput saved to {output_filename}\n")
