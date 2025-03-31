# Amazon Sales Chat Bot

<div align="center">
  <!-- Backend -->
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white" />
  <img src="https://img.shields.io/badge/Google-4285F4?style=for-the-badge&logo=google&logoColor=white" />
  <img src="https://img.shields.io/badge/LlamaIndex-4F5B93?style=for-the-badge&logo=llamaindex&logoColor=white" />
  <img src="https://img.shields.io/badge/LangChain-121212?style=for-the-badge&logo=chainlink&logoColor=white" />
  <img src="https://img.shields.io/badge/LangGraph-FF6B6B?style=for-the-badge&logo=graph&logoColor=white" />
  <img src="https://img.shields.io/badge/Qdrant-4F5B93?style=for-the-badge&logo=qdrant&logoColor=white" />
  <img src="https://img.shields.io/badge/TavilySearch-4F5B93?style=for-the-badge&logo=tavilysearch&logoColor=white" />

  
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

<img src="https://github.com/naveenkrishnan840/amazon-sales-chat-bot/blob/main/backend/graph.png"/>

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
   - Web Search for external doucment generation

3. **AI Decision Making**
   - Multiple LLM integration (Gemini, deepseek)
   - Grade document
   - Hallucination Grader
   - Answer Grader
   - Transform query mechanisms
   - Structured output generation

## List of question ask to chat bot
1. What are the amazon orders is shipped status with SKU, can you mention order id, when its shipped?
2. Can you tell us date is 29-04-2022, what orders happened and status?
3. What trends can I identify from the "Status" of the orders (e.g., Cancelled, Shipped)?
4. What factors contributed to the cancellation of certain orders, and how can I reduce cancellations in the future? 
Sales Channel Insights
5. How has the sales channel (e.g., Amazon, Merchant) impacted the order status and fulfilment?
6. What patterns do I notice in terms of orders being shipped through Amazon vs Merchant?
Fulfilment Process: 
7. How can I streamline the fulfilment process to avoid delays in shipping or cancellations?
8. Do the fulfilment methods (Merchant vs Amazon) affect the delivery times or customer satisfaction?
Courier and Shipping Levels:
9. Are there any trends in the shipping service levels that contribute to faster or slower deliveries?
10. How does the choice of courier impact the delivery success rate, especially with different shipping methods like Easy Ship or Expedited?
## Project Structure 
```
amazone-sales-chat-bot/
├── backend/
|  ├── src/
|  |   ├── __init__.py
|  │   ├── generate/                           
|  │   │   ├── __init__.py                     
|  │   │   ├── generate.py             
|  |   |── grade_documents
|  │   │   ├── __init__.py             
|  │   │   ├── grade_documents.py  
|  |   |── retrieve   
|  │   │   ├── __init__.py         
|  │   │   ├── retrieve.py         
|  |   ├── search_tool             
|  │   │   ├── __init__.py         
|  |   |   ├── web_search_tool.py  
|  |   |── transform_query
|  |   |   |── __init__.py
|  |   |   |── transform_query.py
|  │   ├── build_graph.py          
|  |   ├── esges.py
|  |   ├── state_template.py       
|  |   ├── structured_output.py 
|  │────── .env # If you want
|  │────── pyproject.toml # create virtual env using poetry
|  │────── main.py # Main entry point
|  ├── pyproject.toml
|  ├── ...
```

## Setup Instructions

### Backend Setup

1. Clone the repository
   ```bash
   git clone https://github.com/naveenkrishnan840/amazon-sales-chat-bot.git
   cd amazon-sales-chat-bot
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
    OPEN_API_KEY= "Your api key"
    OPENROUTER_BASE_URL="your url"
    QDRANT_API_KEY="Your api key"
    QDRANT_URL="your url"
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
