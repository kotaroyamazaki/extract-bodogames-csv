# extract-bodogames-csv

[ボードゲーマ](https://bodoge.hoobby.net/)のユーザーのボードゲーム一覧ページから、ボードゲームのデータを CSV で出力するスクリプト
`.env` の `TARGET_URL` に対象 URL を入力して起動することで CSV ファイルが出力されます。

# 実行方法

```bash
echo TARGET_URL='{対象のユーザーのボードゲーム一覧ページURL}' >> .env
python3 main.py
```
