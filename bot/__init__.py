try:
    from ..config.config import WebsiteConfig, PrivateConfig
except:
    from config.config import WebsiteConfig, PrivateConfig

PRIVATECONFIG = PrivateConfig()
BOTCONFIG     = BotConfig()