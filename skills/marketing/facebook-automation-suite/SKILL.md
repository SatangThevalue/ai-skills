---
name: facebook-automation-suite
description: "คู่มือและการสร้างสคริปต์สำหรับจัดการ Facebook Fanpage (โพสต์ออโต้, ดูดข้อมูล, ดึงคอมเมนต์) ผ่าน Python"
version: 1.0.0
author: Tonthong
license: MIT
metadata:
  hermes:
    tags: [facebook, automation, api, scraping, social-media]
    related_skills: [content-marketing-2026-2027, ai-fluency-framework]
---

# Facebook Fanpage Automation Suite

สกิลนี้รวบรวมเทคนิคและการใช้งานไลบรารี Python ยอดนิยม 2 ตัวในการจัดการ Facebook Fanpage สำหรับโปรเจคหาเงินอัตโนมัติ (Zero-Touch) โดยแบ่งออกเป็น "สายขาว" (ใช้ Official API) และ "สายเทา" (ใช้ Web Scraper)

## 1. ไลบรารีที่เลือกใช้

| เป้าหมาย | ชื่อไลบรารี | คำอธิบาย |
| :--- | :--- | :--- |
| **สายโพสต์ / แอดมิน (สายขาว)** | `facebook-python-business-sdk` (Official) | เครื่องมือทางการจาก Facebook (Meta) อัปเดตล่าสุด ใช้ยิงโฆษณา, ดึงคอมเมนต์, โพสต์คอนเทนต์ลงเพจตัวเอง |
| **สายดูดข้อมูล (สายเทา/วิจัย)** | `facebook-scraper` | เครื่องมือดึงข้อมูล (โพสต์, รูป, คอมเมนต์) จาก "เพจคู่แข่ง" หรือกลุ่มสาธารณะ โดยไม่ต้องขอ API Key |

---

## 2. วิธีการติดตั้ง

```bash
# ติดตั้งผ่าน uv ภายใน Virtual Environment ของเรา
uv pip install facebook-business facebook-scraper
```

---

## 3. รูปแบบการใช้งาน (Recipes)

### Recipe 3.1: โพสต์คอนเทนต์/รูปภาพลงเพจตัวเอง (สายขาว)
*ใช้ `facebook-python-business-sdk` เพื่อให้ AI สามารถนำคอนเทนต์ที่สร้างเสร็จแล้วไปโพสต์ลงเพจได้เองทุกวัน*

**ข้อกำหนด:** ต้องมี `PAGE_ACCESS_TOKEN` และ `PAGE_ID` (ได้จากการสร้าง App ใน Facebook Developers)

```python
import os
from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.page import Page

def auto_post_to_page(message: str, image_url: str = None):
    # กำหนดค่าตัวแปร
    access_token = os.getenv('FB_PAGE_ACCESS_TOKEN')
    page_id = os.getenv('FB_PAGE_ID')
    
    # ยืนยันตัวตน
    FacebookAdsApi.init(access_token=access_token)
    page = Page(page_id)
    
    try:
        if image_url:
            # โพสต์พร้อมรูปภาพ
            page.create_photo(params={
                'url': image_url,
                'caption': message
            })
        else:
            # โพสต์ข้อความล้วน
            page.create_feed(params={
                'message': message
            })
        print("✅ Posted successfully to Facebook Page!")
    except Exception as e:
        print(f"❌ Failed to post: {e}")
```
### Recipe 3.1.2: การจัดการโพสต์ คอมเมนต์ และวิดีโอ (Graph API เชิงลึก)
*สามารถนำไปประยุกต์ใช้ในการแก้ไขโพสต์, ตอบกลับคอมเมนต์ (Auto-reply), หรือโพสต์ Video Reels ได้*

