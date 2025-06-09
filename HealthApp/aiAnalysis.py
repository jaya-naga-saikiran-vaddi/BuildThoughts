import openai

import Constants

openai.api_key = Constants.OPENAI_API_KEY


def get_gpt_advice(summary_stats: str) -> str:
    prompt = f"""
    Here is the user's recent health summary:
    {summary_stats}

    Please provide personalized health advice based on this data.
    """

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    advice = response.choices[0].message['content'].strip()
    return advice
