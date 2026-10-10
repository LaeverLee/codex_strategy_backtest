# Codex BTC Strategy Backtest

讓沒有前文的Codex接手BTC策略回測：讀取找策略Skill提交的候選，使用既有Zeabur/OpenClaw Python引擎，核對完整證據、Supabase帳本及驗收結果，再向指定Discord通知。由Codex理解及審查；Python做固定數值運算；不呼叫MiniMax、不下實盤單。

## 從這裡開始

1. [AGENTS](AGENTS.md)與[目前狀態](memory/CURRENT_STATE.md)：先知道授權及部署邊界。
2. [回測Skill](skills/btc-strategy-backtest/SKILL.md)。
3. [回測計畫及規則](skills/btc-strategy-backtest/references/回測規則與執行計畫.md)。
4. [Zeabur操作](skills/btc-strategy-backtest/references/Zeabur連線與操作.md)。
5. [Supabase模型](docs/SUPABASE_DATA_MODEL.md)及[故障恢復](docs/RECOVERY_AND_QUERIES.md)。
6. [排程接管與通知](skills/btc-strategy-backtest/references/排程接管與通知.md)。
7. [已知限制及驗收](docs/LIMITATIONS_AND_ACCEPTANCE.md)。

研究上游在 https://github.com/LaeverLee/codex_strategy_hunt 。本repo不取代來源研究，也不為了50%門檻改策略。

## 部署狀態

2026-10-11：新Skill及bridge已建立並以遠端health、inspect、策略2實際結果做只讀驗證；尚未啟用Codex回測排程，尚未取代OpenClaw每5分鐘回測job。engine是可追查移交副本，無人聲稱本次已部署。現有佇列為空、舊搜尋停用、既有回測啟用；狀態會變，接手須重查。

驗收：驗證與測試各BTC累積淨報酬≥50%、交易≥30、PF≥1.1、Sharpe≥0.5、浮動回撤≤15%；三子段至少兩正、1.5倍成本後正。qualified只是歷史研究通過，非實盤資格。

## 檔案

| 位置 | 內容 |
|---|---|
| skills/btc-strategy-backtest | 可匯出Skill、操作工具、完整references與認證範例 |
| engine | 固定回測、驗證、行情與Supabase同步副本 |
| config | 實際欄位快照、歷史schema與引擎hash；無密鑰 |
| examples | 真實策略2摘要及獨立audit結果，不是fixture |
| memory | 使用者意圖、決策與部署狀態 |
| tests | 政策、失敗資料、格式及無模型調度檢查 |

Python bridge只需標準函式庫及本機ssh。Linux引擎需要numpy/pandas與fcntl；版本未固定，不應宣稱可跨版本完全相同。先記錄現有依賴再部署。測試：python -X utf8 -m unittest discover -s tests -v。

本repo沒有私鑰、密碼、Worker Token、完整Webhook、原始行情或完整曲線。不同Agent必須取得自己的SSH存取權。匯出Skill不會自動建立排程。這不是整台伺服器備份。
