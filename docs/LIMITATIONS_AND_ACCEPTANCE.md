# 實作、驗證與限制

## 本次已驗證

bridge health連新專案；inspect Ready Pod、空queue與兩job啟用狀態；result讀真實策略2、保存完整報告在原本機私密工作區，輸出摘要及audit consistent=true、qualified=false。讀取無DB寫入、不重新回測、不發重複通知。政策/缺數值/邊界/語法等測試見tests。

## 本次尚未驗證或啟用

新bridge run/sync寫入入口、Codex新排程接管、通知端到端、全新資料的回測重現均未執行。現有引擎有真實策略2歷史完成證據，但不能代替新接管驗收。新Skill未安裝到原機生產skills，repo可匯出安裝。

## 現有引擎限制

- evaluate_isolated是程序隔離及程式檢查，不是完整OS網路/檔案沙箱；嚴格沙箱是待實作。
- fixture-only例外仍存在engine，Skill禁止用在正式帳本；移除須另驗證部署。
- 成本可由環境覆寫；通知前核實result成本與政策。
- 快取按version+code_hash、evaluation鍵不含資料/引擎/政策hash；結果檔存在時不會自動重跑新資料。同版本重測可能覆盖DB評估，需新鍵設計。
- qualified對NaN防護不完整；獨立audit已補檢查但未修改遠端引擎。audit不驗來源/成本/資料，仍須前置核對。
- 部分fold/stress沒有交易曲線；資料庫status可能滯後、run finished_at可能空。
- source semantic review由Codex核對，不是獨立模型证明。
- 日線、動態ROI、trailing、限價與intrabar順序未完整支持。
- 沒有新獨立holdout、完整參數穩健性與風險匹配基準，qualified不授權實盤。

## 之後驗收

新接管真實候選必须核對source review/程式與spec/hash、固定成本/資料快照、七split及audit、交易曲線、DB關聯、archive、HTTP通知。重複輪次不重跑、不重送；中途失敗保留證據可恢復；舊新排程不能並行领queue。完全相同環境輸入再計算的重現測試應在獨立目录進行，不污染正式DB。
