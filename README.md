# extract-bodogames-csv

[ボードゲーマ](https://bodoge.hoobby.net/)のユーザーのボードゲーム一覧ページから、ボードゲームのデータを CSV で出力するスクリプト
`.env` の `TARGET_URL` に対象 URL を入力して起動することで CSV ファイルが出力されます。


# セットアップ

1. 自身のChrome のバージョンを調べる。
<img width="396" alt="image" src="https://user-images.githubusercontent.com/7589567/224527168-17429274-ffb6-4b26-9de5-35d9c4362457.png">

2. 対応するバージョンの[chromedriver](https://chromedriver.chromium.org/downloads) のインストール

3. env のセット

``` bash 
echo TARGET_URL='{対象のユーザーのボードゲーム一覧ページURL}' >> .env
```

# 実行

```bash
python3 main.py
```
