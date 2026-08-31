---
name: mql5-onnx-gui-integration
description: คู่มือและโครงสร้างโค้ดสำหรับสร้าง MQL5 EA ที่มีการเชื่อมต่อโมเดล ONNX (Machine Learning) และการสร้าง GUI Dashboard บนกราฟ (Chart)
---

# MQL5 ONNX & GUI Integration

สกิลนี้ช่วยในการสร้าง MQL5 Expert Advisor (EA) หรือ Indicator ที่มี 2 องค์ประกอบหลัก:
1. **ONNX (Open Neural Network Exchange):** การนำเข้าโมเดล AI/ML ที่เทรนจาก Python (เช่น PyTorch/Scikit-learn) มาใช้ทำนายทิศทางตลาด
2. **GUI Dashboard:** การสร้างหน้าต่างโต้ตอบ (Panel) บนหน้าจอกราฟ MT5 โดยใช้ MQL5 Standard Library (`Controls`) และการจัดการ Event ด้วย `OnChartEvent`

## 1. การเชื่อมต่อและใช้งาน ONNX ใน MQL5

MQL5 รองรับไฟล์ `.onnx` แบบ native ทำให้สามารถรัน Inference ได้รวดเร็วโดยไม่ต้องเรียก Python ภายนอก

### Workflow การใช้ ONNX:
1. โหลดไฟล์โมเดล: `OnnxCreate()` หรือ `OnnxCreateFromBuffer()`
2. กำหนดรูปร่างและชนิดข้อมูล (Shape & Type): `OnnxSetInputShape()`, `OnnxSetOutputShape()`
3. การคำนวณ (Inference): `OnnxRun()`
4. คืนหน่วยความจำ: `OnnxRelease()`

### โค้ดตัวอย่าง ONNX:
```mql5
#resource "model.onnx" as uchar ExtModel[]

long     ExtOnnxHandle = INVALID_HANDLE;

int OnInit()
{
   // 1. สร้าง ONNX Model จาก Resource Buffer
   ExtOnnxHandle = OnnxCreateFromBuffer(ExtModel, ONNX_DEFAULT);
   if(ExtOnnxHandle == INVALID_HANDLE)
   {
      Print("OnnxCreateFromBuffer error: ", GetLastError());
      return(INIT_FAILED);
   }

   // 2. กำหนด Input Shape (ตัวอย่าง: Batch=1, Features=10)
   const long input_shape[] = {1, 10};
   if(!OnnxSetInputShape(ExtOnnxHandle, ONNX_DEFAULT, input_shape))
   {
      Print("OnnxSetInputShape error: ", GetLastError());
      return(INIT_FAILED);
   }

   // 3. กำหนด Output Shape (ตัวอย่าง: Batch=1, Output=1)
   const long output_shape[] = {1, 1};
   if(!OnnxSetOutputShape(ExtOnnxHandle, 0, output_shape))
   {
      Print("OnnxSetOutputShape error: ", GetLastError());
      return(INIT_FAILED);
   }
   
   return(INIT_SUCCEEDED);
}

void OnDeinit(const int reason)
{
   if(ExtOnnxHandle != INVALID_HANDLE)
   {
      OnnxRelease(ExtOnnxHandle);
      ExtOnnxHandle = INVALID_HANDLE;
   }
}

// ฟังก์ชันสำหรับเรียกใช้งานโมเดล
double Predict(matrix &inputs)
{
   if(ExtOnnxHandle == INVALID_HANDLE) return 0;
   
   vector output_data;
   // 3. รัน Inference
   if(!OnnxRun(ExtOnnxHandle, ONNX_NO_CONVERSION, inputs, output_data))
   {
      Print("OnnxRun error: ", GetLastError());
      return 0.0;
   }
   
   return output_data[0];
}
```

## 2. การสร้าง GUI Dashboard บนหน้าจอกราฟ (Chart)

สำหรับการสร้างหน้าจอ Interface แนะนำให้ใช้ **MQL5 Standard Library (`<Controls\Dialog.mqh>`)** เพราะมีโครงสร้างแบบ OOP จัดการเรื่อง Event, การลากหน้าต่าง (Drag-and-drop) และ Object Life-cycle ได้ดีกว่าการใช้ `ObjectCreate()` เปล่าๆ

