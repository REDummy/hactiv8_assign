
# SMART BREW CALCULATOR — ASSIGNMENT 23 & 24 
---

# STEP 01: Define Your Project Scope & Goals

## 1. What does your AI system do?
An AI-powered specialty coffee assistant that generates personalized brewing recipes, provides step-by-step guidance, and adapts recommendations based on user taste preferences and coffee bean characteristics.

---

## 2. Who are the users?
- Beginner to intermediate coffee brewers  
- Specialty coffee enthusiasts  
- Café customers  

Technical level: Non-technical  
Expected usage: approximately 1,000 users per day (around 30,000 requests per month)

---

## 3. What does “success” look like?
- Brewing recommendation satisfaction ≥ 90 percent (based on user ratings or repeat usage)  
- Users are able to brew coffee without professional assistance  
- Increased repeat usage of personalized recipes  

---

## 4. What are your hard constraints?
- Output must be in Bahasa Indonesia  
- Monthly budget should remain below 15 USD  
- Target response latency under 3 seconds  
- System must only handle coffee-related queries and avoid medical or health advice  

---

## 5. What data will you feed the model?

Data sources:
- Coffee beans database (100–500 entries)  
- Brewing recipes (50–100 structured recipes)  
- Brewing theory summaries  
- Professional brewing techniques  

Typical context per request:
- 2–3 retrieved chunks  
- Approximately 200–300 tokens per chunk  
- Total context size: approximately 600–650 tokens  

---

# STEP 02: Choose the Right Model

| Dimension   | Requirement                     | Score | Drives Toward     |
|-------------|---------------------------------|------|-------------------|
| Quality     | Moderate to high accuracy       | 2    | Balanced models   |
| Speed       | Real-time (< 3 seconds)         | 3    | Fast models       |
| Cost        | Very tight budget               | 3    | Low-cost models   |
| Constraints | Bahasa Indonesia support        | 2    | Flexible support  |

---

## Model Choice
Gemini 3.1 Flash  

Reason:  
Provides a strong balance of speed, low operational cost, and multilingual capability suitable for high-frequency interactive usage.

---

# STEP 03: Design Your Prompt

---

## A — System Prompt

```text
You are a specialty coffee barista assistant for a smart brew calculator.

Help users brew coffee using methods such as V60, Origami, Kalita, AeroPress, French Press, Hario Switch, Tricolate, and Pulsar.

Only answer questions related to coffee, brewing methods, recipes, and taste recommendations.

Respond in Bahasa Indonesia in a friendly and helpful tone.

Structure responses as follows:
- Short introduction
- Bullet points or step-by-step instructions
- Include measurements (grams, ml, time, temperature)
- Include grind size and brew ratio
- Include expected flavor profile

If a question is outside scope, politely refuse.

Do not provide medical or health advice.
````

***

## B — Context / RAG Injection

Example structure:


Bean: Ethiopia Yirgacheffe
Process: Washed
Notes: floral, citrus
Roast: light

Recipe:
Brewer: Origami
Ratio: 1:16
Temperature: 92°C
Grind: medium-fine

Typical size:

*   2–3 chunks
*   Approximately 600–650 tokens total

***

## C — Sample User Messages

Message 1:  
Aku punya beans Ethiopia, enaknya brew pakai Origami gimana?

Message 2:  
Aku suka kopi yang strong dan pahit, brewer apa yang cocok?

Message 3:  
Kalau pakai Pulsar buat natural coffee enaknya ratio berapa?

***

## D — Expected Output Definition

Format: Bullet list and step-by-step instructions  
Length: Medium (\~150–200 tokens)  
Tone: Friendly and educational  
Language: Bahasa Indonesia

***

### Example Response


Ethiopia cocok untuk Origami karena karakter floral dan citrus.

Resep:
- Kopi: 15g
- Air: 240ml (rasio 1:16)
- Grind size: medium-fine
- Suhu air: 92°C

Langkah:
1. Bloom 30 detik dengan 50ml air
2. Lanjutkan tuang dalam 3 tahap
3. Total waktu seduh 2:30–3:00

Hasil:
- Rasa floral dan citrus
- Acidity bright
- Aftertaste clean

***

# STEP 04: Token Estimation

| Component       | Tokens |
| --------------- | ------ |
| System Prompt   | 150    |
| User Message    | 30     |
| Context (RAG)   | 650    |
| Expected Output | 180    |

***

Total per request:

*   Input tokens: 150 + 30 + 650 = 830
*   Output tokens: 180

Total tokens per call: approximately 1,010

Key consideration: Bahasa Indonesia typically uses 1.5 to 2 times more tokens than English.

***

# STEP 05: Monthly API Cost Estimation

## Baseline Calculation

Inputs:

*   Input tokens per call: 830
*   Output tokens per call: 180
*   Requests per month: 30,000
*   Input price: 0.25 USD per 1M tokens
*   Output price: 1.50 USD per 1M tokens

***

Input cost:
(830 × 30,000 ÷ 1,000,000 × 0.25) ≈ 6.23 USD

Output cost:
(180 × 30,000 ÷ 1,000,000 × 1.50) ≈ 8.10 USD

***

Total monthly cost:
≈ 14.33 USD

***

