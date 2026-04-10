from google import genai

client = genai.Client(api_key="API_KEY")

while True:
    input = input("User: ").strip()
    if not input:
        break

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=input,
    )

    print(f"Gemini: {response.text}\n")