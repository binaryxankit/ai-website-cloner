# Website Cloning Service

This project is a web application that can clone the visual appearance of any public website using AI. It consists of a Next.js frontend and a FastAPI backend.

## Features

- Website URL input and validation
- Website scraping with BeautifulSoup
- AI-powered website cloning using Google's Gemini Pro
- Live preview of cloned websites
- Responsive design with zoom controls
- Pixel-perfect cloning

## Prerequisites

### System Requirements

- Python 3.11 (required for Playwright compatibility)
- Node.js 18 or higher
- npm or yarn
- Google Gemini API key

### Software Installation

1. Install Python 3.11 from [python.org](https://www.python.org/downloads/)
2. Install Node.js from [nodejs.org](https://nodejs.org/)
3. Install Git from [git-scm.com](https://git-scm.com/)

## Setup

### Backend Setup

1. Navigate to the backend directory:

   ```bash
   cd backend
   ```

2. Create a Python virtual environment:

   ```bash
   # Windows
   python -m venv venv
   .\venv\Scripts\activate

   # Linux/Mac
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install Python dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the backend directory with your Google API key:

   ```
   GOOGLE_API_KEY=your_api_key_here
   ```

5. Start the backend server:
   ```bash
   uvicorn app.main:app --reload
   ```
   The backend will run on `http://localhost:8000`

### Frontend Setup

1. Navigate to the frontend directory:

   ```bash
   cd frontend
   ```

2. Install Node.js dependencies:

   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm run dev
   ```
   The frontend will run on `http://localhost:3000`

## Usage

1. Open your browser and navigate to `http://localhost:3000`
2. Enter a public website URL in the input field
3. Click "Clone Website" to start the cloning process
4. Wait for the process to complete
5. View the cloned website in the preview section
6. Use the zoom controls (50% to 150%) to adjust the view

## Project Structure

```
website-cloner/
├── frontend/                 # Next.js frontend
│   ├── src/
│   │   ├── app/             # Main application code
│   │   └── components/      # React components
│   ├── public/              # Static assets
│   └── package.json         # Frontend dependencies
│
├── backend/                  # FastAPI backend
│   ├── app/
│   │   ├── main.py         # Main API endpoints
│   │   ├── scraper.py      # Website scraping logic
│   │   └── llm_service.py  # AI integration
│   └── requirements.txt     # Backend dependencies
│
└── README.md                # Project documentation
```

## API Endpoints

### POST /clone

- **Purpose**: Clone a website using AI
- **Input**: `{ "url": "https://example.com" }`
- **Output**: `{ "html": "...", "message": "Website cloned successfully" }`

## Troubleshooting

### Common Issues

1. **Backend Connection Error**

   - Ensure the backend server is running on port 8000
   - Check if the frontend is configured to use the correct backend URL

2. **API Key Issues**

   - Verify your Google API key is correctly set in the `.env` file
   - Check if the API key has the necessary permissions

3. **Python Version Issues**

   - Ensure you're using Python 3.11
   - Verify the virtual environment is activated

4. **Node.js Issues**
   - Clear npm cache: `npm cache clean --force`
   - Delete node_modules and reinstall: `rm -rf node_modules && npm install`

## Security Considerations

- CORS is configured to only allow requests from the frontend
- Input validation for URLs
- Secure handling of API keys
- No sensitive data storage

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License.
