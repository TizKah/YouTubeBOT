# YouTube Bot

This repository contains a YouTube bot that automates various actions on the YouTube platform. The bot is designed to interact with YouTube using the provided user accounts and perform tasks such as searching for videos, liking, subscribing, and commenting.

## Features

The YouTube bot offers the following features:

1. **VPN Connection**: The bot utilizes Zen Mate VPN to establish a secure connection while interacting with YouTube.

2. **User Login**: The bot logs in to user accounts specified in the `usuarios.txt` file. Each line in the file should contain the username, followed by a space, and the corresponding password.

3. **Email Authentication**: In case of email authentication, the bot automatically clicks to request the verification code. It then opens another browser to access the verification account (provided through the `mailVerificacion` and `contraseñaVerificacion` variables in the code).

4. **YouTube Search**: The bot searches for the specified keyword stored in the `busquedaEnYoutube` variable on YouTube.

5. **Video Interaction**: After searching, the bot clicks on the video with a name matching the entries in the `videos.txt` file. Each line in the file should contain the name of a video.

6. **Actions on Video**: Once the video is accessed, the bot performs the following actions:
   - Likes the video.
   - Subscribes to the channel.
   - Posts a comment using one of the comments stored in the `comentarios.txt` file. Each line in the file should contain a comment.

## Prerequisites

Before using the YouTube bot, make sure you have the following requirements installed:

- **Google Chrome browser**: The bot relies on Chrome for browser automation. Ensure that you have Chrome installed and updated to a compatible version.
- **VPN ZEN-MATE**: The extension is loaded directly from the folder. That's why you will first have to have the downloaded Zen mate extension folder in the main folder.
- **Selenium library**: Install the Selenium library, which is a popular tool for browser automation. You can install it using the following command:

pip install selenium

- **Undetected-Chromedriver library**: Install the Undetected-Chromedriver library, which provides a wrapper around the ChromeDriver to avoid detection. You can install it using the following command:

pip install undetected-chromedriver

Please make sure to have the correct version of Chrome installed and compatible with the Selenium and Undetected-Chromedriver libraries.

If you have any questions or issues, please refer to the documentation of the respective libraries for further assistance.


## Usage

1. Clone this repository to your local machine.
2. Install the necessary dependencies and set up the required environment (e.g., VPN client, browser).
3. Create the required input files:
   - `usuarios.txt`: Provide the user accounts in the format `username password` on separate lines.
   - `comentarios.txt`: Add comments you want the bot to post, each on a new line.
   - `videos.txt`: Enter the names of videos you want the bot to interact with, each on a new line.
4. Configure the `mailVerificacion` and `contraseñaVerificacion` variables in the code to match your verification account details.
5. Run the bot script.
6. Monitor the bot's activity and check the YouTube videos to see the performed actions.

**Note:** Please use this bot responsibly and in compliance with YouTube's terms of service. Be cautious to avoid any potential violations or misuse.

That's it! You can now use the YouTube bot to automate interactions on YouTube using the provided user accounts.

## Disclaimer

This YouTube bot is for educational and personal purposes only. The developers are not responsible for any misuse or violation of YouTube's terms of service. Use this bot at your own risk.

If you have any questions or issues, please feel free to create an issue in the repository or contact us.

Happy automating on YouTube!
