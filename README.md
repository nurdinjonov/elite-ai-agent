# JARVIS-X — Avtonom AI Agent

JARVIS-X — Smart Life Assistant, Multi-AI Orchestration, Memory tizimi, RAG va ko'plab vositalar bilan jihozlangan to'liq avtonom AI Agent.

## JARVIS Roli

JARVIS — professional AI life assistant sifatida ikkinchi miya, strategik fikrlash hamkori va mahsuldorlik optimizatori bo'lib xizmat qiladi. U foydalanuvchiga samaraliroq fikrlash, o'rganish, rejalashtirish va harakat qilishda yordam beradi.

**Asosiy tamoyillar:**
- Aqliy harakatni doimo kamaytirish
- Tuzilgan chiqishlarni taqdim etish
- Amaliy qadamlarni taklif qilish
- Foydalanuvchi xatti-harakatlariga moslashish
- Hech qachon murakkablashtirmaslik
- Hech qachon bildirishnomalar bilan haddan tashqari ko'p bezovta qilmaslik
- Hech qachon umumiy maslahat bermaslik

## Xususiyatlar

- 🤖 **Multi-AI Orchestration** — OpenRouter, Groq provayderlarini qo'llab-quvvatlaydi
- 🧠 **Memory System** — Qisqa va uzoq muddatli xotira (ChromaDB)
- 📚 **RAG** — Lokal hujjatlardan bilim olish
- 🔧 **Tools** — Web qidiruv, fayl boshqaruvi, kod bajarish, terminal
- 🎓 **Life Assistant** — Dars jadvali, uy vazifalari, kundalik reja
- 🌐 **Ko'p tilli** — O'zbek, Ingliz, Rus tillarini avtomatik aniqlaydi
- 🎙 **Voice** (ixtiyoriy) — Whisper STT + piper TTS
- 🧬 **Intelligence Modules** — Kognitiv yuk, fokus, prokrastinatsiya, o'qitish

## Tezkor ishga tushirish

```bash
# 1. Reponi klonlash
git clone https://github.com/AzimjonKamiljanov/elite-ai-agent.git
cd elite-ai-agent

# 2. Avtomatik setup (barcha OS uchun)
python setup.py
# yoki
python3 setup.py

# 3. API kalitlarini sozlash
# .env faylini tahrirlang va API kalitlarini kiriting

# 4. JARVIS-X ni ishga tushirish

# Windows:
jarvis.bat

# Linux/macOS:
./jarvis

# Yoki to'g'ridan-to'g'ri:
python start.py

# Faqat Life Assistant rejimida:
python start.py --life-only

# 5. Diagnostika
python health_check.py
```

## Rejimlar

| Rejim | Buyruq | Tavsif |
|-------|--------|--------|
| PRO | `/pro` | Batafsil, tadqiqot darajasidagi javoblar |
| CODE | `/code` | Kod yozishga ixtisoslashgan |
| FAST | `/fast` | Tez, qisqa javoblar |
| STUDY | `/study` | O'qitish yordamchisi — Feynman texnikasi |
| FOCUS | `/focus` | Ultra-qisqa javoblar, faqat joriy vazifa |
| PLANNER | `/planner` | Kundalik reja va vaqtni boshqarish |

## Intelligence Modullari

### CognitiveLoadBalancer
Aqliy ish yukini kuzatadi: vazifalar soni, muddat bosimi va dam olish naqshlari asosida yuk darajasini hisoblaydi: `low`, `moderate`, `high`, `critical`.

### TimePerceptionEngine
Pomodoro tsikllari (25 daq ish / 5 daq tanaffus) va chuqur ish bloklari yordamida vaqtni tuziladi. Joriy fokus sessiyasini kuzatadi.

### AntiProcrastinationEngine
Takroriy kechiktirishlarni aniqlaydi. 5 daqiqalik boshlash texnikasini va micro-qadam strategiyasini taklif qiladi.

### LifeNarrativeEngine
Haftalik aks ettirish: yutuqlar, qiyinchiliklar, o'sish ko'rsatkichlari va maslahatlar.

### AITutorMode
Mavzularni tushuntirish, xulosa yaratish, viktorina generatsiyasi, uy vazifasiga yordam va o'qish rejasi.

### PersonalityAdapter
Foydalanuvchi afzalliklariga moslashadi: `concise`/`detailed`, `motivational`/`neutral`, `technical`/`simple`.

## Arxitektura

