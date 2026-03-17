from google import genai
from google.genai import types
import os

client = genai.Client(api_key = os.getenv("GEMINI_API_KEY"))


lyric_search_declaration = {
    "name": "lyric_search",
    "description": "Search for a song given a song lyric.",
    "parameters": {
        "type": "object",
        "properties": {
            "lyric": {
                "type": "string",
                "description": "The lyric that is used to search for and identify the song",
            },
        },
        "required": ["lyric"],
    },
}

def lyric_search(lyric: str) -> dict[str, str | int]:
    """Search for a song (mock API)."""
    return {"lyric": lyric}



tools = types.Tool(function_declarations=[lyric_search_declaration])
config = types.GenerateContentConfig(tools=[tools])


# Define user prompt
contents = [
    types.Content(
        role="user", parts=[types.Part(text="What song starts with 'Somebody once told me the world is gonna roll me.'")]
    )
]

# Send request with function declarations
response = client.models.generate_content(
    model="gemini-3-flash-preview",
    contents=contents,
    config=config
)

print(response.candidates[0].content.parts[0].function_call)


# Extract tool call details, it may not be in the first part.
tool_call = response.candidates[0].content.parts[0].function_call

if tool_call.name == "lyric_search":
    result = lyric_search(**tool_call.args)
    print(f"Function execution result: {result}")


# Create a function response part
function_response_part = types.Part.from_function_response(
    name=tool_call.name,
    response={"result": result},
)

# Append function call and result of the function execution to contents
contents.append(response.candidates[0].content) # Append the content from the model's response.
contents.append(types.Content(role="user", parts=[function_response_part])) # Append the function response

client = genai.Client()
final_response = client.models.generate_content(
    model="gemini-3-flash-preview",
    contents=contents,
    config=config
)

print(final_response.text)