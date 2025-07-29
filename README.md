# voice-booker

> A voice-driven appointment booking agent powered by LiveKit, Groq, Deepgram, and Cartesia, integrating with Google Calendar.

## Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)

## Features

- Real-time voice communication using LiveKit.
- Low-latency audio transcription with Deepgram.
- Intelligent scheduling logic powered by Cartesia and Groq.
- Seamless Google Calendar integration for creating, listing, and managing events.
- Error handling and user feedback for smooth interactions.

## Tech Stack

- **LiveKit** for audio/video streaming.
- **Deepgram** API for speech-to-text transcription.
- **Groq** chip for acceleration of AI inference.
- **Cartesia** for decision-making and NLP orchestration.
- **Google Calendar API** for event management.

## Prerequisites

- Node.js v14+ (or Python 3.8+)
- Conda (optional, for environment management)
- Google Cloud project with Calendar API enabled
- LiveKit server URL and API key/secret
- Deepgram API key
- Groq environment setup
- Cartesia API credentials

## Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/<your-username>/ai-voice-schedular-agent.git
   cd ai-voice-schedular-agent
   ```

2. **Create a Conda environment** (optional but recommended)

   ```bash
   conda create -n voice-booker python=3.10
   conda activate voice-booker
   ```

3. **Install dependencies**

   For Python:

   ```bash
   pip install -r requirements.txt
   ```

## Configuration

Create a `.env` file in the project root with the following variables:

```dotenv
# LiveKit
LIVEKIT_URL=<your_livekit_server_url>
LIVEKIT_API_KEY=<your_livekit_api_key>
LIVEKIT_API_SECRET=<your_livekit_api_secret>

# Deepgram
DEEPGRAM_API_KEY=<your_deepgram_api_key>

# Google Calendar
GOOGLE_CLIENT_ID=<your_google_client_id>
GOOGLE_CLIENT_SECRET=<your_google_client_secret>
GOOGLE_REDIRECT_URI=http://localhost:3000/auth/callback

# Groq
GROQ_API_KEY=<your_groq_api_key>

# Cartesia
CARTESIA_ENDPOINT=<your_cartesia_endpoint>
CARTESIA_API_KEY=<your_cartesia_api_key>
```

## Usage

1. **Download the files**

   ```bash
   python agent.py download-files   # or python app.py
   ```

2. **Run the code**

   ```bash
   python agent.py console   # or python app.py
   ```

3. **Interact via voice**

   - The agent will confirm details and create an event on your Google Calendar.

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new branch: `git checkout -b feature/my-feature`.
3. Commit your changes: `git commit -m 'Add some feature'`.
4. Push to the branch: `git push origin feature/my-feature`.
5. Open a Pull Request.

Please ensure your code follows the existing style and passes any tests.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
