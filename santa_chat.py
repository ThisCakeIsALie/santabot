import os
import requests
from dotenv import load_dotenv

load_dotenv()

# API Settings
BASE_API_URL = 'https://api.ai21.com/studio/v1/{}/complete'
SANTA_COMPLETION_SETTINGS = {
	'model': 'j1-jumbo',
	'api_key': os.getenv('AI21_API_KEY'),
	'max_tokens': 256,
	'temperature': 0.7,
	'stop_sequences': ['\n']
}

# Prompts
with open('santa_prompt.txt', 'r') as f:
	SANTA_BASE_PROMPT = f.read()

def construct_santa_prompt(history, new_user_input):
	prompt = SANTA_BASE_PROMPT

	for item in history:
		user_input, santa_response = item['input'], item['response']

		prompt += f"\nYou: {user_input}\nSanta: {santa_response}"

	prompt += f"\nYou: {new_user_input}\nSanta:"

	return prompt

def query_text_completion(prompt, **completion_settings):
	api_url = BASE_API_URL.format(completion_settings['model'])

	response = requests.post(
		api_url,
		headers = {"Authorization": f"Bearer {completion_settings['api_key']}"},
		json={
			"prompt": prompt,
			"numResults": completion_settings.get('num_results', 1),
			"maxTokens": completion_settings.get('max_tokens', 64),
			"stopSequences": completion_settings.get('stop_sequences', []),
			"topKReturn": completion_settings.get('top_k_return', 0),
			"temperature": completion_settings.get('temperature', 1.0)
		}
	)
	
	response_json = response.json()
	completions = response_json['completions']

	has_multiple_completions = len(completions) > 1

	if has_multiple_completions:
		return [completion['data']['text'].strip() for completion in completions.values()]
	else:
		return completions[0]['data']['text'].strip()

def generate_santa_response(new_user_input, history = []):
	prompt = construct_santa_prompt(history, new_user_input)
	completion = query_text_completion(prompt, **SANTA_COMPLETION_SETTINGS)

	return completion

if __name__ == '__main__':
	print(generate_santa_response('Sorry, what was the name again?', [
		{'input': 'Hi Santa, what is your name?', 'response': 'I am called Richard.'},
	]))