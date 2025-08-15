from langchain.schema import HumanMessage
from utils import llm
from Address_Convertor import get_location
from Mandi_Price_Tool import get_state_data
from Query_Parser import extract_farm_info
from weather_tool import weather_openmeteo
from Soil_Tool import soil_tool

def get_farming_advice(location, state, crop, soil, weather, mandi_price, farmer_query):
    """
    location: dict with keys 'village', 'district', 'state', 'lat', 'lon'
    crop: str, crop name
    soil: dict with keys like 'texture', 'ph', 'organic_carbon'
    weather: dict with keys like 'temperature', 'rainfall', 'humidity', 'forecast'
    farmer_query: str, the question farmer is asking
    """

    # Construct structured prompt
    prompt = f"""
    You are an expert agronomist and agricultural advisor. Answer the farmer's question
    based on the following information. Be concise, actionable, and practical.

    Location: {location}
    State: {state}
    Crop: {crop}
    Soil: {soil}
    Weather: {weather}
    Mandi Price: {mandi_price}
    Farmer's Question: {farmer_query}

    Provide:
    1. Practical recommendation
    2. Explanation (brief)
    3. Any cautions or best practices
    """

    # LangChain LLM call
    response = llm([HumanMessage(content=prompt)])
    return response.content

def agent(query: str)->str:
    structured_input = extract_farm_info(query)
    crop = structured_input.get("crop_type", "unknown")
    state = structured_input.get("state", "unknown")
    location = structured_input.get("location", "unknown")
    farmer_query = query
    print(f"Extracted Crop: {crop}, State: {state}, Location: {location}")

    if location == "unknown":
        return "Unable to provide advice without crop and location information."
    
    lat, lon = get_location(location)
    soil = soil_tool(lat, lon)
    weather = weather_openmeteo(lat, lon)
    mandi_price = get_state_data(state)

    print(lat, lon, soil, weather, mandi_price)

    return get_farming_advice(location, state, crop, soil, weather, mandi_price, farmer_query)
    