# 🤖 EliteAgent — Ilg'or Avtonom AI Agent

[![Python](https://img.shields.io/badge/Python-3.11%2B-blue)](https://www.python.org/)
[![LangGraph](https://img.shields.io/badge/LangGraph-0.2%2B-orange)](https://github.com/langchain-ai/langgraph)
[![LangChain](https://img.shields.io/badge/LangChain-0.3%2B-green)](https://github.com/langchain-ai/langchain)
[![ChromaDB](https://img.shields.io/badge/ChromaDB-0.5%2B-purple)](https://www.trychroma.com/)

EliteAgent — **ReAct (Reason + Act)** paradigmasiga asoslangan, **LangGraph** orkestratorida ishlaydigan to'liq avtonom AI agent. U web qidiruv, kod bajarish, fayl boshqaruv, terminal buyruqlar, uzoq muddatli xotira va RAG bilim bazasi kabi ilg'or imkoniyatlarni birlashtiradi.

---

## Arxitektura

```
FOYDALANUVCHI → ORCHESTRATOR (LangGraph) → [Fikrlash → Rejalashtirish → Bajarish] → JAVOB
                     ↕                              ↕                    ↕
              XOTIRA TIZIMI                   BILIM BAZASI          ASBOBLAR
           (Qisqa + Uzoq muddatli)          (ChromaDB + RAG)    (Web, Kod, Fayl, Terminal)
```

### Graf oqimi

```
START → enrich_context → reasoning → [tools → reasoning]* → END
```

---

## Texnologiyalar steki

| Komponent         | Texnologiya                        |
|-------------------|------------------------------------|
| Orchestrator      | LangGraph                          |
| LLM               | OpenAI GPT-4o                      |
| Vektorlash        | OpenAI text-embedding-3-small      |
| Vektor bazasi     | ChromaDB                           |
| Web qidiruv       | Tavily API                         |
| Ramka             | LangChain                          |
| Sozlamalar        | Pydantic-Settings                  |
| Terminal UI       | Rich                               |

---

## Loyiha tuzilmasi

```
elite_agent/
├── agent/
│   ├── __init__.py
│   ├── graph.py            # LangGraph orchestrator — asosiy agent oqimi
│   ├── state.py            # Agent holati (state) ta'rifi
│   ├── nodes.py            # Graf tugunlari (fikrlash, bajarish, kuzatish)
│   └── prompts.py          # Tizim promptlari
├── memory/
│   ├── __init__.py
│   ├── short_term.py       # Qisqa muddatli suhbat xotirasi
│   └── long_term.py        # Uzoq muddatli vektor xotira (ChromaDB)
├── tools/
│   ├── __init__.py
│   ├── web_search.py       # Internet qidiruv asbob (Tavily API)
│   ├── code_executor.py    # Python kod bajarish asbob
│   ├── file_manager.py     # Fayl o'qish/yozish asbob
│   └── terminal.py         # Terminal buyruqlarni bajarish asbob
├── knowledge/
│   ├── __init__.py
│   └── ingest.py           # Hujjatlarni indekslash va RAG tizimi
├── config/
│   ├── __init__.py
│   └── settings.py         # Barcha sozlamalar (pydantic-settings)
├── data/
│   ├── chroma_db/.gitkeep
│   ├── documents/.gitkeep
│   └── agent_memory/.gitkeep
├── main.py                 # Asosiy ishga tushirish fayli (interactive terminal UI)
├── requirements.txt        # Kutubxonalar ro'yxati
├── .env.example            # Namuna muhit o'zgaruvchilari
├── .gitignore
└── README.md
```

---

## O'rnatish va ishga tushirish

### 1. Repozitoriyni klonlash

```bash
git clone https://github.com/abbosbek112/elite-ai-agent.git
cd elite-ai-agent
```

### 2. Virtual muhit yaratish

```bash
python -m venv venv
source venv/bin/activate      # Linux/macOS
# venv\Scripts\activate       # Windows
```

### 3. Kutubxonalarni o'rnatish

```bash
pip install -r requirements.txt
```

### 4. Muhit o'zgaruvchilarini sozlash

```bash
cp .env.example .env
# .env faylini tahrirlang va API kalitlarini kiriting
```

`.env` fayli namunasi:

```env
OPENAI_API_KEY=sk-your-openai-api-key-here
OPENAI_MODEL=gpt-4o
TAVILY_API_KEY=tvly-your-tavily-api-key-here
CHROMA_PERSIST_DIR=./data/chroma_db
AGENT_NAME=EliteAgent
AGENT_MAX_ITERATIONS=15
```

### 5. Agentni ishga tushirish

```bash
python main.py
```

---

## Foydalanish misollari

| Buyruq / So'rov                          | Tavsif                                    |
|------------------------------------------|-------------------------------------------|
| `Bugungi ob-havo qanday?`               | Tavily orqali real vaqtda qidiradi        |
| `Python da Fibonacci yoz`               | Kodni bajarib natija ko'rsatadi           |
| `/ingest ./data/documents`              | Katalogdagi hujjatlarni indekslaydi       |
| `/remember Men Python dasturchiман`     | Faktni uzoq muddatli xotiraga saqlaydi   |
| `/recall Python`                        | Xotiradan semantik qidiradi               |
| `requirements.txt faylini o'qi`         | Fayl tarkibini ko'rsatadi                 |
| `ls -la buyrug'ini bajari`              | Terminal buyruqni ishga tushiradi         |
| `/clear`                                | Suhbat tarixini tozalaydi                 |
| `/exit`                                 | Dasturdan chiqadi                         |

---

## Kengaytirish tavsiyalari

- **Yangi asbob qo'shish**: `tools/` katalogiga yangi fayl yarating, `@tool` dekoratorini ishlating va `tools/__init__.py` dagi `ALL_TOOLS` ro'yxatiga qo'shing.
- **Yangi xotira turi**: `memory/` katalogiga qo'shing va `nodes.py` dagi `enrich_context_node` funksiyasini yangilang.
- **LLM almashtirish**: `agent/nodes.py` dagi `llm` o'zgaruvchini boshqa `ChatModel` bilan almashtiring.
- **Yangi hujjat formati**: `knowledge/ingest.py` dagi `_load_file` metodiga yangi `elif` blok qo'shing.

---

## Litsenziya

MIT License — erkin foydalanishingiz mumkin.
