from google import genai
from google.genai import types
import os

client = genai.Client(api_key = os.getenv("GEMINI_API_KEY"))


control_thermostat_declaration = {
    "name": "control_thermostat",
    "description": "Increases or decreases the temperature of the thermostat.",
    "parameters": {
        "type": "object",
        "properties": {
            "temperature": {
                "type": "integer",
                "description": "The temperature the thermostat should be increased or decreased by.",
            },
        },
        "required": ["temperature"],
    },
}

def control_thermostat(temperature: int) -> dict[str, str | int]:
    """Increase or decrease the temperature in a room (mock API)."""
    return {"temperature": temperature}


tools = types.Tool(function_declarations=[control_thermostat_declaration])
config = types.GenerateContentConfig(tools=[tools])


# Define user prompt
contents = [
    types.Content(
        role="user", parts=[types.Part(text="Turn the temperature up on the thermostat 4 degrees")]
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

if tool_call.name == "control_thermostat":
    result = control_thermostat(**tool_call.args)
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