---
name: fb-reels-monetization-playbook
description: "ระบบสแครปและวิเคราะห์ Facebook Reels คู่แข่งด้วย Python เพื่อสกัดเป็นเทมเพลตสคริปต์ทำเงินสำหรับ Affiliate สินค้า"
version: 1.0.0
author: Satang
license: MIT
metadata:
  hermes:
    tags: [facebook, reels, monetization, affiliate, scraping, template]
    related_skills: [facebook-automation-suite, zero-touch-monetization-playbook]
---

# Facebook Reels Monetization Playbook 🚀

สกิลนี้ต่อยอดจาก `facebook-automation-suite` โดยเน้นเป้าหมายที่การ **"หาเงิน" (Monetization)** ผ่านคลิปสั้น (Reels) สกิลนี้ครอบคลุมตั้งแต่สคริปต์ดึงข้อมูลคลิปไวรัลของคู่แข่ง ไปจนถึงเทมเพลตการสร้างคอนเทนต์สำหรับปั้นยอดขาย Affiliate (โดยเฉพาะสินค้า Home/Gadget ราคา 199-499 บาท ตามกลยุทธ์หลัก)

---

## 1. กลยุทธ์การทำเงินจาก Reels (The Strategy)

1. **สอดแนมคู่แข่ง (Spy):** ใช้ Python ดึงข้อมูลโพสต์วิดีโอ (Reels/VOD) จากเพจเป้าหมายหรือเพจคู่แข่ง
2. **สกัด Pain Points:** ดึงคอมเมนต์จากคลิปเหล่านั้นมาวิเคราะห์ว่าลูกค้าชอบอะไร หรือติดปัญหาอะไร
3. **ผลิตซ้ำด้วยเทมเพลต (Re-produce):** นำข้อมูลที่ได้มาใส่ใน "เทมเพลตวิดีโอทำเงิน" 4 รูปแบบ
4. **โพสต์และรับค่าคอมมิชชั่น:** สร้างคลิปใหม่จากสคริปต์ แล้วโพสต์พร้อมแปะลิงก์ Affiliate (>10% Commission)

---

## 2. สคริปต์ Python ค้นหาและวิเคราะห์ Reels

สคริปต์นี้จะเข้าไปดึงโพสต์จากเพจเป้าหมาย กรองเอาเฉพาะโพสต์ที่เป็น **วิดีโอ** เรียงลำดับตามความนิยม (Likes/Comments) เพื่อหาคลิป Reels ที่เป็นไวรัล

```python
from facebook_scraper import get_posts
import time
import json

def scrape_viral_reels(page_name: str, pages_limit: int = 3, min_likes: int = 100):
    print(f"⏳ กำลังค้นหาวิดีโอไวรัลจากเพจ: {page_name}...")
    viral_videos = []
    
    try:
        # ดึงข้อมูลโพสต์และคอมเมนต์
        for post in get_posts(page_name, pages=pages_limit, options={"comments": True}):
            # กรองเฉพาะวิดีโอ (Reels มักจะถูกจัดเป็นวิดีโอ) และยอดไลก์ถึงเกณฑ์
            if post.get('video') and post.get('likes', 0) >= min_likes:
                data = {
                    "post_id": post.get('post_id'),
                    "text": post.get('text', '')[:200] + '...', # เอาข้อความแคปชั่นมาบางส่วน
                    "video_url": post.get('video'),
                    "likes": post.get('likes'),
                    "comments_count": post.get('comments'),
                    "shares": post.get('shares'),
                    "top_comments": []
                }
                
                # เก็บ Top Comments เพื่อหา Pain Point หรือสิ่งที่คนสนใจ
                if 'comments_full' in post:
                    for comment in post['comments_full'][:5]: 
                        data['top_comments'].append(comment['comment_text'])
                        
                viral_videos.append(data)
            time.sleep(2) # สำคัญ: หน่วงเวลาเพื่อป้องกันการถูกแบน
            
    except Exception as e:
        print(f"❌ เกิดข้อผิดพลาด: {e}")
        
    # เรียงลำดับตามยอดแชร์และยอดไลก์ (Engagement สูงสุด)
    viral_videos = sorted(viral_videos, key=lambda x: (x['shares'] or 0, x['likes'] or 0), reverse=True)
    
    print(f"✅ พบวิดีโอไวรัลจำนวน {len(viral_videos)} คลิป")
    
    # Save as JSON for LLM Template processing
    with open(f"{page_name}_viral_reels.json", "w", encoding="utf-8") as f:
        json.dump(viral_videos, f, ensure_ascii=False, indent=4)
        
    return viral_videos

# วิธีใช้งาน: หาคลิปไวรัลจากเพจรีวิวสินค้า (เช่น 'JonesSalad' หรือเพจคู่แข่ง)
# scrape_viral_reels("apple", pages_limit=5)
```

---

## 3. เทมเพลตสคริปต์ Reels สำหรับทำเงิน (Monetization Templates)

เมื่อเราได้ข้อมูลวิดีโอไวรัลและคอมเมนต์ (Pain points) จากสคริปต์ด้านบนแล้ว ให้นำมาสร้างเป็นสคริปต์ Reels ตามเทมเพลตต่อไปนี้ (สามารถให้ AI แต่งตามนี้ได้เลย):

