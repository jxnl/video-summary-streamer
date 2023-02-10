# Youtube Summarizer
This FastAPI YouTube summary app utilizes two key features to improve speed and efficiency:

1. The app takes advantage of YouTube video transcripts, which can be easily retrieved via the YouTube Transcript API.
To tokenize the video text, the app uses regular expressions as a tokenizer, instead of using more complex natural language processing tools like spacy or nltk. The text is then divided into N_BATCH tokens and the summarization process is performed in parallel, with the results being combined at the end (MAP-REDUCE).

2. The summarized batches could be combined into a single batch, but this would result in a longer wait time for the first summary token to appear.

# Improving Whisper Transcriptions for Faster Summarization
One possible future improvement to the app (which would allow us to do all audio and all video) is to figure out how to stream whisper transcriptions, which would allow for faster summarization by summarizing the first n_tokens of the whisper transcriptions. This would result in a shorter wait time for the first summary token, bounded by the time to download the video and the time to produce the `n_tokens`.

# Running the App
To run the app, simply run the following commands:

```
pip install -r requirements.txt
# If you use poetry, run the following instead:
# poetry init
```

Then, navigate to the `summary_app` directory and run the following command:

```
uvicorn app:run:app --reload
```

# Calling the Streaming Endpoints
You can call the streaming endpoints using the following curl commands:

For regular streaming:

```
curl --no-buffer -X 'POST' \
  'http://127.0.0.1:8000/youtube'\
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer <OPENAI_API_TOKEN>' \
  -d '{
  "url": "https://www.youtube.com/watch?v=9Q9_CQxFUKY"
}'
```
For SSE with a [DONE] token:

```
curl --no-buffer -X 'POST' \
  'http://127.0.0.1:8000/youtube_sse'\
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer <OPENAI_API_TOKEN>' \
  -d '{
  "url": "https://www.youtube.com/watch?v=9Q9_CQxFUKY"
}'
```

# Future Work
1. Support for whisper transcriptions for all audio and video.
2. Streaming of whisper transcriptions for all audio and video.
3. A way to incorporate time stamps into the summary. (e.g. by including [t=12s] tokens?). In SSE, a possible implementation could be to return {data: data, is_time: bool}.