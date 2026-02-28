import api.API_KEY as api_key
from .models import Product
import google.generativeai as genai
import json
import os

genai.configure(api_key=api_key.API_KEY)
model = genai.GenerativeModel("gemini-1.5-pro")

# Your input data (could be a string, CSV contents, etc.)
input_data = Product.get.all.values_list()

categories = """
gifting
knit tops
denim
dresses
sweaters
woven tops
bottoms
footwear
skirts
accessories
outerwear
sweatshirts
"""

result = model.generate_content(
    f"Convert this data into a structured list of product name with the category: {input_data} {categories}",
    generation_config=genai.GenerationConfig(
        response_mime_type="application/json",
        response_schema={
            "type": "array",
            "items": {
                "prod_name": "string",
                "category": "string"
                }
            }
    )
)

# Parse and save to a JSON file
data = json.loads(result.text)

with open("categories.json", "w") as f:
    json.dump(data, f, indent=2)

print("Saved!")