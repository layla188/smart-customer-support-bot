# ✦ LumaAssist — Smart Customer Support Bot

An intelligent conversational customer-support assistant built for **LumaCart**, a fictional e-commerce company based in Cairo, Egypt.

LumaAssist combines **Retrieval-Augmented Generation (RAG), tool calling, live APIs, and conversation memory** to provide helpful and grounded customer-support experiences.

The assistant can answer company-related questions using a knowledge base, perform order calculations, retrieve live exchange rates, and remember information across conversation turns.

---

## 🚀 Project Overview

Traditional customer-support chatbots often provide generic responses or struggle with questions that require external information.

LumaAssist addresses this by combining:

- Knowledge-base retrieval for company-specific questions.
- Tool calling for calculations and live data.
- Short-term conversation memory.
- A multi-turn conversational interface.
- Safety rules to reduce fabricated information.
- A professional Streamlit web application.

The user can interact naturally with the assistant without needing to know which tools are being used in the background.

---

## ✨ Features

### 1. Knowledge-Base Grounded Answers

LumaAssist uses the LumaCart company knowledge base to answer questions about:

- Products
- Shipping
- Returns
- Payment methods
- Customer support
- Company policies

The retrieval pipeline uses:

1. PDF document loading.
2. Text chunking.
3. Hugging Face embeddings.
4. FAISS vector search.
5. FlashRank reranking.
6. LLM-based answer generation.

---

### 2. Tool Calling

The assistant can automatically select and execute specialized tools depending on the user's question.

Available tools include:

| Tool | Description |
|---|---|
| `search_knowledge_base` | Searches the LumaCart knowledge base using vector retrieval and reranking. |
| `calculate_order_total` | Calculates discounts, shipping fees, and final order totals. |
| `get_exchange_rate` | Retrieves the latest available exchange rate and converts currencies. |

The user does not need to manually select a tool.

The LLM determines which tool is appropriate based on the conversation context.

---

### 3. Conversation Memory

LumaAssist includes short-term conversation memory for the current session.

The assistant can remember information such as:

```text
User: My name is Layla.

Assistant: Nice to meet you, Layla!

User: What is my name?

Assistant: Your name is Layla.
```

The memory stores previous user and assistant messages and includes them in future LLM requests during the same session.

---

### 4. Multi-Turn Conversations

Users can ask follow-up questions without restarting the conversation.

Example:

```text
User: What payment methods are available?

Assistant: LumaCart supports cash on delivery where available,
cards through the approved payment gateway, and digital
payment options shown during checkout.

User: Is cash on delivery available everywhere?

Assistant: Availability may vary depending on your location
and order details.
```

---

### 5. Live Currency Conversion

The assistant uses the Frankfurter exchange-rate API to retrieve available currency rates.

Example:

```text
User: Convert 100 USD to EUR.

Assistant:
1 USD = 0.8726 EUR

100 USD = 87.26 EUR
```

Exchange rates may change over time.

---

### 6. Order Total Calculator

The calculator tool supports:

- Subtotal
- Discount percentage
- Shipping fees
- Final order total

Example:

```text
Subtotal: 800 EGP
Discount: 10%
Shipping: 50 EGP

Final total: 770 EGP
```

The tool validates values such as negative amounts and invalid discount percentages.

---

### 7. Knowledge-Base Citations

Knowledge-base search results include source information such as:

- Source number
- PDF page number
- Reranking score
- Retrieved content

Supporting information can be displayed in the application when available.

---

### 8. Professional Streamlit Interface

The application includes:

- Dark professional interface.
- LumaCart branding.
- Sidebar navigation.
- New conversation button.
- Persistent chat history.
- Suggested questions.
- Chat input.
- Loading indicators.
- Discreet tool activity information.
- Supporting information section.
- Company information and privacy guidance.

---

## 🧠 System Architecture

```text
                         User
                          |
                          v
                    Streamlit UI
                       app.py
                          |
                          v
                  LumaAssist Agent
                     agent.py
                          |
              +-----------+-----------+
              |                       |
              v                       v
        Conversation              LLM Client
          Memory                   llm.py
        memory.py                     |
                                      v
                              Tool Calling Loop
                                      |
             +------------------------+------------------------+
             |                        |                        |
             v                        v                        v
       Knowledge Base          Order Calculator        Exchange Rate
            Tool                    Tool                    Tool
             |                        |                        |
             v                        |                        v
      FAISS Retrieval                |                Frankfurter API
             |                        |
             v                        v
       FlashRank                 Calculation
       Reranking
             |
             v
       LumaCart PDF
```

---

## 📁 Project Structure

```text
smart-customer-support-bot/
│
├── data/
│   └── LumaCart_Company_Knowledge_Base.pdf
│
├── vectorstore/
│   ├── index.faiss
│   └── index.pkl
│
├── src/
│   ├── __init__.py
│   ├── config.py
│   ├── ingestion.py
│   ├── retrieval.py
│   ├── reranker.py
│   ├── tools.py
│   ├── memory.py
│   ├── llm.py
│   └── agent.py
│
├── app.py
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```

---

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| Streamlit | Web application interface |
| LangChain | LLM and retrieval integration |
| OpenRouter | LLM API access |
| Hugging Face Embeddings | Text embeddings |
| FAISS | Vector similarity search |
| FlashRank | Document reranking |
| PyPDF | PDF document loading |
| Requests | External API requests |
| Pydantic | Data validation through dependencies |

