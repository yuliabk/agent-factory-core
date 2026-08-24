# כלים ותקציב ניסוי

## עקרון תקציבי

תקרת הניסוי היא 200-500 ₪ בחודש. הסכומים להלן הם מעטפות תקציב פנימיות, לא מחירון ספק. לפני רכישה או מעבר ל-Production יש לאמת מחירים עדכניים.

| קטגוריה | כלי מוצע | מעטפת חודשית |
|---|---|---:|
| Agent ו-Knowledge Runtime | Dify Cloud או Self-hosted | 0-150 ₪ |
| Automation | n8n Cloud או Self-hosted | 0-150 ₪ |
| Model ו-Embeddings | OpenAI API עם Limits | 50-200 ₪ |
| Storage ו-Backups | Managed Postgres/Object Storage | 0-75 ₪ |
| Email ו-Website channel | ספק קיים או Free Tier | 0-50 ₪ |
| WhatsApp | נדחה עד Phase 3 | מחוץ ל-MVP הראשוני |

התקציב בפועל יישמר באמצעות Usage Caps, מודלים חסכוניים למשימות פשוטות, Caching, הגבלת Context ו-Evaluation לפני הרחבת שימוש.

## חלופות ארכיטקטורה

### מסלול A - Cloud Low-Code

- יתרון: הקמה מהירה וכמעט ללא תחזוקת שרתים.
- חסרון: עלות חודשית גבוהה יותר ופחות שליטה על Data Residency.
- מתאים: פיילוט מהיר ומידע לא רגיש.

### מסלול B - Self-hosted

- יתרון: שליטה טובה יותר ויכולת בידוד.
- חסרון: דורש תחזוקה, עדכונים, גיבויים ואבטחה.
- מתאים: לאחר שה-Workflow יציב או כאשר לקוח דורש שליטה בתשתית.

### המלצת MVP

להתחיל ב-Cloud או Sandbox מנוהל עם נתונים סינתטיים. רק לאחר שה-Evaluations עוברות, לבחור מסלול Production לפי רגישות הלקוח.

## כלים שאינם נדרשים בשלב הראשון

- Kubernetes.
- מערכת Multi-agent מורכבת.
- Vector Database ייעודי לפני שנפח המסמכים מצדיק זאת.
- WhatsApp Production.
- Fine-tuning.

