# Amazon Sales Chat Bot

<div align="center">
  <!-- Backend -->
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white" />
  <img src="https://img.shields.io/badge/MySQL-4479A1?style=for-the-badge&logo=mysql&logoColor=white" />
  <img src="https://img.shields.io/badge/Faiss-4F5B93?style=for-the-badge&logo=faiss&logoColor=white" />
  <img src="https://img.shields.io/badge/Google-4285F4?style=for-the-badge&logo=google&logoColor=white" />
  <img src="https://img.shields.io/badge/LangChain-121212?style=for-the-badge&logo=chainlink&logoColor=white" />
  <img src="https://img.shields.io/badge/FlashrankRerank-4B9CD3?style=for-the-badge&logo=flash&logoColor=white" />
  <img src="https://img.shields.io/badge/LangGraph-FF6B6B?style=for-the-badge&logo=graph&logoColor=white" />
  
  <!-- Frontend -->
  <img src="https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black" />
  <img src="https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white" />
  <img src="https://img.shields.io/badge/React-61DAFB?style=for-the-badge&logo=react&logoColor=black" />

  <h3>Your AI Co-pilot for Amazon Sales Chat Bot 🚀</h3>

  <p align="center">
    <b>Vector DB Retriever | Grade Document | Hallucination Grader | Answer Grader | Transaform Query | Generate Content </b>
  </p>
</div>

# Overview
The <b>Amazon Sales Chat Bot </b> is an Self Reflective Rag, this rag system that provides a seamless, efficient, and personalized experience.
This rag reveals a combination of successful transactions and cancellations, offering insight into customer preferences, logistical efficiency, and promotional effectiveness. By analyzing these patterns, the business can take steps to optimize fulfillment, reduce cancellations, and tailor marketing efforts to better meet customer needs. Exploring the root causes of issues like cancellations and delays could lead to valuable improvements in both customer service and overall sales strategies.

# Motivation
In every business or project, whether it’s sales, fulfillment, or customer service, there will be challenges and successes. Canceled orders? They’re not failures. They’re opportunities to learn, adapt, and refine your processes. Maybe it's about understanding customer needs better, optimizing the product offering, or adjusting shipping times. Each cancellation is simply a moment for growth.

## key Features
     
### Self Reflective RAG Diagrams

<img src="https://github.com/naveenkrishnan840/amazon-sales-chat-bot/blob/main/graph.png"/>

## Architecture

The system is built on a modern tech stack with three distinct agent types, each powered by:

1. **State Management**
   - LangGraph for maintaining agent message state
   - Handles complex navigation flows and decision making
   - Structured workflow management
    
2. **Content Processing**
   - RAG (Retrieval Augmented Generation) pipeline
   - Vector store integration for efficient information storage
   - Automatic content structuring and organization

3. **AI Decision Making**
   - Multiple LLM integration (Gemnin, deepseek)
   - Context-aware navigation
   - Self-review mechanisms
   - Structured output generation


## Project Structure 
```
ai-hedge-fund/
├── src/
│   ├── assistant/                           # Agent definitions and workflow
│   │   ├── __init__.py                      # init file
│   │   ├── primary_assistant.py             # primary assistant agent
│   │   ├── hotel_assistant.py               # hotel_assistant agent
│   │   ├── flight_assistant.py              # flight assistant agent
│   │   ├── car_rental_assistant.py          # Car rental agent
│   │   ├── excursion_assistant.py           # Car rental agent
|   ├── database                             # To store the vector files
│   ├── tools/                               # Agent tools
│   │   ├── __init__.py                      # init file
|   |   ├── car_rental.py                    # To handle the search, update, cancel things
|   |   ├── flights.py                       # To handle the search, update, cancel things
|   |   ├── hotels.py                        # To handle the search, update, cancel things
|   |   ├── excursions.py                    # To handle the search, update, cancel things
|   |   ├── lookup_policies_search_tool.py   # To retrieve the policy content
│   ├── build_graph.py                       # building the graph
|   ├── question.py
|   ├── request_validate.py                  # request validation
|   ├── utilities.py 
│────── .env # If you want
│────── data_insertion.py # customer related records insert to mysql db
│────── pyproject.toml # create virtual env using poetry
│────── main.py # Main entry point
├── pyproject.toml
├── ...
```

## Setup Instructions

### Backend Setup

1. Clone the repository
   ```bash
   git clone https://github.com/naveenkrishnan840/customer-support-bot.git
   cd customer-support-bot
   cd backend
   ```

2. Install Poetry (if not already installed)

   Mac/Linux:
   ```bash
   curl -sSL https://install.python-poetry.org | python3 -
   ```
   Windows:
   ```bash
   (Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -
   ```

3. Set Python version for Poetry
   ```bash
   poetry env use python3.12
   ```

4. Activate the Poetry shell:
   For Unix/Linux/MacOS:
   ```bash
   poetry shell
   # or manually
   source $(poetry env info --path)/bin/activate
   ```
   For Windows:
   ```bash
   poetry shell
   # or manually
   & (poetry env info --path)\Scripts\activate
   ```

5. Install dependencies using Poetry:
   ```bash
   poetry install
   ```

6. Set up environment variables in `.env`:
   ```bash
    GOOGLE_API_KEY="Your api key"
    TAVILY_API_KEY="Your api key"
    COHERE_API_KEY="Your api key"
    MYSQL_HOST="Your host url"
    MYSQL_USER="Your user"
    MYSQL_PASSWORD="your password"
    MYSQL_DB="your database name"
    LANGCHAIN_TRACING_V2=true
    LANGCHAIN_ENDPOINT="https://api.smith.langchain.com"
    LANGCHAIN_API_KEY="your api key"
    LANGCHAIN_PROJECT="your project name"
   ```

7. Run the backend:

   Make sure you are in the backend folder

    ```bash
    uvicorn app.main:app --reload --port 8000 
    ```

   For Windows User:

    ```bash
    uvicorn app.main:app --port 8000
    ```

8. Access the API at `http://localhost:8000`

### Frontend Setup

1. Open a new terminal and make sure you are in the WebRover folder:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Run the frontend:
   ```bash
   npm run dev
   ```

4. Access the frontend at `http://localhost:3000`

For mac users: 

Try running http://localhost:3000 on Safari browser. 

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

Made with ❤️ by [@naveenkrishnan840](https://github.com/naveenkrishnan840)