### โครงสร้างการสร้าง GUI Panel:
```mql5
#include <Controls\Dialog.mqh>
#include <Controls\Button.mqh>
#include <Controls\Label.mqh>

class CAIPanel : public CAppDialog
{
private:
   CButton           m_btnPredict;
   CLabel            m_lblResult;

public:
                     CAIPanel(void) {}
                    ~CAIPanel(void) {}
   
   // ฟังก์ชันหลักที่ใช้สร้างหน้าจอ
   virtual bool      Create(const long chart, const string name, const int subwin, const int x1, const int y1, const int x2, const int y2);
   
   // การผูก Event (คลิกปุ่ม)
   EVENT_MAP_BEGIN(CAIPanel)
      ON_EVENT(ON_CLICK, m_btnPredict, OnClickPredict)
   EVENT_MAP_END(CAppDialog)

protected:
   bool              CreateButton(void);
   bool              CreateLabel(void);
   void              OnClickPredict(void); // สิ่งที่จะทำเมื่อคลิกปุ่ม
};

// ... (หลังจากนี้คือการ Implement การจัดวาง Layout และฟังก์ชัน OnClick)
```

### การผูก Event ในโปรแกรมหลัก:
สิ่งที่สำคัญที่สุดคือต้องรับ Event จาก MT5 ด้วยฟังก์ชัน `OnChartEvent` แล้วส่งต่อให้ Panel
```mql5
CAIPanel panel;

int OnInit()
{
   // สร้างหน้าต่างขนาดกว้าง 300 สูง 200
   if(!panel.Create(0, "AI Dashboard", 0, 20, 20, 320, 220))
      return(INIT_FAILED);
      
   panel.Run(); // วาดขึ้นจอ
   return(INIT_SUCCEEDED);
}

void OnDeinit(const int reason)
{
   panel.Destroy(reason); // ล้างหน้าจอเมื่อปิด EA
}

// จำเป็นต้องมีเพื่อให้ GUI รับรู้การคลิกเมาส์
void OnChartEvent(const int id, const long &lparam, const double &dparam, const string &sparam)
{
   panel.ChartEvent(id, lparam, dparam, sparam);
}
```

## 3. Best Practices & Pitfalls (ข้อควรระวัง)

1. **ONNX Data Preprocessing**: ข้อมูลดิบจากตลาด (เช่น Open, High, Low, Close, RSI) จะต้องถูก **Normalize/Scale (เช่น Z-Score, Min-Max)** ใน MQL5 ให้เหมือนกับตอนที่เตรียมข้อมูลฝึก (Train) ใน Python ทุกประการ หากลืมขั้นตอนนี้ ค่า Predict จะผิดเพี้ยนทันที
2. **Resource Embedded (`#resource`)**: ควรรวมไฟล์ `.onnx` เข้าไปเป็น Resource ในตัว EA เสมอ (ใช้ `.ex5` ไฟล์เดียวจบ) เพื่อไม่ให้เกิดปัญหาผู้ใช้ลืม Copy ไฟล์โมเดลไปใส่ใน Folder `MQL5/Files`
3. **Threading & Performance**: ฟังก์ชัน `OnnxRun()` ทำงานอยู่บน Thread หลักเดียวกับ Chart ถ้าโมเดลของคุณลึกมาก การเรียกใช้ทุกๆ Tick อาจจะทำให้กราฟค้างได้ (UI Freeze) แนะนำให้เรียก `OnnxRun()` เฉพาะตอน **ขึ้นแท่งเทียนใหม่ (New Bar)** หรือรันแบบหน่วงเวลา
4. **CCanvas สำหรับกราฟิกขั้นสูง**: หากคุณไม่พอใจกับหน้าต่างแบบ CAppDialog และต้องการวาด Heatmap, เกจวัดระดับ หรือกราฟิกที่ต้องควบคุม Pixel เอง ให้ใช้ `<Canvas\Canvas.mqh>` ควบคู่กัน (ใช้วาด Pixel แบบอิสระแล้วแนบรูปลงกราฟ)
