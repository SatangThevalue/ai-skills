# แม่แบบไฟล์ธุรกรรมทางบัญชีคลังสินค้าและงบการเงิน
# ใช้อ้างอิงสำหรับการพัฒนาตัวระบบคุมบัญชีหลังบ้านหรือนำไปปรับใช้ใน Google Sheets/Obsidian

## 1. ผังบัญชีมาตรฐาน (Chart of Accounts Templates)
เซฟเป็นไฟล์ `coa.csv`

```csv
account_code,account_name_th,account_name_en,category,type
1101,เงินสดในมือ,Cash on Hand,Asset,Current Asset
1102,เงินฝากธนาคาร,Cash at Bank,Asset,Current Asset
1103,ลูกหนี้การค้า,Accounts Receivable,Asset,Current Asset
1104,สินค้าคงเหลือ,Inventory,Asset,Current Asset
1105,ภาษีซื้อที่ยังไม่ถึงกำหนด,Input VAT Pending,Asset,Current Asset
1201,ที่ดิน อาคาร และอุปกรณ์,Property Plant and Equipment,Asset,Non-Current Asset
1202,ค่าเสื่อมราคาสะสม,Accumulated Depreciation,Asset,Contra-Asset
2101,เจ้าหนี้การค้า,Accounts Payable,Liability,Current Liability
2102,ภาษีหัก ณ ที่จ่ายค้างจ่าย,Withholding Tax Payable,Liability,Current Liability
2103,ภาษีขาย,Output VAT,Liability,Current Liability
2201,เงินกู้ยืมระยะยาว,Long-term Loans,Liability,Non-Current Liability
3101,ทุนเรือนหุ้น,Share Capital,Equity,Equity
3102,กำไรสะสม,Retained Earnings,Equity,Equity
4101,รายได้จากการขายสินค้า,Sales Revenue,Revenue,Revenue
4102,รายได้จากการให้บริการ,Service Revenue,Revenue,Revenue
5101,ต้นทุนขาย,Cost of Goods Sold (COGS),Expense,Expense
5102,เงินเดือนและสวัสดิการ,Salaries and Benefits,Expense,Expense
5103,ค่าเช่าและค่าบริการ,Rent Expense,Expense,Expense
5104,ค่าสาธารณูปโภค,Utilities Expense,Expense,Expense
```

## 2. ตัวอย่างการลงสมุดรายวันทั่วไป (General Journal Log Example)
เซฟเป็นไฟล์ `journal.csv`
*หมายเหตุ: คอลัมน์ `amount_satang` บันทึกในหน่วยสตางค์ (Integer) เพื่อป้องกันความคลาดเคลื่อนจาก float*

```csv
entry_id,date,ref_no,account_code,dr_cr,amount_satang,description
1,2026-06-01,PO-260601-01,1104,Dr,15000000,ซื้อสินค้าล็อต 100 ชิ้น (หน่วยละ 150 บาท)
1,2026-06-01,PO-260601-01,1105,Dr,1050000,ภาษีซื้อ 7%
1,2026-06-01,PO-260601-01,2101,Cr,16050000,ตั้งเจ้าหนี้การค้า
2,2026-06-05,SO-260605-01,1102,Dr,3210000,รับเงินค่าขายสินค้า 10 ชิ้น
2,2026-06-05,SO-260605-01,4101,Cr,3000000,รายได้จากการขาย (หน่วยละ 300 บาท)
2,2026-06-05,SO-260605-01,2103,Cr,210000,ภาษีขาย 7%
3,2026-06-05,SO-260605-01,5101,Dr,1500000,บันทึกต้นทุนขาย 10 ชิ้น (ล็อตที่ 1 ทุน 150 บาท)
3,2026-06-05,SO-260605-01,1104,Cr,1500000,ตัดยอดสต๊อกสินค้าคงเหลือ
```

## 3. ตัวอย่างการจัดการ Stock Card (Inventory Stock Card Template)
เซฟเป็นไฟล์ `stock_card.csv`

```csv
date,doc_no,txn_type,qty_in,cost_in_satang,qty_out,cost_out_satang,balance_qty,balance_value_satang,notes
2026-06-01,PO-260601-01,IN,100,15000,0,0,100,1500000,รับเข้าล็อต 1 ทุน 150 บาท
2026-06-03,PO-260603-01,IN,50,16000,0,0,150,2300000,รับเข้าล็อต 2 ทุน 160 บาท
2026-06-05,SO-260605-01,OUT,0,0,10,15000,140,2150000,ขายสินค้า 10 ชิ้น (ตัด FIFO ล็อต 1 ทุน 150 บาท)
```
