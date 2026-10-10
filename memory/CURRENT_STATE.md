# 現況及使用者決策

快照日期2026-10-11（Asia/Taipei），非即時狀態。

使用者先要求回測Codex排程Skill的詳盡計畫，後要求提交至LaeverLee/codex_strategy_backtest，內容越詳盡越好。計畫要求固定門檻、規則、資料分段、來源審查、去重、恢復、Supabase及指定通知。此刻只完成Skill及repo，尚未啟用新排程。

新Supabase jygaprrhtuwzffyrnipt；舊專案不碰。OpenClaw Service69e0fa56345a78e2a2f79a25；namespace environment-69e0f4905ae0a69725e92658。SSH原電腦root@8.209.199.155使用專用金鑰，本repo不含金鑰。

只讀核對：搜尋job52d4bf14-f93e-4f00-8e67-fc770aef6929 disabled；回測job a8f06958-e766-4780-b4bf-a845977100b7 enabled，每5分鐘。queue空。ctrl搜尋current_version3、回測current_version1；不能把control版本當完整完成數量。

策略1來源審查失敗，不當成原策略績效。策略2首次Codex真實候選，1h雙動量5/10，BTCUSDT移植反向BTCUSD受控變體，正式queued且七組回測完成，但qualified=false。驗證-78.443%、測試-88.7498%、浮動DD88.8033%、cost stress-92.7841%。無合格策略，無實盤或紙上交易啟動。

研究仍由Codex btc-codex heartbeat每15分鐘；回測仍OpenClaw既有job。新回測Skill、遠端read-only bridge和獨立metric audit已驗證；run/sync寫入及排程切換未於本次執行。完整輸入資料及曲線仍留原環境，GitHub只有摘要。
