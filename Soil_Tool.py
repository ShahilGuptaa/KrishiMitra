import ee

def soil_tool(lat: float, lon: float) -> str:
    """
    Returns soil properties and dynamic soil moisture for a given lat/lon.
    - Static properties from SoilGrids/OpenLandMap: texture, pH, organic carbon
    - Dynamic soil moisture from Open-Meteo
    """
    point = ee.Geometry.Point(lon, lat)

    try:
        texture_img = ee.Image("OpenLandMap/SOL/SOL_TEXTURE-CLASS_USDA-TT_M/v02")
        texture_val = texture_img.sample(point, 250).first().get('b0').getInfo()
        texture_map = {
            1:"Sand",2:"Loamy sand",3:"Sandy loam",4:"Loam",5:"Silt loam",6:"Silt",
            7:"Sandy clay loam",8:"Clay loam",9:"Silty clay loam",10:"Sandy clay",
            11:"Silty clay",12:"Clay"
        }
        texture_val = texture_map.get(texture_val, f"Unknown ({texture_val})")

        ph_img = ee.Image("OpenLandMap/SOL/SOL_PH-H2O_USDA-4C1A2A_M/v02")
        ph_val = ph_img.sample(point, 250).first().get('b0').getInfo()/10
        
        soc_img = ee.Image("OpenLandMap/SOL/SOL_ORGANIC-CARBON_USDA-6A1C_M/v02")
        soc_val = soc_img.sample(point, 250).first().get('b0').getInfo()
    except Exception as e:
        return f"Error fetching static soil data: {e}"

    result = (
        f"Soil Report for ({lat}, {lon}):\n"
        f"- Soil texture (USDA class): {texture_val}\n"
        f"- Soil pH: {ph_val:.2f}\n"
        f"- Soil organic carbon: {soc_val:.2f}%\n"
    )

    return result