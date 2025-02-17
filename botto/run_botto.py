import os
import json
import logging.config

from tld_botto import TLDBotto
from config import parse

# Configure logging
logging.config.fileConfig(fname="log.conf", disable_existing_loggers=False)
logging.getLogger("discord").setLevel(logging.CRITICAL)
logging.getLogger("discord.gateway").setLevel(logging.INFO)
logging.getLogger("asyncio").setLevel(logging.CRITICAL)
logging.getLogger("urllib").setLevel(logging.CRITICAL)
log = logging.getLogger("TLDBotto")

try:
    config_path = os.getenv("MOTTOBOTTO_CONFIG", "config.json")
    log.debug(f"Config path: %s", config_path)
    config = parse(json.load(open(config_path)))
except (IOError, OSError, ValueError) as err:
    log.error(f"Config file invalid: {err}")
    exit(1)

log.info(f"Triggers: {config['triggers']}")

client = TLDBotto(config)
client.run(config["authentication"]["discord"])
