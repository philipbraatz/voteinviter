try:
    from .config.config import WebsiteConfig, PrivateConfig
except:
    from config.config import WebsiteConfig, PrivateConfig

WEBSITECONFIG = WebsiteConfig()
PRIVATECONFIG = PrivateConfig()

try:
    from .website.webmain import WebMain
except:
    from website.webmain import WebMain