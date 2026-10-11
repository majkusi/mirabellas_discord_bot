import os
from dataclasses import dataclass
from dotenv import load_dotenv


@dataclass
class Config:
    llm_api_key: str
    llm_model: str
    discord_token: str
    discord_guild_id: str


def load_config() -> Config:
    load_dotenv()
    return Config(llm_model=os.environ["LLM_MODEL"], 
                  llm_api_key=os.environ["LLM_API_KEY"],
                  discord_token=os.environ["DISCORD_TOKEN"],
                  discord_guild_id=os.environ["DISCORD_GUILD_ID"])