```
elite-ai-agent/
├── jarvis_life.py         # Life Assistant CLI
├── start.py               # Asosiy ishga tushirish nuqtasi
├── jarvis                 # Linux/macOS launcher
├── jarvis.bat             # Windows launcher
│
├── core/                  # AI Agent modullari
│   ├── jarvis.py          # Asosiy Orchestrator
│   ├── ai_router.py       # Multi-AI yo'naltiruvchi
│   ├── modes.py           # Rejim tizimi (FAST/CODE/PRO/STUDY/FOCUS/PLANNER)
│   ├── intelligence.py    # Intelligence modullari (yangi)
│   ├── education.py       # O'qish va focus tracking
│   ├── language.py        # Til aniqlovchi
│   ├── memory.py          # Xotira tizimi
│   ├── tools.py           # Vositalar reestri
│   ├── rag.py             # RAG tizimi
│   └── voice.py           # Ovoz tizimi
│
├── life/                  # Life Assistant modullari
│   ├── models.py          # Pydantic data modellari
│   ├── storage.py         # JSON saqlash
│   ├── scheduler.py       # Dars jadvali
│   ├── homework.py        # Uy vazifalari
│   ├── daily_planner.py   # Kundalik reja
│   └── reminders.py       # Eslatmalar
│
├── tools/                 # Tashqi vositalar
│   ├── web_search.py      # DuckDuckGo qidiruv
│   ├── file_manager.py    # Fayl operatsiyalari
│   ├── code_executor.py   # Kod bajarish
│   └── terminal.py        # Terminal buyruqlari
│
├── config/                # Sozlamalar
│   ├── models.json        # AI model konfiguratsiyasi
│   ├── settings.json      # Umumiy sozlamalar
│   └── schedule_config.json  # Jadval sozlamalari
│
└── data/                  # Ma'lumotlar
    ├── memory/            # ChromaDB saqlash
    ├── documents/         # RAG hujjatlar
    └── schedule/          # Jadval JSON fayllari
```

## Buyruqlar

### AI Agent (start.py)
| Buyruq | Tavsif |
|--------|--------|
| `/fast` | FAST rejimiga o'tish |
| `/code` | CODE rejimiga o'tish |
| `/pro` | PRO rejimiga o'tish |
| `/study <mavzu>` | STUDY rejimiga o'tish va mavzu haqida so'rash |
| `/focus [daqiqa]` | Focus/Pomodoro sessiyasini boshlash (default: 25 min) |
| `/focus stop` | Focus sessiyasini to'xtatish |
| `/planner` | PLANNER rejimiga o'tish |
| `/modes` | Barcha mavjud rejimlar ro'yxati |
| `/providers` | AI provayderlar holati |
| `/models` | Konfiguratsiya qilingan AI modellari |
| `/today` | Bugungi to'liq sharh |
| `/status` | To'liq tizim holati |
| `/cognitive` | Kognitiv yuk tahlili |
| `/reflect` | Haftalik aks ettirish |
| `/help` | Yordam matnini ko'rsatish |
| `/exit` | Chiqish |

### Life Assistant (jarvis_life.py)
#### Jadval
| Buyruq | Tavsif |
|--------|--------|
| `/schedule` | Bugungi dars jadvali |
| `/week` | Haftalik dars jadvali |
| `/add_class <fan> <kun> <boshlanish> <tugash> [xona]` | Yangi dars qo'shish |
| `/remove_class <id>` | Darsni o'chirish |
| `/load_sample` | Namuna jadval yuklash |

#### Uy Vazifalari
| Buyruq | Tavsif |
|--------|--------|
| `/homework` | Bajarilmagan uy vazifalari |
| `/add_hw <fan> <tavsif> [muddat] [ustuvorlik]` | Yangi uy vazifasi qo'shish |
| `/done_hw <id>` | Uy vazifasini bajarilgan deb belgilash |

#### Vazifalar
| Buyruq | Tavsif |
|--------|--------|
| `/tasks` | Barcha bajarilmagan vazifalar |
| `/add_task <sarlavha> [tavsif] [muddat]` | Yangi vazifa qo'shish |
| `/done_task <id>` | Vazifani bajarilgan deb belgilash |

#### Reja va Eslatmalar
| Buyruq | Tavsif |
|--------|--------|
| `/plan` | Bugungi optimal reja |
| `/reminders` | Barcha eslatmalar |
| `/stats` | Statistika |
| `/summary` | Kun oxiri xulosasi |

#### Intelligence
| Buyruq | Tavsif |
|--------|--------|
| `/today` | Bugungi to'liq sharh (dars, vazifalar, kognitiv yuk) |
| `/focus [daqiqa]` | Focus/Pomodoro sessiyasini boshlash |
| `/focus stop` | Focus sessiyasini to'xtatish |
| `/cognitive` | Kognitiv yuk tahlili |
| `/reflect` | Haftalik aks ettirish |

## Sozlash

### .env fayli
```env
# AI Providers
OPENROUTER_API_KEY=your_key_here
GROQ_API_KEY=your_key_here

# Life Assistant
JARVIS_WAKE_UP_TIME=07:00
JARVIS_CLASS_ALERT_MINUTES=15

# Memory
CHROMA_PERSIST_DIR=./data/memory
```

## Ma'lumotlar Modellari

- **ClassSchedule** — Dars jadvali (fan, kun, vaqt, xona, o'qituvchi)
- **Homework** — Uy vazifasi (fan, tavsif, muddat, ustuvorlik)
- **Task** — Umumiy vazifa (sarlavha, kategoriya, muddat)
- **DailyPlan** — Kundalik reja (darslar, o'qish bloklari, dam olish)
