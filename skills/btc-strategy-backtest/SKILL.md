---
name: btc-strategy-backtest
description: 由Codex嚴格核對BTC策略候選，透過SSH驅動既有Zeabur Python回測引擎、獨立驗收與同步帳本；供本使用者回測排程，不做策略搜尋或實盤下單。
---

# BTC策略嚴格回測

先讀 references/回測規則與執行計畫.md、references/Zeabur連線與操作.md及references/排程接管與通知.md。涉及DB讀references/Supabase資料模型.md。本Skill安裝不代表排程已啟用，接管須有使用者指示與單一排程所有權。

由Codex審查規格與解讀；固定Python計算，不呼叫MiniMax。每輪最多一候選，不修改來源規則或參數，無候選安靜。先health/inspect，核對來源approved、code hash、db_committed及資料快照。已完成結果先讀，不重測。拒絕規則不完整、未來資訊、源碼變更或fixture；現有程序隔離不能稱完整沙箱。

驗證與測試各BTC累積淨報酬≥50%、交易≥30、PF≥1.1、Sharpe≥0.5、浮動DD≤15%；三子段至少兩正；1.5倍成本淨收益>0。任一缺失、不合理或非有限數值不能合格。用verify_result.py獨立核對全部分段，若與引擎qualified不一致阻擋公告並保存diagnostic，不改DB掩蓋。

執行run前確認舊回測排程已依接管授權停用，保留同一鎖；run回傳成功不等於處理候選成功，必須讀result、metadata、archive、七組evaluation。不得刪鎖、重寫hash或人工設定db_committed。固定成本與分段變更必須新政策及版本；已用测试資料不是新留出。

保存本地backtest-codex/state.json（版本、hash、資料、驗收、同步、通知）及runs/<UTC>/報告。結果完成後先核遠端Python通知收據（backtest_notification_receipts），HTTP成功事件不再由Codex重送；通知失敗依references恢復並核實HTTP，不重新回測。沒有重要變化時Codex對話安靜。連線失敗寫未執行；不得虛構績效。遠端同步不完整按恢復手冊重播，同錯誤兩次後診斷。禁止實盤下單。
