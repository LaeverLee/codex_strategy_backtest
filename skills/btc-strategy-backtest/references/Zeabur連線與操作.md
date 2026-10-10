# Zeabur連線與實際操作

## 1. 認證與路徑

本機Python→ssh root@8.209.199.155→kubectl exec Ready服務Pod→Python runtime→新Supabase Worker。不是透過OpenClaw對話生成策略，無MiniMax。

namespace=environment-69e0f4905ae0a69725e92658，Service=69e0fa56345a78e2a2f79a25，root=/home/node/.openclaw/workspace/strategy_lab_v7/sessions。Pod會改變，自動探索而非固定名稱。

私密Worker=/home/node/.openclaw/workspace/strategy_lab_v7/connection.json；OpenClaw設定及SQLite私密job不能全文dump。原電腦連線C:/Users/250726/Documents/Codex/2026-10-08/new-chat-2/work/zeabur-codex.json，key C:/Users/250726/.ssh/btc_strategy_codex；別台電腦用自己金鑰，模板identity_file替换自己的絕對路徑。初次ssh核host key，無人值守需可用ssh agent或專用認證。bridge拒絕未知host key，不略過。

## 2. 安裝與命令

將btc-strategy-backtest資料夾放入自己的Codex skills。連線模板另複製到config/connection.local.json，不提交。Python bridge標準庫足夠；Linux引擎numpy/pandas/fcntl。Skill匯出不包含伺服器登入、排程或行情。

從repo根目錄執行（Windows可用Python絕對路徑）：

```text
python -X utf8 skills/btc-strategy-backtest/scripts/backtest_bridge.py health --config config/connection.local.json
python -X utf8 skills/btc-strategy-backtest/scripts/backtest_bridge.py inspect --config config/connection.local.json
python -X utf8 skills/btc-strategy-backtest/scripts/backtest_bridge.py result --config config/connection.local.json --version 2 --output private/2.json
python -X utf8 skills/btc-strategy-backtest/scripts/verify_result.py private/2.json
```

result只印摘要與audit，完整報告保存--output；不存在回RESULT_PENDING。verify_result退出0表示audit與引擎判定一致（不代表盈利），退出2是不一致。

只有接管排程、策略前置檢查完成後才執行以下寫入：

```text
python -X utf8 skills/btc-strategy-backtest/scripts/backtest_bridge.py run --config config/connection.local.json --execute
python -X utf8 skills/btc-strategy-backtest/scripts/backtest_bridge.py sync --config config/connection.local.json --execute
```

run用既有lab_runtime.py backtest，取得/tmp/backtest_research_v7.lock，先sync、跑一候選、finally再sync；傳輸最多等待900秒。run失聯可能遠端仍在跑，先inspect程序/result，不重複盲跑。--execute是CLI寫入意圖，不替代使用者排程接管授權。

## 3. 結果位置

pytest/Strategy待測；pytest/research_results/<version>.json完整结果；<version>.rejected.json技術拒絕；Research_Qualified/Rejected歸檔；goldhuntv2/research與sync_journal重播來源。原始行情pytest/k_line_data/<tf>/*.csv、funding_BTCUSD_PERP.csv及manifest。完整py/json/spec/code hash與DB互核。

## 4. 部署副本

本repo engine無模型調度且未部署。config/engine-manifest.json是本地hash；部署前與inspect遠端hash比，差異須逐一閱讀備份。遠端runtime目前保留舊入口，禁止呼叫hunt。bridge無install功能，不會默默覆蓋引擎。依賴尚無lockfile，不能聲稱跨版本bitwise reproducibility。不得直接執行schema-reference.sql。
