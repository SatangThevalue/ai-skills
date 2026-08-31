---
name: thai-dw-price-table
description: "คู่มือและวิธีการดึงข้อมูลตารางราคา DW (Derivative Warrants) ของแต่ละบริษัทผู้ออกหลักทรัพย์ในตลาดหุ้นไทย"
---
# การดึงตารางราคา DW (Derivative Warrants) ในตลาดหุ้นไทย

ตารางราคา DW (Price Table / Matrix) คือตารางที่เปรียบเทียบราคาเสนอซื้อ (Bid) ของหุ้นอ้างอิง กับราคาเสนอซื้อ (Bid) ของ DW ซึ่ง Market Maker (ผู้ออก) เป็นผู้กำหนดและดูแลสภาพคล่อง

เนื่องจากปัจจุบัน **ไม่มี Central API ฟรีที่รวมตารางราคาทุกค่ายไว้ในที่เดียว** การดึงตารางราคาจึงต้องใช้วิธี **Web Scraping หรือการดึงผ่าน Hidden API (XHR/AJAX)** จากเว็บไซต์ของผู้ออกแต่ละราย 

## แหล่งข้อมูลและสถานะของผู้ออกหลัก (Major Issuers)
- **DW01 (Bualuang):** `blswarrant.com` (ดึงตาราง HTML ตรงๆ ได้จาก `https://www.blswarrant.com/mydw/{symbol}`)
- **DW13 (KGI):** `thaiwarrant.com` (ดึงตาราง HTML ตรงๆ ได้จาก `https://www.thaiwarrant.com/dw/{symbol}`)
- **DW19 (Yuanta):** `dw19club.yuanta.co.th` (เว็บไซต์ปิดปรับปรุง หรือเปลี่ยนโดเมน)
- **DW24 (Finansia):** `dw24.co.th` (โดเมนไม่สามารถเข้าถึงได้)
- **DW28 (Macquarie):** `thaidw.com` (ใช้ React SPA (Single Page Application) ซึ่งข้อมูลเรนเดอร์ผ่าน Javascript Client-side และดึง API จาก backend `trkd-hs.com` การดึงตารางตรงๆ ต้องอาศัยเครื่องมือจำลอง Browser อย่าง Selenium, Playwright หรือแกะ API request)
- **DW41 (J.P. Morgan):** `jpmorgandw.com` (โดเมนปิดการเข้าถึง หรือจำกัดวงการเข้าถึง)

## วิธีการดึงข้อมูลที่สามารถทำได้ทันทีด้วย Python (ไม่ต้องใช้ Selenium/Playwright)

### 1. DW01 Bualuang (ใช้ BeautifulSoup แกะ HTML Table)
เว็บไซต์ DW01 มีหน้าตารางราคาที่ถูกเรนเดอร์เป็นตาราง HTML ทันทีเมื่อโหลดหน้าเว็บ ทำให้สามารถกวาดข้อมูลได้ตรงๆ โดยไม่ต้องพึ่ง Browser Automation:
1. URL: `https://www.blswarrant.com/mydw/{dw_symbol}`
2. ใช้ `urllib.request` เปิดหน้าเว็บ (ไม่ต้องใช้ API, ตั้ง Header User-Agent เป็น Mozilla)
3. ตารางราคาจะอยู่ในตารางที่ 2 ของหน้าเว็บ (`tables[1]`)
4. ข้อมูลจะอยู่ใน `<tr>` ซึ่งเราสามารถ clean text เพื่อลบ whitespace เปล่าๆ ออกได้

*(ดูโค้ดที่ `scripts/bualuang_dw_scraper.py`)*

### 2. DW13 KGI (ใช้ BeautifulSoup แกะ HTML Table)
เว็บไซต์ DW13 โหลดตารางราคามาเป็น HTML เช่นกัน
1. URL: `https://www.thaiwarrant.com/dw/{dw_symbol}`
2. ตารางราคาคือตารางที่ 2 ของหน้าเว็บ (`tables[1]`)
3. ข้อมูลวันที่อยู่ใน `<tr>` ที่ 2 และราคาเริ่มที่ `<tr>` ที่ 4

*(ดูโค้ดที่ `scripts/kgi_dw_scraper.py`)*

## กลุ่มค่ายที่ต้องใช้ Browser Automation (Playwright/Selenium)
ค่ายอย่าง **DW28 Macquarie (thaidw.com)**, **DW41 JPMorgan**, **DW24 Finansia**, และ **DW19 Yuanta (dw19club.yuanta.co.th)** ใช้ Client-Side Rendering (React/Vue) และมี API Protection ที่เข้มงวด (CORS, Check Cookie, บล็อก Headless/Curl)
- **ห้าม** ใช้ `urllib` หรือ `requests` ยิงตรงไปยังหน้าเว็บหรือ API (จะโดน Block หรือได้ HTML ว่างๆ กลับมา)
- **การแก้ปัญหา:** ต้องใช้เครื่องมืออย่าง `playwright` หรือ `selenium` เพื่อเปิดเบราว์เซอร์, สั่งให้รอจนกระทั่งตารางโหลดเสร็จ (เช่น `page.wait_for_selector("table")`) แล้วค่อยดึง HTML ที่ได้จากหน้าเพจมาประมวลผลต่อด้วย `BeautifulSoup`

*(ดูตัวอย่างโค้ดที่ `scripts/playwright_dw_scraper.py`)*

## ข้อควรระวังในการทำระบบดึงราคา (Pitfalls)
1. **Rate Limits & IP Blocking:** ควรหน่วงเวลาในการเรียกข้อมูลด้วย `time.sleep()` 
2. **Dynamic / SPA Websites:** ค่ายอย่าง DW28 (Macquarie) ไม่สามารถโหลดด้วย `urllib` แล้วดึงจาก HTML ได้ตรงๆ เพราะตัวเว็บสร้างตารางด้วย Javascript ภายหลัง คุณจะต้องเจาะลึกไปถึง Network Request หรือใช้ `Playwright` / `Selenium` เพื่อเรนเดอร์หน้าเว็บก่อนดึงข้อมูล
3. **Data Expiration:** ตารางราคามี Time Decay (ค่าเสื่อมเวลา) ต้องดู Column วันที่ในตารางประกอบเสมอ ห้ามดึงตารางราคาเก็บไว้ข้ามวันโดยไม่อัปเดต