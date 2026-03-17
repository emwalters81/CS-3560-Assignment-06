from google import genai
from google.genai import types
import os

client = genai.Client(api_key = os.getenv("GEMINI_API_KEY"))


set_timer_declaration = {
    "name": "set_timer",
    "description": "Sets a timer for a given number of minutes.",
    "parameters": {
        "type": "object",
        "properties": {
            "minutes": {
                "type": "integer",
                "description": "Duration of the timer in minutes.",
            },
        },
        "required": ["minutes"],
    },
}

def set_timer(minutes: int) -> dict[str, str | int]:
    """Set a timer (mock API)."""
    return {"minutes": minutes}



tools = types.Tool(function_declarations=[set_timer_declaration])
config = types.GenerateContentConfig(tools=[tools])


# Define user prompt
contents = [
    types.Content(
        role="user", parts=[types.Part(text="Set a timer for 20 minutes.")]
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

if tool_call.name == "set_timer":
    result = set_timer(**tool_call.args)
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