```python
from facebook_business.adobjects.pagepost import PagePost
from facebook_business.adobjects.comment import Comment

# 1. แก้ไขโพสต์เดิม (Update Post)
def update_page_post(post_id: str, new_message: str):
    post = PagePost(post_id)
    try:
        post.api_update(params={'message': new_message})
        print(f"✅ Post {post_id} updated!")
    except Exception as e:
        print(f"❌ Update failed: {e}")

# 2. ตอบกลับคอมเมนต์อัตโนมัติ (Reply to Comment)
def reply_to_comment(comment_id: str, reply_message: str):
    comment = Comment(comment_id)
    try:
        # NOTE: การตอบคอมเมนต์ใช้ฟังก์ชันสร้างคอมเมนต์ซ้อนเข้าไป
        comment.create_comment(params={'message': reply_message})
        print(f"✅ Replied to comment {comment_id}!")
    except Exception as e:
        print(f"❌ Reply failed: {e}")

# 3. โพสต์วิดีโอ (Reels / Video)
def auto_post_video(page_id: str, video_filepath: str, description: str):
    page = Page(page_id)
    try:
        video = page.create_video(params={
            'description': description,
            'published': 'true'
        }, files={
            'source': video_filepath
        })
        print(f"✅ Video posted successfully! ID: {video.get('id')}")
        return video.get('id')
    except Exception as e:
        print(f"❌ Video upload failed: {e}")
        return None

### Recipe 3.1.3: Auto-Pin Comment สำหรับ Reels & Affiliate Link
*Facebook Reels ในไทยไม่มีปุ่มตะกร้าเหมือน TikTok กลยุทธ์หลักในการทำ Affiliate และขายของคือ "ยิงคอมเมนต์แรกอัตโนมัติแล้วสั่งปักหมุด (Pin Comment)" ทันทีที่วิดีโอโพสต์สำเร็จ*

```python
import requests

def post_and_pin_first_comment(page_access_token: str, post_id: str, comment_text: str):
    """
    สร้างคอมเมนต์แรกใต้โพสต์/Reel แล้วสั่งปักหมุด (Pinned Comment)
    """
    url = f"https://graph.facebook.com/v19.0/{post_id}/comments"
    params = {
        "access_token": page_access_token,
        "message": comment_text
    }
    resp = requests.post(url, data=params).json()
    comment_id = resp.get("id")
    if not comment_id:
        print(f"❌ Create comment failed: {resp}")
        return False

    # สั่งปักหมุดคอมเมนต์ผ่าน Graph API
    pin_url = f"https://graph.facebook.com/v19.0/{post_id}"
    pin_params = {
        "access_token": page_access_token,
        "pinned_comment_id": comment_id
    }
    pin_resp = requests.post(pin_url, data=pin_params).json()
    if pin_resp.get("success"):
        print(f"✅ Comment {comment_id} pinned successfully!")
        return True
    else:
        print(f"⚠️ Pinning note: {pin_resp}")
        return True
```
```

### Recipe 3.2: สแครปข้อมูลและคอมเมนต์จากเพจอื่น (สายดูดข้อมูล)
*ใช้ `facebook-scraper` เหมาะกับการเอาไปส่องคู่แข่งว่าเขาขายของดีไหม ลูกค้าคอมเมนต์ว่าอะไร แล้วเอา Data นั้นมาให้ AI แต่งสคริปต์วิดีโอของเรา*

**ข้อจำกัด:** Facebook ปรับโครงสร้างเว็บดักบ่อย สคริปต์นี้อาจจะติด Limit (ควรหน่วงเวลา และสลับ IP หากดึงเยอะ)

```python
from facebook_scraper import get_posts
import time

def scrape_competitor_page(page_name: str, pages_limit: int = 1):
    print(f"⏳ เริ่มดึงข้อมูลจากเพจ {page_name}...")
    results = []
    
    # วนลูปดึงโพสต์จากเพจ (แนะนำให้ตั้งหน่วงเวลา เพื่อไม่ให้โดนบล็อก)
    for post in get_posts(page_name, pages=pages_limit, options={"comments": True}):
        data = {
            "post_id": post['post_id'],
            "text": post['text'],
            "time": post['time'].strftime('%Y-%m-%d %H:%M:%S') if post['time'] else None,
            "likes": post['likes'],
            "comments_count": post['comments'],
            "shares": post['shares'],
            "top_comments": []
        }
        
        # เก็บข้อมูลคอมเมนต์ (เพื่อเอามาหา Pain point ลูกค้า)
        if 'comments_full' in post:
            for comment in post['comments_full'][:5]:  # เอาแค่ 5 คอมเมนต์เด่น
                data['top_comments'].append(comment['comment_text'])
                
        results.append(data)
        time.sleep(2) # หน่วงเวลาสำคัญมาก
        
    print(f"✅ ดึงมาได้ {len(results)} โพสต์")
    return results
```

---

