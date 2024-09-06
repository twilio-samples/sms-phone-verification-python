"""
For the purposes of this tutorial, we will be hardcoding a list of accounts that are allowed to enter the website, along with their phone numbers. In a production setting, you would have to use your chosen database instead.

Keep in mind that if you were to use your own database, you would have to avoid storing passwords as plaintext. There are plenty of libraries that help developers manage passwords such as Flask Security.

The dictionary can be modified to include different emails and phone numbers as you please. Make sure the phone numbers are in E.164 format as seen in the settings.py example above. Be sure to add your phone number to an existing item in the dictionary, or create a new item with your information. Each username is a unique key which is helpful in our case because we want to look up the usernames quickly in the login step.
"""
KNOWN_PARTICIPANTS = {
  'herooftime@hyrule.com': "<YOUR_PHONE_NUMBER>",
  'zelda@hyrule.com': '+15551234567',
  'tetra@hyrule.com': '+15557654321'
}
