import google.generativeai as genai

genai.configure(api_key="AIzaSyAsKZFN4WDqU4miwFHmq32aG9JqH1D9d0A")

models = genai.list_models()
for m in models:
    print(m.name)
