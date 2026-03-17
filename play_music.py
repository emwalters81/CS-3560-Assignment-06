from google import genai
from google.genai import types
import os

client = genai.Client(api_key = os.getenv("GEMINI_API_KEY"))


play_music_declaration = {
    "name": "play_music",
    "description": "Plays music in a specified room.",
    "parameters": {
        "type": "object",
        "properties": {
            "room": {
                "type": "string",
                "description": "Room where the music should play.",
            },
            "genre": {
                "type": "string",
                "description": "Genre of music to play.",
            },
            "volume": {
                "type": "integer",
                "description": "Volume level from 0 to 100.",
            },
        },
        "required": ["room", "genre"],
    },
}

def play_music(room: str, genre: str, volume: int = 50) -> dict[str, str | int]:
    """Play music in a room (mock API)."""
    return {"room": room, "genre": genre, "volume": volume}


tools = types.Tool(function_declarations=[play_music_declaration])
config = types.GenerateContentConfig(tools=[tools])


# Define user prompt
contents = [
    types.Content(
        role="user", parts=[types.Part(text="Play some rock music in the living room at 70 volume")]
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

if tool_call.name == "play_music":
    result = play_music(**tool_call.args)
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