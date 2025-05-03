# YouTube Video Transcript Processor using Google Gemini Flash API

This project provides a Python-based command-line tool that extracts the transcript from a YouTube video and allows users to interactively process the content using Google's Gemini 2.0 Flash API. The tool supports summarization, custom prompt-based processing, and default key-point generation with explanations.

## Features

- Extracts transcript text from any YouTube video (if available)
- Accepts custom input from the user to specify what to do with the transcript
- Uses Google Gemini 2.0 Flash API to:
  - Summarize the video content
  - Generate key bullet points with explanations and real-life examples
  - Respond to user-defined prompts
- Saves the processed output to a `.txt` file using the video ID as the filename

## Requirements

- Python 3.7 or higher
- Google Gemini API key
- Required Python libraries:
  - `requests`
  - `python-dotenv`
  - `youtube-transcript-api`

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/youtube-gemini-transcript.git
   cd youtube-gemini-transcript
