# 🤖 Фунт 2.0 - Bot Behavior & Activity Patterns

Complete guide to how the bot acts, when it responds, and all its activities.

---

## 📅 Scheduled Activities (Automatic)

### 1. **News Posts** - 4 times per day

**Schedule:**
- 4 random times between 9:00 AM and 9:00 PM (9-21 hours)
- Each day at midnight (00:00), new random times are generated for the next day
- Minutes are randomized (0-59)

**Example daily schedule:**
```
11:27 - News post 1
14:53 - News post 2
17:14 - News post 3
20:41 - News post 4
```

**What happens:**
1. Bot fetches latest news from UNIAN.net
2. If news available: sends news headline + bot's sarcastic comment
3. If no news available: creates fake news with sarcastic comment

**Style:** Cynical, short, language-specific (Russian)

---

### 2. **Conversation Initiation** - Every 2 hours

**Schedule:**
- Runs every 2 hours continuously throughout the day
- Can happen: 00:00, 02:00, 04:00, 06:00, 08:00, 10:00, 12:00, 14:00, 16:00, 18:00, 20:00, 22:00

**How it works:**
1. Randomly picks one of 3 people:
   - Дmitry Sadovoi (@doom4a) - Russian, Putin supporter
   - Vladimir Kravchenko (@Vladimir_vkr) - Moscow resident, blandness
   - Alexey Bekish (@avbekish) - Belarusian, fishing obsession

2. Picks random trigger topic from their profile:
   - For Doom: Putin, Europe, Russia, sanctions, Kaliningrad
   - For Vavan: Moscow, Russia, sanctions, war
   - For Scot: fishing, sudaks, Belarus, Putin

3. Generates provocative question via DeepSeek AI
4. Sends to chat mentioning the person by name

**Example messages:**
```
Дум, а не пизда ли тебе, что вокруг одни европейцы?
Ваван, ты в Домодедово сидишь и правда веришь в Путина?
Скот, рыбалка клевала или только членом промахнулся?
```

---

## 💬 Reactive Activities (When You Send Messages)

### **ALWAYS Active** - Message Recognition

The bot **continuously listens** for these triggers and responds:

#### **Type 1: Keyword Triggers** ✅ Auto-respond

Bot checks **4 categories of keywords**:

**Political Keywords** (52 words):
- путин, кремль, европа, украина, россия, война, санкции, доллар, биткоин, зеленский, лукашенко, трамп, и др.

**News Keywords** (64 words):
- новость, вброс, слухи, унян, дроны, взрыв, наступление, водка, алкаш, дейнга, и др.

**Women Keywords** (5 words):
- любовница, жена, измена, секс, девушка

**Gossip Keywords** (4 words):
- говорят, слышал, история, по слухам

**Action:** Responds with sarcastic comment on the topic

---

#### **Type 2: Bot Mention** ✅ Direct reply

When someone writes **"фунт"** anywhere in message:
- Bot responds directly to that person
- Doesn't mention others
- Uses their name context if available

---

#### **Type 3: Reply to Bot Message** ✅ Conversation

When someone replies to bot's message:
- Bot continues the conversation
- Remembers the context of previous exchange
- Can use bot's own message as context for response

---

#### **Type 4: URL/Link in Message** ✅ Content analysis

When someone pastes a link:
- Bot tries to parse the webpage
- Extracts text content
- Checks if content matches keywords
- Responds based on content of the article/page

---

### **Probability-Based Reactions**

#### **Opportunistic Attack** - 15-20% random chance

When someone from ACQUAINTANCES (Doom, Vavan, Scot) writes **ANY** message:
- 15-20% chance: Bot ignores the topic completely
- Sends a provocative personal attack instead
- Uses their known weaknesses/taunt vectors

**Example:**
```
User writes: "Hey, anyone know good coffee place?"
Bot (if 15-20% chance triggers): "Ваван, опять в Москве сидишь? Жопе холодно?"
```

---

## 🕐 Complete Daily Timeline Example

```
06:00 - Nothing (outside active hours)
08:00 - Proactive conversation init #1
09:00 - Nothing (too early)
10:00 - Proactive conversation init #2
11:27 - NEWS POST #1 ⭐
12:00 - Proactive conversation init #3
14:00 - Proactive conversation init #4
14:53 - NEWS POST #2 ⭐
16:00 - Proactive conversation init #5
17:14 - NEWS POST #3 ⭐
18:00 - Proactive conversation init #6
20:00 - Proactive conversation init #7
20:41 - NEWS POST #4 ⭐
22:00 - Proactive conversation init #8
23:00 - Nothing
00:00 - New schedule for tomorrow generated
...continues next day
```

---

## 📊 Activity Summary Table

| Activity | Frequency | Trigger | Response Time |
|----------|-----------|---------|---|
| **News Posts** | 4x/day | Scheduled (random times 9-21h) | Immediate |
| **Conversations** | Every 2h | Scheduled (all day) | Immediate |
| **Keyword Reply** | On demand | Keywords found | Immediate |
| **Bot Mention** | On demand | "фунт" in text | Immediate |
| **Reply to Bot** | On demand | Reply to bot message | Immediate |
| **Link Analysis** | On demand | URL in message | ~5 sec (parsing) |
| **Opportunistic** | 15-20% | Known person messages | Immediate |

---

## 🎭 Response Personality

**All responses are:**
- ✅ Sarcastic & cynical
- ✅ Short (1-7 sentences, max 5 words each)
- ✅ Often lies/exaggerates for effect
- ✅ May ignore the actual topic (20% of time)
- ✅ Personal attacks on known people
- ✅ Political opinions (pro-Ukraine, anti-Russia)
- ✅ Always stays in character (45-year-old Alexei Karlyukov from Minsk)

---

## 🚀 First Run Behavior

When bot starts:
1. Immediately sends a news post
2. Initializes scheduler with new random times
3. Starts listening for all triggers
4. Ready for all 8+ types of interactions

---

## 🛠 Commands (User-Initiated)

These require explicit user typing:

| Command | What It Does |
|---------|-------------|
| `/start` | Welcome message + command list |
| `/help` | Full documentation |
| `/stats` | Shows metrics (uptime, message counts, API calls) |
| `/context` | Shows last 10 messages bot remembers |
| `/clear` | Resets context & joke history |

---

## 💾 Memory & Context

- **Remembers:** Last 20 messages in chat
- **Anti-repetition:** Tracks used jokes/taunt vectors
- **Context window:** Uses last 10 messages when generating responses
- **Duration:** Resets on `/clear` command or restart

---

## 📈 Metrics Tracked

The bot automatically tracks:
- Total messages sent/received
- User messages vs bot messages
- Proactive messages count
- API calls (DeepSeek) and errors
- Jokes/taunts used
- Uptime (shown in `/stats`)

View with: `/stats` command

---

## ⚙️ Configuration Changes Made

**Today's update:**
- News posts: Changed from 6x to **4x per day**
- Other activities: No changes
- Conversation initiation: Still every 2 hours
- All keyword triggers: Still active
- All reaction patterns: Unchanged

---

## 📝 Quick Reference

**Bot is MOST active when:**
- 9:00 AM - 9:00 PM (news posting window)
- Every 2 hours (proactive conversations)
- Someone mentions keywords
- Someone mentions "фунт"
- Someone replies to bot message

**Bot is LESS active when:**
- 22:00 - 09:00 (night, no news)
- No messages from users
- Outside trigger topics

**Bot NEVER sends unsolicited:**
- DMs
- @mentions outside scheduled proactive times
- Spam or repetitive messages
