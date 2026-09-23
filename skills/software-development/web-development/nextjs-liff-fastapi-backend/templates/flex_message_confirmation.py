def generate_draft_confirmation_flex(draft_id: str, amount: float, merchant: str, transaction_type: str, liff_id: str) -> dict:
    """สร้าง JSON สำหรับ Flex Message ยืนยันรายการ Draft"""
    
    # กำหนดสีตามประเภทของ transaction
    color = "#ef4444" if transaction_type.lower() == "expense" else "#22c55e"
    type_text = "รายจ่าย" if transaction_type.lower() == "expense" else "รายรับ"
    
    return {
        "type": "flex",
        "altText": f"มีรายการ{type_text}รอให้คุณยืนยัน",
        "contents": {
            "type": "bubble",
            "size": "kilo",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "🤖 AI อ่านข้อมูลสำเร็จ!",
                        "weight": "bold",
                        "color": "#001962",
                        "size": "sm"
                    },
                    {
                        "type": "text",
                        "text": f"฿ {amount:,.2f}",
                        "weight": "bold",
                        "size": "xxl",
                        "margin": "md",
                        "color": color
                    },
                    {
                        "type": "text",
                        "text": f"ร้านค้า: {merchant or 'ไม่ระบุ'}",
                        "size": "xs",
                        "color": "#888888",
                        "wrap": True,
                        "margin": "sm"
                    }
                ]
            },
            "footer": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "button",
                        "style": "primary",
                        "color": "#001962",
                        "action": {
                            "type": "uri",
                            "label": "แก้ไข / ยืนยันรายการ",
                            "uri": f"https://liff.line.me/{liff_id}/liff/confirm/{draft_id}"
                        }
                    }
                ]
            }
        }
    }