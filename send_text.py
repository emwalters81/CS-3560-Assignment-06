from google import genai
from google.genai import types
import os

client = genai.Client(api_key = os.getenv("GEMINI_API_KEY"))


send_message_declaration = {
    "name": "send_message",
    "description": "Sends a message to a contact.",
    "parameters": {
        "type": "object",
        "properties": {
            "contact": {
                "type": "string",
                "description": "The person who will receive the text message.",
            },
            "message": {
                "type": "string",
                "description": "The text message that will be sent to the contact.",
            },
        },
        "required": ["contact", "message"],
    },
}

def send_message(contact: str, message: str = "") -> dict[str, str | int]:
    """Send a message (mock API)."""
    return {"contact": contact, "message": message}



tools = types.Tool(function_declarations=[send_message_declaration])
config = types.GenerateContentConfig(tools=[tools])


# Define user prompt
contents = [
    types.Content(
        role="user", parts=[types.Part(text="Send Mom a Happy Birthday message.")]
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

result = None

if tool_call.name == "send_message":
    result = send_message(**tool_call.args)
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