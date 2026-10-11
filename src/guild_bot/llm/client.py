import os
from google import genai
from guild_bot.llm.prompts import build_tldr_prompt,build_silesian_prompt
from google.genai import types

class LlmClient():

    def __init__(self, llm_model: str, llm_api_key: str):
        self.llm_model = llm_model
        self.llm_api_key = llm_api_key
        self.client = genai.Client(
            api_key=self.llm_api_key,
            http_options=types.HttpOptions(
                timeout=30_000,                                       # 30 s per request, in ms
                retry_options=types.HttpRetryOptions(attempts=2),     # 1 try + 1 retry
            ),
        )



    async def create_interaction(self, prompt):
        response = await self.client.aio.models.generate_content(
            model = self.llm_model,
            contents = prompt.contents,
            config = types.GenerateContentConfig(
                system_instruction = prompt.system_instruction,
            ),
        )
        return response.text

    async def llm_translate_to_silesian(self,message):
        prompt = build_silesian_prompt(message)
        return await self.create_interaction(prompt)

    async def llm_create_tldr(self,messages):
        prompt = build_tldr_prompt(messages)
        return await self.create_interaction(prompt)