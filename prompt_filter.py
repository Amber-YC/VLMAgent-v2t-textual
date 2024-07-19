from openai import OpenAI
import json
from html_text_fetch import fetch_html
from resiliparse.extract.html2text import extract_plain_text


client = OpenAI(api_key="") # your own api_key

def get_plain_text(file_path, n):
    with open(file_path, 'r', encoding='utf-8') as file:
        for i, line in enumerate(file):
            if i == n - 1:
                data = json.loads(line)
                plain_text = data.get("plain_text", "")
                return plain_text
    return None

pos_file = "pos_texts.jsonl"
pos_exp = get_plain_text(pos_file, 1)
neg_file = "neg_texts.jsonl"
neg_exp = get_plain_text(neg_file, 1)

test_url = "https://www.amazon.sg/?&tag=googlepcabksg-22&ref=pd_sl_72dcplo99p_e&adgrpid=151972199943&hvpone=&hvptwo=&hvadid=673345669615&hvpos=&hvnetw=g&hvrand=12056086564015237948&hvqmt=e&hvdev=c&hvdvcmdl=&hvlocint=&hvlocphy=2702&hvtargid=kwd-10573980&hydadcr=2947_429125"
test_html = fetch_html(test_url)
test_text = extract_plain_text(test_html, main_content=False, links=False, skip_elements=['li'], noscript=True)

chat_completion = client.chat.completions.create(
    messages=[
        {"role": "system", "content": "You are a student in Department of Computer Science."},
        {
            "role": "user",
            "content": """Now you need to decide whether a website contains useful tutorials about how to use an OS system, a certain website or a certain app on pc according to the textual contents of its HTML. """ +
                        """ I will give you a positive example, a negative example, and some explanations.\ """
                        "POSITIVE EXAMPLE:" + pos_exp +
                        "NEGATIVE EXAMPLE:" + neg_exp +
                        "Here is the textual contents of the HTML which you need to analyze:" + test_text +
                        "please give me an answer: Y if it contains useful tutorials, N if not."
        }
    ],
    model="gpt-4")


reply = chat_completion.choices[0].message.content
print(f"ChatGPT: {reply}")

