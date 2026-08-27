import os
from google import genai
from google.genai import types
from groq import Groq
from dotenv import load_dotenv
from src.math_solver import solve_math
from src.critical_thinking import critical_thinking_response
from src.web_search import search_web
from src.knowledge import get_knowledge_summary

load_dotenv()

GROQ_MODELS = [
    "llama3-70b-8192",
    "llama-3.1-8b-instant",
    "mixtral-8x7b-32768",
    "gemma2-9b-it"
]

GEMINI_MODELS = [
    "models/gemini-2.0-flash-lite",
    "models/gemini-2.0-flash-001",
    "models/gemini-flash-latest",
]

# ── API Clients ──
gemini_client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# ── Conversation History ──
conversation_history = []
MAX_HISTORY = 15

# ── Track which AI is active ──
current_ai = "gemini"  # Start with Gemini

SYSTEM_PROMPT = """
You are TAM — Thoughtful Adaptive Mind 🤖
You are Soud's personal AI assistant, built to answer questions about Soud
(his skills, projects, education, experience) and also help visitors with
general questions, math, code, and more.

Your personality:
- Friendly, warm and encouraging
- Sharp and highly intelligent
- Patient when explaining complex topics
- Speaks clearly and simply

Your capabilities:
- Answer questions about Soud using his knowledge base
- Solve mathematics step by step
- Help with critical thinking and logic
- Answer general knowledge questions
- Write, explain and debug code
- Search the web for current information
- Read and analyze uploaded files
- Speak out loud using voice mode (click 🎙️ in header to activate)

Rules:
- Only introduce yourself when asked who you are
- Never start every reply with your name or introduction
- Never say you are ChatGPT or any other AI
- Always think step by step before answering
- End difficult answers with "Hope that helps! — TAM 💡"
- Never mention knowledge cutoff dates
- NEVER share Soud's phone number or personal address directly
- If asked for contact info, always share Soud's LinkedIn URL
- You CAN mention Soud's email if specifically relevant
- When asked about Soud, answer ONLY using the knowledge base
- If knowledge base doesn't have the answer say "I don't have that information about Soud yet — feel free to ask him directly!"
- Never make up facts about Soud
- For general questions about companies, people, places — answer using web search or your knowledge
"""


def gemini_stream(messages, full_system_prompt):
    global current_ai
    try:
        # Build contents list OUTSIDE generate()
        contents = []
        last_user_msg = ""

        for i, msg in enumerate(messages):
            if msg["role"] == "system":
                continue
            elif msg["role"] == "user":
                last_user_msg = msg["content"]
                if i < len(messages) - 1:
                    contents.append(
                        types.Content(
                            role="user",
                            parts=[types.Part.from_text(text=msg["content"])]
                        )
                    )
            elif msg["role"] == "assistant":
                contents.append(
                    types.Content(
                        role="model",
                        parts=[types.Part.from_text(text=msg["content"])]
                    )
                )

        # Add final user message
        contents.append(
            types.Content(
                role="user",
                parts=[types.Part.from_text(text=last_user_msg)]
            )
        )

        # Build config OUTSIDE generate()
        gen_config = types.GenerateContentConfig(
            system_instruction=full_system_prompt,
            max_output_tokens=1000,
            temperature=0.7,
        )

        current_ai = "gemini"

        def generate():
            full_response = ""
            try:
                response = gemini_client.models.generate_content_stream(
                    model="models/gemini-flash-latest",
                    contents=contents,
                    config=gen_config
                )
                for chunk in response:
                    if chunk.text:
                        full_response += chunk.text
                        yield chunk.text

            except Exception as e:
                error_msg = str(e)
                print(f"Gemini inner error: {error_msg}")

                # Switch to Groq and yield its response
                print("🔄 Switching to Groq backup...")
                global current_ai
                current_ai = "groq"

                try:
                    groq_result, _ = groq_stream(messages, full_system_prompt)
                    for chunk in groq_result:
                        full_response += chunk
                        yield chunk
                except Exception as groq_error:
                    yield "⏳ Both AI systems are busy. Please try again in a few minutes! — TAM 💡"

            if full_response:
                conversation_history.append({
                    "role": "assistant",
                    "content": full_response
                })
                if len(conversation_history) > MAX_HISTORY:
                    conversation_history.pop(0)

        return generate(), True

    except Exception as e:
        error_msg = str(e)
        print(f"Gemini error: {error_msg}")
        print("🔄 Switching to Groq...")
        current_ai = "groq"
        return groq_stream(messages, full_system_prompt)


