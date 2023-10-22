from textwrap import dedent
from langchain.prompts import PromptTemplate

SYSTEM_TEMPLATE = ""

STATE_EXTRACTION_TEMPLATE= '''
Given a text, I want you to extract what the major plot points are and place each of these events into a CSV format list. 
You should place them in chronological order, and assign each of them a time stamp depending on when they happen in the book.
These timestamps should be spaced at irregular intervals. So some would be closer together by timestamp than others, but they would NOT be spaced at regular intervals. 
Provide granular timestamps and detail on minor events in between major plot points as well. 
Timestamps should be unique to each event, and are arranged in increasing order according to the chronological order of the story. 
You should give each of these states an importance ranking of either No Importance, Low Importance, Medium Importance, High Importance, or Critical Importance. 
The importance should capture the role of the event in the overall story plot. 
This will provide a detailed timeline summary with importance annotations for analyzing events in a text. 
The output should be in the CSV format: Event,Time,Importance

For example:

Watson meets Holmes and agrees to share lodgings,0,Medium Importance

Days later they visit crime scene,3,High Importance

Your response should ONLY contain the list of states and NOTHING else. DO NOT INCLUDE ANY ADDITIONAL TEXT.

The CSV List:'''