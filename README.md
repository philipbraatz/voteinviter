# VoteInviter    [![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/) [![PyPI pyversions](https://img.shields.io/badge/discord-green)](https://pypi.python.org/pypi/ansicolortags/) [![PyPI pyversions](https://img.shields.io/badge/requests-yellowgreen)](https://pypi.python.org/pypi/ansicolortags/) [![PyPI pyversions](https://img.shields.io/badge/python-dotenv-yellowgreen)](https://pypi.python.org/pypi/ansicolortags/) [![PyPI pyversions](https://img.shields.io/badge/SQLite3-yellowgreen)](https://pypi.python.org/pypi/ansicolortags/)

A Discord bot that allows Discord users to request to join your **private** discord guild from an **external website**. Requests can be looked reviewed by staff and then be put to a **secure vote** by the existing members in your guild.

* Webhook informs staff when new users request an invite
  * Staff can approve, "Quick approve", or deny them
* Discord bot handles voting securely by hiding reactions as they come in
  * Reactions are removed and Vote is updated in the message
* Website gets updated with votes as they come in
---


- [x] Implemented
- [ ] Needs implementing
---
## Setup
1. pip install -r **requirements.txt**
2. create a **.env** file in the root directory, and fill it with
   1. BOT_TOKEN=my_bot_token_here
   2. CLIENT_ID=my_bot_client_id_here
   3. OAUTH_CLIENT_TOKEN=my_oath_token_here
   4. WEBHOOK_ID=id_for_my_webhook_here
   5. API_KEY=any_secrect_value_used_for_api
   6. WEBSITE_SECRET_KEY=any_secrect_value
3. Configure **botconfig.ini** for the bot
   1. Update [Bot] Section to your guilds id's
      1. master_server - Server hosting the votes
      2. voting_channel - Channel where users will vote
      3. welcome_channel - Discord Welcome channel
      4. staff_role - Role used to access commands
   2.  [ ] vote_ping - Users with this role will be pinged when a vote starts
      5. [ ] welcome_message - Welcome the user that has been voted in
4. Configure **webconfig.ini** for the website
   1. You can probably leave this alone
   2. Defaults to debug mode on localhost port 80
5. Run both bot and website in any order
   1. Run the website 
        > python app.py web
   2. Run the bot
        > python app.py bot
## Configurability
* [ ] Pass the vote 
  * [ ] by percentage (75% positive to 25% negative)
     * [ ] Minimal difference in percentage
  * [x] by number of votes (3 more votes positive than negative) 
     * [x] Minimal difference in vote count
* [x] Minimal number of votes to pass
* [x] How long before the invite link expires
* [ ] Command prefix

## Commands
#### Commands are only useable by users with the "staff" role

|command prefix **!v**|
---
* Help
  * [x] invite
    * Gives you a link straight to sign-up
  * [x] link
    * Shares the link to the site
* Voting
  * [ ] stop
    * Force stop an active vote
  * [ ] quick
    * Toggles "Quick voting"
* Admin - only useable with "admin" role
  * [ ] manualinv
    * DM a manually created an invite
  
