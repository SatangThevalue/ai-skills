# Agent Frameworks Installation & Compatibility Guide (Python 3.11)

คู่มือการติดตั้งและตรวจสอบความเข้ากันได้ของ 4 Framework AI Agent ยอดนิยม (CrewAI, LangGraph, AutoGen, CAMEL) ในสภาพแวดล้อม VPS ผ่าน `uv`

---

## 1. การติดตั้งแบบครบชุด (Unified Venv)

ทั้ง 4 ไลบรารีสามารถ Resolve dependencies ร่วมกันบน **Python 3.11** ได้สำเร็จโดยไม่มีข้อขัดแย้ง:

```bash
mkdir -p ~/agent-frameworks && cd ~/agent-frameworks
uv venv .venv --python python3.11
source .venv/bin/activate

# ติดตั้งครบ 4 ตัวในคำสั่งเดียว
uv pip install crewai langgraph pyautogen camel-ai
```

---

## 2. เวอร์ชันและข้อกำหนดการ Import (Import Syntax Quirks)

| Framework | Verified Version | แพ็กเกจที่ลง | คำสั่ง Import ที่ถูกต้อง | ข้อควรระวัง |
|---|---|---|---|---|
| **CrewAI** | `1.15.23` | `crewai`, `crewai-core` | `import crewai` | ต้องระวัง tokenizers/onnxruntime dependencies |
| **LangGraph** | `1.2.12` | `langgraph`, `langgraph-checkpoint` | `import langgraph` | โมดูลไม่มีแอตทริบิวต์ `__version__` ให้เช็คผ่าน `importlib.metadata` |
| **AutoGen** | `0.7.5` | `pyautogen`, `autogen-agentchat` | `import autogen_agentchat`<br>`import autogen_core` | **ห้ามใช้** `import autogen` แบบเดี่ยวๆ ในเวอร์ชันใหม่ (0.4+) เพราะแยก Core กับ AgentChat |
| **CAMEL** | `0.2.90` | `camel-ai` | `import camel` | ใช้ร่วมกับ Pydantic v2 ได้ราบรื่น |

### สคริปต์ตรวจสอบความพร้อม (Verification One-liner):

```python
python -c "
import crewai, langgraph, autogen_agentchat, autogen_core, camel, importlib.metadata
print('CrewAI:', importlib.metadata.version('crewai'))
print('LangGraph:', importlib.metadata.version('langgraph'))
print('AutoGen:', importlib.metadata.version('autogen-agentchat'))
print('CAMEL:', importlib.metadata.version('camel-ai'))
print('✅ ALL 4 FRAMEWORKS ACTIVE')
"
```

---

## 3. การกู้คืนพื้นที่ดิสก์ (Disk Space Management)

การติดตั้ง 4 Framework พร้อมกันจะดาวน์โหลด Wheels ราว 117 แพ็กเกจ (~2.5GB Cache) 
บน VPS ที่มีพื้นที่จำกัด (เช่น < 10GB) **ต้องรันคำสั่งเคลียร์ Cache ทันทีหลังติดตั้ง**:

```bash
uv cache clean
# คืนพื้นที่ดิสก์ทันที 2.5 - 2.8 GB
```