## 4. แผนประยุกต์ใช้เพื่อ "หาเงิน"
คุณสตางค์สามารถนำ 2 ไลบรารีนี้มาผูกกันใน Prefect Pipeline ได้เลย:
1. **[Data Extraction]:** ใช้ `facebook-scraper` วิ่งไปดูดโพสต์สินค้าขายดีของเพจร้านดัง หรือเพจคู่แข่ง (ดูว่าลูกค้าคอมเมนต์ด่า หรือชมเรื่องอะไร)
2. **[AI Ideation]:** นำข้อความที่ดึงมา (เช่น ลูกค้าด่าว่าสายชาร์จพังง่าย) ไปบอก LLM (CLIProxyAPI) ให้เขียนสคริปต์วิดีโอของเรา โดยเน้น Hook เรื่อง "สายชาร์จถึกทน"
3. **[Auto-Publish]:** เมื่อ AI ทำคลิปและ Caption พร้อม HashTag เสร็จ ก็ใช้ `facebook-python-business-sdk` (Official) สั่งโพสต์คลิปนั้นลงเพจ Facebook / Reels ของเราเองอัตโนมัติ
4. **[Auto-Pin & Multi-Page Flipping]:** ปั้นชุดเพจ 10-15 เพจกระจาย 4 Niche (จิตวิทยา, พัฒนาตัวเอง, คำคม, การเงิน) โดยยิงคลิปสั้น 15-20 วินาที พร้อม Auto-Pin คอมเมนต์ดึงคนไป Affiliate หรือสะสมผู้ติดตาม 5,000-10,000 คนเพื่อขายต่อ (Flipping) ดูรายละเอียดแผนธุรกิจและเมทริกซ์ความเสี่ยงใน `references/page-flipping-and-anti-ban.md`

## 5. การวิเคราะห์ข้อมูลเพจด้วย requests + BeautifulSoup (ทางเลือกสำหรับเพจสาธารณะ)
ในกรณีที่ `facebook-scraper` ถูกบล็อกหรือติดข้อจำกัด สามารถใช้ Python พื้นฐาน (requests + BeautifulSoup) เพื่อดึง meta tags สำคัญ (og:title, og:description) หรือค้นหาข้อมูลใน HTML ของเพจสาธารณะได้ เหมาะสำหรับการสกัดข้อมูลพื้นฐาน เช่น ยอดผู้ติดตาม, บริการ, หรือสโลแกนเพจ

```python
import codecs
import subprocess

def scrape_public_page_info(url: str):
    # ใช้ curl แทน requests เพื่อเลียนแบบเบราว์เซอร์ได้เนียนกว่าในบางกรณี และดึงข้อมูลดิบมาหา text
    cmd = f'curl -s -L -A "Mozilla/5.0 (compatible; Googlebot/2.1; +https://www.google.com/bot.html)" "{url}" > /tmp/fb.html && grep -oP \\'"text":"\\K[^"]+(?=")\\' /tmp/fb.html | head -n 50'
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        # ข้อมูลภาษาไทยมักถูกเข้ารหัสเป็น unicode escape (เช่น \\u0e14)
        decoded_text = codecs.decode(result.stdout.replace('\\\\', '\\'), 'unicode_escape')
        return decoded_text
    except Exception as e:
        return f"Error: {e}"
```

## 6. ข้อควรระวัง (Pitfalls)
- **Account Ban:** ห้ามใช้แอคเคาท์จริงของตัวเองในการใช้ `facebook-scraper` เพื่อดึงข้อมูล (หลีกเลี่ยงการส่ง cookies) ให้ใช้แบบ Guest Mode (ไม่ล็อกอิน) เพื่อลดความเสี่ยงที่เฟสส่วนตัวจะบิน
- **Token Expiry:** `PAGE_ACCESS_TOKEN` ของ Facebook Business API มักจะหมดอายุใน 60 วัน ต้องหาวิธีต่ออายุ (Extend Token) หรือสร้างแบบ Never-expire
- **Multi-Page Posting Detection:** เมื่อโพสต์หลายเพจพร้อมกัน (เช่น 10-15 เพจ) ห้ามยิง API พร้อมกันในเสี้ยววินาทีเด็ดขาด เพราะ Meta จะ Flag ว่าเป็น Spam Bot จาก IP เดียวกัน ให้ตั้ง `random.uniform(120, 420)` (หน่วงเวลา 2–7 นาที) ระหว่างการโพสต์แต่ละเพจเสมอ
- **Audio Duplicate / Shadowban:** เสียงพากย์ AI ห้ามใช้โทนและสปีดเดิม 100% กับทุกเพจ ให้สลับเสียง (เช่น นิวัฒน์ สลับ พรหมวดี) และสุ่มปรับ pitch ±3-5% ในการเรนเดอร์คลิปแต่ละเพจ
