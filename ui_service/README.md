# JARVIS UI APP

## Project setup

Update the tokens in the .env files with proper values.

| Tokens              | Default | Description                                                                        |
|---------------------|---|------------------------------------------------------------------------------------|
| VUE_APP_API_SERVER  |http://127.0.0.1:8000| The base URL of the API or backend server.                                                    |
| VUE_APP_API_VERSION |api/v1| API version. This will be appended to VUE_APP_API_SERVER when making an API call                                |
| VUE_APP_CLIENT_ID   |zMSG4Ieu8E0FZyctUh4uMjNrj41MpAkhzHDIheEK| OAuth client ID. The default client ID is suitable for the API server in development. |

## Run UI App

The app is containerized using Docker. To run the application, use the following command:

```
docker-compose up
```

The service will start at  http://127.0.0.1:8080 unless the port mapping in the Docker Compose configuration is
modified.

## Features

1. User Authentication
2. Add Topic/Knowledge
3. Upload Datasets for a Topic/Knowledge
4. Live status monitoring.
5. Topic based chat.
6. User and Topic based Chat History.
7. Chat UI plugging.

## Chat UI Plugin

The UI application runs in two different modes.

1. web: This is the default workflow where the application runs in standalone mode. In this mode, the application
   operates independently. It provides access to all available operations, allowing users to perform any supported task
   within the app. Additionally, it offers a detailed view of the application's contents, giving users comprehensive
   insights and control over the data and functionality.
2. plugin: When operating in plugin mode, the application's actions are constrained, limiting visibility solely to the
   chat window. Users will only have access to chat-related functionalities, excluding other features available in the
   standalone version. This mode is specifically designed to facilitate the integration of the chat feature into
   external websites or platforms, providing a seamless and focused user experience for communication purposes. It
   enables developers to easily incorporate the chat functionality into their existing web applications or websites
   without cluttering the interface with unnecessary elements.

### Integrating chat plugin.

Copy and paste the following line into the website(HTML code) where you wish to integrate the chat feature.

```html

<script src="http://127.0.0.1:8080/plugins/jarvis_ai_chatbot.js"></script>
```

After saving the changes, refresh the page to view a floating JARVIS logo at the bottom right corner of the website.
Clicking on the logo will open the chat window for interaction.

Note: The UI application must be hosted at http://127.0.0.1:8080. If the UI application is hosted on a different
machine, replace 127.0.0.1:8080 with the machine's IP address or domain. Explicitly specify this in the URL query
parameter as target. For example, if the UI application is hosted at 10.21.3.4:8080, then the source of the script
should be updated as follows:

```html

<script src="http://10.21.3.4:8080/plugins/jarvis_ai_chatbot.js?target=10.21.3.4:8080"></script>
```

Upon logging in, the default behavior is to display a list of topics/knowledge. From this list, users can select a
specific topic to engage in conversation using our user interface. Alternatively, we can navigate the user directly to a
specific chat, where the conversation is focused solely on that particular topic without the ability to view or select
other topics.To accomplish this, simply include the topic slug in the script source using the key "topic".

```html

<script src="http://127.0.0.1:8080/plugins/jarvis_ai_chatbot.js?topic=aiml-framework"></script>
```

Additionally, an obfuscated version of the file is accessible within the plugin's directory. This version mirrors the
previous file's functionality while encrypting internal details, rendering it suitable for production environments.

```html

<script src="http://127.0.0.1:8080/plugins/jarvis_ai_chatbot.obfuscate.js"></script>
```