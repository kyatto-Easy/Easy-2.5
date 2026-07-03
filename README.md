======================================================================
         Easy-1.5 プログラミング言語 説明書 (README)
======================================================================

このプログラムは、独自の簡単な日本語・英語コマンドを使って、
簡易的なゲーム演出やAIチャット、ステータス操作が楽しめるコードエディタです。

----------------------------------------------------------------------
💡 基本的な機能
----------------------------------------------------------------------
* 文字色自動変更 (シンタックスハイライト)
  正しいコマンドを入力すると、文字に自動で色が付きます。
  打ち間違いのチェックに便利です。

* テーマ切り替え
  [ L ] ボタンを押すとライトモード（白背景）、
  [ D ] ボタンを押すとダークモード（黒背景）に切り替わります。

* 多言語対応
  日本語と English のサンプルコードを切り替えることができます。

----------------------------------------------------------------------
🛠️ コマンド一覧（リファレンス）
----------------------------------------------------------------------
コマンドの後ろには必ず 【半角スペース】 を空けてから数や文字を入力してください。

◆ 1. 基本・演出コマンド
・表示 [メッセージや変数]  /  print
  ログ画面に文字を表示します。
  (例) 表示 冒険が始まった！

・アニメ [メッセージ]  /  type
  タイピングしているかのように、1文字ずつアニメーションしながら文字を表示します。

・待つ [秒数]  /  wait
  指定した秒数だけプログラムを一時停止します（小数も使えます）。
  (例) 待つ 1.5

・カウントダウン [秒数]  /  countdown
  指定した秒数から 「■ 3...」 「■ 2...」 とログ画面でカウントダウンを行います。

・消去  /  clear
  ログ画面をきれいにリセットします。

◆ 2. ステータス・ゲーム操作コマンド
・計算 [変数名] = [式]  /  calc
  変数（データを引き出しに保管する機能）を作ったり、計算をしたりします。
  (例) 計算 得点 = 100
  (例) 計算 得点 = 得点 + 50

・HP [0〜100の数値]  /  hp
  画面上部にある「HPバー」の残量を変更します。
  (例) HP 80

・得点 [数値や変数]  /  score
  画面上部にある「SCORE」の表示をリアルタイムに書き換えます。
  (例) 得点 得点（変数の中身を表示）

・ランダム [変数名] [最小値] [最大値]  /  random
  指定した範囲のランダムな数字をサイコロのように生成し、変数に保存します。
  (例) ランダム ダメージ 10 30

・アイテム [アイテム名]  /  item
  カバンにアイテムを追加し、現在の全所持品をログに表示します。
  (例) アイテム 薬草

・名前入力 [変数名]  /  input_name
  ポップアップを開き、プレイヤーに名前を入力させます。
  入力された名前は変数に保存されます。
  (例) 名前入力 プレイヤー名

◆ 3. AI・会話演出コマンド
・AI [メッセージ]  /  ai
  ナビゲーターAIに話しかけます。言葉（「こんにちは」「疲れた」など）に
  応じてAIが自動で返答してくれます。

・チャット [名前] [メッセージ]  /  chat
  「[名前]: メッセージ」の形で、ゲームの会話イベントのようなログを表示します。
  (例) チャット 魔王 よくぞここまで来た。

◆ 4. 条件分岐（もし〜なら）
・もし [条件]  〜  それとも [条件]  〜  その他  〜  終わり
・if  〜  elif  〜  else  〜  endif
  数値や変数の大きさを比べて、実行する中身を変化させます。
  (使える記号: ==, !=, >, <, >=, <=)
  (例)
  もし 得点 >= 50
    表示 合格！
  その他
    表示 不合格...
  終わり

◆ 5. システム・サウンドコマンド
・効果音 [1か2]  /  se
  システム警告音などの効果音をピピッと言わせます（1と2で音が変わります）。

・音  /  beep
  パソコンの標準ビープ音を鳴らします。

・警告 [メッセージ]  /  alert
  警告ポップアップウィンドウを出して、メッセージを表示します。

・バイブ [回数]  /  vibe
  ログ画面を赤くチカチカと震わせ、ダメージ演出などを行います。

・アプリ終了  /  close
  コードエディタのウィンドウを閉じます。

----------------------------------------------------------------------
🎮 おすすめサンプルコード
----------------------------------------------------------------------
エディタに貼り付けて「▶ 実行する」を押してみてください。

名前入力 ユーザー
チャット ナビゲーター ようこそ、 ユーザー さん！

計算 得点 = 0
表示 --- 運試しゲーム ---
ランダム サイコロ 1 6

もし サイコロ >= 4
  表示 大成功！
  アイテム 伝説の盾
  計算 得点 = 100
その他
  表示 失敗...
  HP 50
  バイブ 3
終わり

得点 得点
AI アイテム
======================================================================
MIT License

Copyright (c) 2026

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
