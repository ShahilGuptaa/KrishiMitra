import ee

# Initialize Earth Engine
try:
    if not ee.data._initialized:
        ee.Initialize(project='ee-guptashahil')
        print("Google Earth Engine initialized successfully")
except Exception as e:
    print("Earth Engine not authenticated. Please run 'ee.Authenticate()' once in terminal.")
    raise e
