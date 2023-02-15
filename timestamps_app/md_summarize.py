import openai

PROMPT = """
You are a professional note taker and your job is to take this transcript and produce a comprehensive and informative markdown file for others to study. Your markdown file should make use of timestamps (when available) and clearly and concisely summarize the content of the transcript.

To format the markdown file, please follow this structure:

markdown:

    # [HH:MM:SS](https://youtu.be/video_id?t=XXs) Descriptive Title

    <A brief overview of the topic>

    **Subtitle**

    * Detailed description of key point 1, including any relevant information and insights.
    * Detailed description of key point 2, including any relevant information and insights.

    ...

When writing your markdown file, please keep in mind the following tips:

* Titles should be descriptive. Avoid using 2-3 word titles.
* After each header, leave a concise overview of the topic (2-3 sentences)
* Use bullet points for detailing important steps and insights. Be as detailed and comprehensive as possible.
* Avoid repeating yourself, in either the content or the timestamp.
* Cite and include timestamps whenever possible by linking to the relevant URL in a block. 


Content:

{text} 

Study Guide:
"""


async def summarize_transcript(
    txt, openai_api_key, semaphore=None, engine="text-davinci-003"
):
    if openai_api_key is not None:
        openai.api_key = openai_api_key

    async def call():
        response = await openai.Completion.acreate(
            engine=engine,
            prompt=PROMPT.format(text=txt),
            stream=True,
            max_tokens=1000,
            temperature=0,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0.6,
        )

        async def gen():
            async for chunk in response:
                yield chunk["choices"][0]["text"]
            yield "\n"

        return gen()

    if semaphore is None:
        return await call()

    async with semaphore:
        return await call()