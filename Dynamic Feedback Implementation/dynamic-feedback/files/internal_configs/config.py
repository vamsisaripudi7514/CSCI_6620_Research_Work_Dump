dev_databases_path = 'database/dev_databases'
dev_json_path = 'data/dev.json'

# model='..' #gpt-4o or deepseek-coder
# api = '..'
base_url = 'http://'

# google_api_key = "AIzaSyB9GTBJp66n2IIYDtkPgGUpx0BW31RLnsI"
# google_api_key = "AIzaSyCvAST1xbF6SvXCx9Z21noqRC9gTHXL7C8"
# google_api_key = "AIzaSyAKX4LasDe3u7ORAn8F0oUzQPYAXpIlDDg"
# google_api_key = "AIzaSyDzrH17ZWRJZQz2xdUu8OzwHxiLsQ6DsEk"
google_api_key = "AIzaSyDT7kIrzXBGPxHxfvfXhUyqsteygXpc-g0"
generation_config = {
  "temperature": 0,              # updated temperature
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 65536,
  "response_mime_type": "application/json",  # set to return a JSON object
}
# model_name = "gemini-2.0-flash-thinking-exp-01-21"
# model_name = "gemini-2.5-pro-exp-03-25"
# model_name = "gemini-2.0-flash-lite"
# model_name = "gemini-2.0-flash"
model_name = "gemini-1.5-pro"