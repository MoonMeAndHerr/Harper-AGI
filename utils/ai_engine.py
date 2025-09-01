import os
import openai
OPENAI_KEY = os.environ.get('OPENAI_API_KEY')
if OPENAI_KEY:
    openai.api_key = OPENAI_KEY

def llm_generate(prompt: str, max_tokens: int = 200) -> str:
    if not OPENAI_KEY:
        return '(MOCK LLM) ' + ' '.join(prompt.split()[:30]) + ' ... (set OPENAI_API_KEY to enable full LLM)'
    try:
        resp = openai.ChatCompletion.create(
            model='gpt-4o-mini',
            messages=[{'role':'system','content':'You are a helpful marketing assistant.'},
                      {'role':'user','content':prompt}],
            max_tokens=max_tokens,
            temperature=0.7
        )
        return resp.choices[0].message.content.strip()
    except Exception as e:
        return f'[LLM ERROR: {e}]'

def mock_generate_post_ideas(company, audience, content_type, goals, platform, explanation):
    ideas = []
    for i in range(3):
        title = f'{company} {content_type} Tip {i+1}'
        caption = f'{title} — A quick tip for {audience}. Goals: {", ".join(goals)}.'
        hashtags = f'#{company.replace(" ","")} #{platform} #HarperAI'
        ideas.append({"title":title,"caption":caption,"hashtags":hashtags})
    return ideas
