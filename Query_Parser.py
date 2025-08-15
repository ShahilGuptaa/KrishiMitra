from langchain.output_parsers import StructuredOutputParser, ResponseSchema
from langchain.prompts import PromptTemplate
from utils import llm 

def extract_farm_info(farmer_input: str):
    response_schemas = [
        ResponseSchema(
        name="location",
        description="Location of the farm (village, district, state, etc.)"),
        ResponseSchema(name="state", description="State where the farm is located. Use the location information to locate the indian state"),
        ResponseSchema(name="crop_type", description="Type of crop being grown")
    ]

    output_parser = StructuredOutputParser.from_response_schemas(response_schemas)
    format_instructions = output_parser.get_format_instructions()

    prompt = PromptTemplate(
        template="""
    You are an assistant that extracts structured agricultural data from farmer queries. Always translate the laguage of the query into English.

    Farmer's Input:
    {farmer_input}

    {format_instructions}

    Make sure:
    - "location" is just the location.
    - "state" is the state name, not the full address.
    - "crop_type" is only the crop name.
    If information is missing, put "unknown".
    """,
        input_variables=["farmer_input"],
        partial_variables={"format_instructions": format_instructions},
    )
    try:
        _input = prompt.format_prompt(farmer_input=farmer_input)
        output = llm(_input.to_messages()).content
        
        # Try to parse into dict
        parsed = output_parser.parse(output)
        
        # Fallback handling if fields are missing
        for key in ["location", "state", "crop_type"]:
            if key not in parsed or not parsed[key].strip():
                parsed[key] = "unknown"
                
        return parsed
    
    except Exception as e:
        return {
            "query": "unknown",
            "location": "unknown",
            "crop_type": "unknown",
            "error": str(e)
        }