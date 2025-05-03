# YouTube Transcript Processor with Google Gemini Flash API

This Python script provides a simple and interactive way to extract and process YouTube video transcripts using the Google Gemini 2.0 Flash API. Users can choose to generate summaries, ask custom questions, or receive structured key points with examples—ideal for learning, content research, or knowledge extraction.

## Features

- Extracts transcripts from YouTube videos (if captions are publicly available)
- Prompts user to choose how they want to process the transcript
- Integrates with Google Gemini Flash API for high-quality content generation
- Automatically generates a descriptive title if YouTube metadata is unavailable
- Saves processed results in a text file named after the video title

## Requirements

- Python 3.7+
- [Google Gemini API Key](https://aistudio.google.com/app/apikey)
- YouTube videos must have available transcripts

## Dependencies

Install required Python packages:

```bash
pip install -r requirements.txt
