# 使用者要求與對話記憶

本文件重建可見需求與已知處理結果，不是平台逐字對話匯出；密碼/Token/Webhook完整網址已排除。詳細策略研究历史見上游repo。

1. 使用者在Zeabur建立OpenClaw，要求掃描找策略及回測Python、記憶與logs，改善找策略品質。
2. 新紀錄建立於全新Supabase專案，而非舊表混用，專案OpenClaw Strategy Lab、新加坡、LaeverLee組織。
3. BTC累積淨報酬至少50%，后来固定驗證與測試各50%，且其餘風險/交易門檻全部满足。
4. 搜尋由Codex本身讀來源、中文翻譯、生成與審查，不透過MiniMax。Codex研究排程提交到OpenClaw待回測資料夾，保留既有Python引擎。
5. 搜尋每輪即使沒候選也送指定搜尋Webhook；回測另送指定回測Webhook。停用1494372820380160100統一announce。通知目的ID不等於可直接取代完整私密URL。
6. 首個真實候選queued及DB核對後停旧搜尋；已在策略2完成。回測保留。
7. 研究repo要讓全新Codex看懂任務、步驟、記憶及技能。已更新到290c964，詳述DB存放及復原。
8. 使用者：「如果回測也請你做出排程skill，要嚴格遵守回測規則，先給我看看計畫書」。已提供計畫，建議固定Python計算、Codex檢查與解讀；尚未啟用排程。
9. 使用者問Supabase存放邏輯及各表意義是否要寫入，確認必需；已列入此repo及可匯出Skill references。
10. 最新要求：「把回測的commit在這 https://github.com/LaeverLee/codex_strategy_backtest 一樣越詳盡越好」。此次交付Skill、工具、引擎副本、完整文件、實例、測試，commit/push；未做生產接管。

新Agent不可擴大實盤權限、降低門檻、把原source變體叫忠實重現、忽略資料未涵蓋日期，或宣稱历史測試期為全新holdout。没有可信合格候選是允许结果，不為配額捏造。