### Template 1: Problem-Agitate-Solve (PAS) 🔥
*เหมาะสำหรับสินค้าที่แก้ปัญหาชัดเจน เช่น ไม้ถูพื้น, หัวก๊อกน้ำแรงดัน*
* **Hook (0-3 วิ):** [พูดถึง Pain Point จากคอมเมนต์ที่ดึงมา] เช่น "ใครเบื่อปัญหา... แบบนี้บ้าง ทำยังไงก็ไม่หายซักที!"
* **Agitate (3-7 วิ):** ขยี้ปัญหาให้ดูแย่ลง "ปล่อยไว้นานๆ ระวังจะ... เสียทั้งเงินเสียทั้งเวลา"
* **Solve (7-15 วิ):** โชว์ภาพ Before/After (Visual Transformation ภายใน 3 วิ) "จนมาเจอตัวนี้... มันช่วยให้... ได้แบบนี้เลย"
* **CTA (15-20 วิ):** "ใครสนใจ กดตะกร้าหน้าโปรไฟล์เลย ลิงก์ใต้คลิปนะ"

### Template 2: 3 Reasons Why (เหตุผลที่ต้องมี) 💡
*เหมาะสำหรับ Gadget, สินค้าไลฟ์สไตล์ ราคา 199-499 บาท*
* **Hook (0-3 วิ):** "3 เหตุผลที่... [ชื่อสินค้า/ประเภทสินค้า] ตัวนี้ กำลังฮิตสุดๆ ในตอนนี้!"
* **Body (3-12 วิ):** 
  - ข้อ 1: [ฟีเจอร์เด่นที่ 1 + ประโยชน์]
  - ข้อ 2: [ฟีเจอร์เด่นที่ 2 + ประโยชน์]
  - ข้อ 3: [ฟีเจอร์เด่นที่ 3 + ตอบโจทย์ Pain Point จากคอมเมนต์]
* **CTA (12-15 วิ):** "คุ้มขนาดนี้ ต้องมีติดบ้านไว้แล้ว พิกัดตะกร้าเหลืองเลยครับ"

### Template 3: The "Secret Hack" (ความลับที่คนไม่รู้) 🤫
*เหมาะสำหรับสินค้าที่ใช้พลิกแพลงได้ หรือช่วยประหยัดเวลา*
* **Hook (0-3 วิ):** "ความลับของ... [ปัญหา] ที่ร้าน... ไม่อยากให้คุณรู้!"
* **Body (3-10 วิ):** "ปกติเรามักจะใช้เวลาเป็นชั่วโมงกับเรื่องนี้ แต่แค่มี [ชื่อสินค้า] คุณสามารถทำเสร็จได้ใน 1 นาที (โชว์การใช้งาน)"
* **CTA (10-15 วิ):** "เลิกทำแบบเดิมๆ แล้วมาลองตัวนี้ดู พิกัดด้านล่างเลย"

### Template 4: Review ตอบคอมเมนต์ (UGC Style) 💬
*เหมาะสำหรับสร้างความน่าเชื่อถือ โดยจำลองตอบคำถามจากคอมเมนต์ที่ดึงมาจากคู่แข่ง*
* **Hook (0-3 วิ):** (แปะสติกเกอร์คอมเมนต์ที่สแครปมาบนหน้าจอ) "จากคอมเมนต์นี้ที่ถามว่า... จริงไหม?"
* **Body (3-12 วิ):** "วันนี้มาพิสูจน์ให้ดูเลยครับ... (ทดสอบสินค้าให้ดูแบบดิบๆ เรียลๆ ไม่ต้องจัดแสงเยอะ)"
* **CTA (12-15 วิ):** "ของจริงตรงปก ไม่จกตา ใครอยากได้ตามไปกดที่ตะกร้าได้เลยครับ"

---

## 4. Prompt สำหรับผูกเข้ากับ LLM (Prefect + CLIProxyAPI)

ให้นำข้อมูล JSON ที่ได้จากสคริปต์ โยนเข้า LLM (ผ่าน CLIProxyAPI) พร้อมกับ Prompt นี้ เพื่อผลิตสคริปต์วิดีโออัตโนมัติ:

```text
คุณคือ Content Creator สาย Affiliate มืออาชีพที่ทำเงินเดือนละ 100,000 บาท 
ฉันมีข้อมูลวิดีโอไวรัลและคอมเมนต์ของลูกค้าจากเพจคู่แข่ง (ดู JSON ด้านล่าง)
หน้าที่ของคุณคือ:
1. วิเคราะห์ Pain points หลักจากคอมเมนต์
2. เลือก 1 ใน 4 เทมเพลต (PAS, 3 Reasons, Secret Hack, UGC) ที่เหมาะสมกับปัญหานี้ที่สุด
3. เขียนสคริปต์วิดีโอ Reels ความยาวไม่เกิน 60 วินาที สำหรับโปรโมทสินค้า [ระบุชื่อสินค้า] ราคา [199-499] บาท
4. สคริปต์ต้องมีภาพประกอบ (Visual cue) ว่าวินาทีไหนต้องโชว์ภาพอะไร (เน้น Before/After ใน 3 วิแรก เพื่อเจาะกลุ่มเป้าหมายทันที)
```

## 5. การบูรณาการกับระบบ Zero-Touch
นำสคริปต์ Python ในข้อ 2 ไปตั้งเป็น Task ใน **Prefect** เพื่อทำงานทุกๆ สัปดาห์ สแกนหาเทรนด์ใหม่ๆ จากเพจคู่แข่ง 3-5 เพจ เมื่อได้สคริปต์มาแล้ว สามารถใช้เครื่องมือตัดต่ออัตโนมัติ (FFmpeg/MoviePy) หรือทำวิดีโอแบบ Faceless แล้วใช้ไลบรารี `facebook-business` (จากสกิล facebook-automation-suite) สั่งโพสต์ลงเพจพร้อมใส่ลิงก์ Affiliate อัตโนมัติ