# ── Groq Stream Response (Backup) ──
def groq_stream(messages, full_system_prompt):
    global current_ai
    try:
        # Add system prompt to messages
        full_messages = [
            {"role": "system", "content": full_system_prompt},
            *[m for m in messages if m["role"] != "system"]
        ]

        stream = groq_client.chat.completions.create(
            model="llama3-70b-8192",
            messages=full_messages,
            temperature=0.7,
            max_tokens=1000,
            stream=True
        )

        current_ai = "groq"

        def generate():
            full_response = ""
            for chunk in stream:
                delta = chunk.choices[0].delta.content
                if delta:
                    full_response += delta
                    yield delta
            conversation_history.append({
                "role": "assistant",
                "content": full_response
            })
            if len(conversation_history) > MAX_HISTORY:
                conversation_history.pop(0)

        return generate(), True

    except Exception as e:
        error_msg = str(e)
        print(f"Groq error: {error_msg}")

        if any(x in error_msg.lower() for x in
               ['quota', 'rate', '429', 'limit', 'exceeded']):
            raise Exception(
                "⏳ Both AI systems have reached their daily limits! "
                "Please try again in 30 minutes. — TAM 💡"
            )
        raise e


# ── Main Stream Router ──
def stream_response(messages, full_system_prompt):
    global current_ai
    if current_ai == "gemini":
        return gemini_stream(messages, full_system_prompt)
    else:
        return groq_stream(messages, full_system_prompt)


# ── Main Chat Function ──
def chat(user_message, file_content=None):

    # Save user message to history
    conversation_history.append({
        "role": "user",
        "content": user_message
    })
    if len(conversation_history) > MAX_HISTORY:
        conversation_history.pop(0)

    # Build knowledge context
    knowledge = get_knowledge_summary()
    full_system_prompt = SYSTEM_PROMPT
    if knowledge:
        full_system_prompt += "\n\n" + knowledge

    if file_content:
        # Check if question is about the file
        file_keywords = ['file', 'document', 'pdf', 'uploaded', 'this',
                        'summarize', 'explain', 'read', 'content',
                        'what does', 'what is in', 'key points']

        is_about_file = any(word in user_message.lower()
                           for word in file_keywords)

        if is_about_file:
            prompt = f"""The user has uploaded a document:

---START OF DOCUMENT---
{file_content}
---END OF DOCUMENT---

User asks: {user_message}

Read the document carefully and answer based on its content.
"""
            messages = [
                {"role": "system", "content": full_system_prompt},
                *conversation_history[:-1],
                {"role": "user", "content": prompt}
            ]
            return stream_response(messages, full_system_prompt)

    # Check math
    if any(word in user_message.lower() for word in
           ['solve', 'calculate', 'math', 'equation',
            'integral', 'derivative', 'factor']):
        math_result = solve_math(user_message)
        if math_result:
            return f"🔢 Math Result:\n{math_result}\n\nHope that helps! — TAM 💡", False

    # Check critical thinking
    if any(word in user_message.lower() for word in
           ['fallacy', 'puzzle', 'riddle', 'analyze',
            'argument', 'debate', 'logic problem']):
        ct_result = critical_thinking_response(user_message)
        if ct_result:
            return ct_result, False

    # Check web search
    web_triggers = [
        'latest', 'news', 'today', 'breaking',
        'right now', 'live', 'trending',
        'score', 'won', 'winner', 'match result',
        'cricket', 'ipl', 'fifa', 'world cup',
        'current price', 'stock price', 'weather',
        'election result', 'recently happened',
        'search for', 'look up', 'find info about',
        'what happened in 2026', 'news about',
        'latest news about', 'recent update'
    ]

    should_search = False
    msg_lower = user_message.lower()
    for trigger in web_triggers:
        if trigger in msg_lower:
            should_search = True
            break

    if should_search:
        search_result = search_web(user_message)
        if search_result:
            history_context = conversation_history[:-1] if len(conversation_history) > 1 else []
            messages = [
                {"role": "system", "content": full_system_prompt},
                *history_context,
                {"role": "user", "content": f"""Answer this question: {user_message}

Here is the latest information from the web:
{search_result}

Instructions:
- Give a clear direct answer first
- Use the web data above to answer accurately
- Keep it conversational and helpful
- Mention the source URLs at the end
- Don't show raw HTML or markdown link syntax"""}
            ]
            return stream_response(messages, full_system_prompt)

    # Normal conversation with history
    messages = [
        {"role": "system", "content": full_system_prompt},
        *conversation_history
    ]
    return stream_response(messages, full_system_prompt)


def get_current_ai():
    return current_ai
