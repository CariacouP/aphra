"""
Module for interacting with the model via the OpenRouter API.
"""

import logging
import toml
import requests
from openai import OpenAI

class LLMModelClient:
    """
    A client for interacting with the model via the OpenRouter API.
    """

    def __init__(self, config_file):
        """
        Initializes the LLMModelClient with the configuration from a file.

        :param config_file: Path to the TOML file containing the configuration.
        """
        self.clients = {}
        self.providers_config = {}
        self.default_provider = "openrouter"
        self.logging_configured = False
        
        self.load_config(config_file)

    def load_config(self, config_file_path):
        """
        Loads configuration from a TOML file and sets up the clients.

        :param config_file_path: Path to the TOML file.
        """
        try:
            with open(config_file_path, 'r', encoding='utf-8') as file:
                config = toml.load(file)
                
            # Load legacy [openrouter] config
            legacy_api_key = config.get('openrouter', {}).get('api_key', 'ollama')
            legacy_base_url = config.get('openrouter', {}).get('base_url', 'https://openrouter.ai/api/v1')
            
            self.providers_config['openrouter'] = {
                'api_key': legacy_api_key,
                'base_url': legacy_base_url
            }
            
            # Load the new [providers] block if it exists
            if 'providers' in config:
                for provider_name, provider_data in config['providers'].items():
                    self.providers_config[provider_name] = {
                        'api_key': provider_data.get('api_key', 'ollama'),
                        'base_url': provider_data.get('base_url', 'http://localhost:11434/v1')
                    }
                    
            # Instantiate OpenAI clients for each provider
            for provider_name, provider_config in self.providers_config.items():
                self.clients[provider_name] = OpenAI(
                    base_url=provider_config['base_url'],
                    api_key=provider_config['api_key']
                )

        except FileNotFoundError:
            logging.error('File not found: %s', config_file_path)
            raise
        except toml.TomlDecodeError:
            logging.error('Error decoding TOML file: %s', config_file_path)
            raise

    def call_model(self, system_prompt, user_prompt, model_name, *,
                   log_call=False, enable_web_search=False,
                   web_search_context="high", stream=False):
        """
        Calls the model with the provided prompts.

        :param system_prompt: The system prompt to set the context for the model.
        :param user_prompt: The user prompt to send to the model.
        :param model_name: The name of the model to use (can be prefixed with provider/ e.g., 'cloud/llama3').
        :param log_call: Boolean indicating whether to log the call details.
        :param enable_web_search: Boolean indicating whether to enable web search via OpenRouter.
        :param web_search_context: Context size for web search ('low', 'medium', 'high').
        :return: The model's response.
        """
        response = None
        try:
            # Determine provider and actual model name
            provider = self.default_provider
            actual_model_name = model_name
            
            if '/' in model_name:
                parts = model_name.split('/', 1)
                if parts[0] in self.clients:
                    provider = parts[0]
                    actual_model_name = parts[1]
                
            client = self.clients.get(provider)
            if not client:
                logging.error('No client configured for provider: %s', provider)
                raise ValueError(f"Provider '{provider}' is not configured.")

            # Prepare the request parameters
            request_params = {
                "model": actual_model_name,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                "max_tokens": 8192
            }

            base_url = self.providers_config[provider]['base_url']
            # Add web search capabilities if enabled (OpenRouter format)
            if enable_web_search and 'openrouter.ai' in base_url:
                # Append :online to model name for web search
                if not actual_model_name.endswith(":online"):
                    request_params["model"] = f"{actual_model_name}:online"

                # Add web search options
                request_params["web_search_options"] = {
                    "search_context_size": web_search_context
                }

            if stream:
                request_params["stream"] = True
                response = client.chat.completions.create(**request_params)
                response_content = ""
                chunk_count = 0
                for chunk in response:
                    if chunk.choices[0].delta.content is not None:
                        chunk_text = chunk.choices[0].delta.content
                        response_content += chunk_text
                        chunk_count += 1
                        if chunk_count % 5 == 0:
                            print('.', end='', flush=True)
                print()  # Add newline at the end
            else:
                response = client.chat.completions.create(**request_params)
                response_content = response.choices[0].message.content

            if log_call:
                self.log_model_call(user_prompt, response_content)

            return response_content
        except requests.exceptions.RequestException as exc:
            logging.error('Request error: %s', exc)
            raise
        except (ValueError, KeyError, TypeError) as exc:
            logging.error('Error parsing response: %s', exc)
            if response and hasattr(response, 'text'):
                logging.error('Response content: %s', response.text)
            else:
                logging.error('No response available')
            raise

    def log_model_call(self, user_prompt, response):
        """
        Logs the details of a model call to a log file.

        :param user_prompt: The user prompt sent to the model.
        :param response: The response received from the model.
        """
        if not self.logging_configured:
            logging.basicConfig(filename='aphra.log', level=logging.INFO,
                                format='%(asctime)s - %(levelname)s - %(message)s')
            self.logging_configured = True

        logging.info("\nUSER_PROMPT\n")
        logging.info(user_prompt)
        logging.info("\nRESPONSE\n")
        logging.info(response)