---

## ⚙️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/smart-customer-support-bot.git
```

Move into the project directory:

```bash
cd smart-customer-support-bot
```

---

### 2. Create a Virtual Environment

Windows:

```powershell
python -m venv .venv
```

Activate the environment:

```powershell
.venv\Scripts\activate
```

---

### 3. Install Dependencies

```powershell
pip install -r requirements.txt
```

---

### 4. Configure Environment Variables

Create a `.env` file in the project root:

```env
OPENROUTER_API_KEY=your_actual_openrouter_api_key
OPENROUTER_MODEL=your_supported_openrouter_model
```

The API key should never be committed to GitHub.

---

## 📚 Build the Knowledge Base

Before running the assistant, generate the FAISS vector store from the PDF.

Run:

```powershell
python -m src.ingestion
```

The ingestion pipeline:

1. Loads the LumaCart PDF.
2. Splits the document into chunks.
3. Generates embeddings.
4. Builds the FAISS vector store.
5. Saves the vector store locally.

The generated `vectorstore/` directory should be included in `.gitignore` if it is not intended to be committed.

---

## 🧪 Test Individual Components

### Test the LLM

```powershell
python -m src.llm
```

---

### Test Retrieval

```powershell
python -m src.retrieval
```

---

### Test Tools

```powershell
python -m src.tools
```

This tests:

- Knowledge-base search.
- Order total calculation.
- Live exchange-rate conversion.

---

### Test the Agent

```powershell
python -m src.agent
```

The terminal agent supports multi-turn conversations and tool calling.

Type:

```text
exit
```

to stop the application.

---

## ▶️ Run the Streamlit Application

Start the application using:

```powershell
streamlit run app.py
```

Streamlit will provide a local URL, usually:

```text
http://localhost:8501
```

---

## 💬 Demo conversation transcript

### Knowledge-Base Question

```text
User:
What payment methods are available?
```

```text
LumaAssist:
LumaCart offers cash on delivery where available,
debit and credit cards through the approved payment gateway,
and digital payment options displayed during checkout.
```

---

### Conversation Memory

```text
User:
My name is Layla.
```

```text
LumaAssist:
Hello, Layla! It's nice to meet you.
```

```text
User:
What is my name?
```

```text
LumaAssist:
Your name is Layla.
```

---

### Order Calculation Tool

```text
User:
Calculate an order with subtotal 800 EGP,
10% discount, and 50 EGP shipping.
```

```text
LumaAssist:
Subtotal: 800.00 EGP
Discount: 80.00 EGP
Shipping: 50.00 EGP
Final total: 770.00 EGP
```

---

### Live Exchange-Rate Tool

```text
User:
Convert 100 USD to EUR.
```

```text
LumaAssist:
The latest available exchange rate is retrieved
from the external exchange-rate service.

100 USD = the converted EUR amount.
```

The exact conversion depends on the current available exchange rate.

---

## 🔐 Safety and Reliability

The assistant follows several safety guidelines:

- Uses the knowledge base for company-related questions.
- Uses specialized tools for calculations and live exchange rates.
- Avoids inventing unsupported company policies.
- Does not fabricate order information.
- Asks for missing information when necessary.
- Avoids promising refunds, replacements, or delivery dates without support.
- Uses a maximum tool-calling iteration limit.
- Handles tool execution errors.
- Does not require users to know the internal tool architecture.

The system is designed to provide grounded assistance, but responses should still be reviewed for production use.

---

## 🧩 Tool Calling Workflow

The agent follows a call-execute-respond loop:

```text
1. User sends a message.
2. The message and conversation history are sent to the LLM.
3. The LLM decides whether a tool is required.
4. The agent identifies the requested tool.
5. The tool arguments are extracted.
6. The Python function is executed.
7. The tool result is returned to the LLM.
8. The LLM generates the final response.
9. The conversation is saved in memory.
```

The agent supports multiple tool calls in a single response and uses an iteration limit to reduce the risk of infinite loops.

---

## 📌 Current Limitations

- Conversation memory currently exists only during the active application session.
- Long-term vector memory across sessions is not implemented.
- Order lookup is not connected to a real order database.
- Exchange-rate availability depends on the external API.
- The knowledge base is based on a fictional LumaCart company.
- The assistant should not be used for real customer transactions without additional security and validation layers.

---

## 🔮 Future Improvements

Potential future improvements include:

- Long-term customer memory using a vector database.
- Real order tracking API integration.
- Authentication and customer identity verification.
- More advanced citation formatting.
- Conversation summarization for long chats.
- Tool execution logs and monitoring.
- Human-agent escalation workflows.
- Automated RAG evaluation.
- Improved error recovery and retry strategies.
- Deployment using Streamlit Cloud or another hosting platform.

---

## 🎯 Learning Outcomes

This project demonstrates practical implementation of:

- Function and tool calling.
- Structured tool execution.
- LLM integration with OpenRouter.
- Short-term conversation memory.
- Retrieval-Augmented Generation.
- Vector similarity search.
- Document reranking.
- External API integration.
- Multi-turn conversational systems.
- Error handling and safe execution loops.
- Streamlit application development.

---

## 👩‍💻 Author

**Layla Yasser**

AI Engineer Track Project

Built as part of a practical AI Engineering roadmap focused on LLM applications, RAG systems, tools, and conversational assistants.