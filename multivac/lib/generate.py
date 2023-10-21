from langchain.schema import (
    SystemMessage,
    AIMessage,
    HumanMessage
)
from multivac.lib.model import GPT
from multivac.lib.prompt import (
    SYSTEM_TEMPLATE,
)
import replicate

def generate_image(prompt, width=512, height=512):
    model = "doriandarko/sdxl-hiroshinagai:563a66acc0b39e5308e8372bed42504731b7fec3bc21f2fcbea413398690f3ec"
    input = {
        "prompt": prompt,
        "width": width,
        "height": height,
    }
    output = replicate.run(model,input=input)
    url = output[0]
    return url
