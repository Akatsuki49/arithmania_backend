from openai import OpenAI
client = OpenAI(api_key="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")

response = client.images.generate(
  model="dall-e-3",
  prompt="a cartoon man dressed as a banker, 3d, in the style of an animated GIF, clean and simple design, facing front",
  size="1024x1024",
  quality="hd",
  n=1,
)

image_url = response.data[0].url
print(image_url)