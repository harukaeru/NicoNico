# Nico.py

ニコニコ動画の動画を落としてmp3に変換するやつです。
自分用に適当につくったので雑極まりない上ぐちゃぐちゃです。

## 必須環境
- Python (プログラミング言語のひとつ)
- ffmpeg (動画変換するやつ)
- pyquery (jQueryみたいなものをpythonでかけるやつ)
- httplib2 (楽にHttpRequestかけるやつ)


## 推奨環境（なくても別に動かせるが、コードを読んだり変更しないとできなさそうなこと)
- Mac OS X (りんごマーク)
- Python 3.x系 (2.xでも動くかもしれないけど試してない)


## 使い方

Mac OS X を前提としています。
それ以外は各自自分のPC環境に応じて脳内補完してください。

### Homebrewのインストール
ggrks

### ffmpegのインストール
```コマンド
$ brew install ffmpeg
```

### pipのインストール
pipとはなんや？→Pythonで使うライブラリを、コマンド一発でインストールできるツール
インストールはggrks

### pyqueryとかのインストール
```コマンド
$ pip install httplib2
$ pip install pyquery
```

### 必須環境構築がおわったあとは
nico.pyを開いて、ニコニコ動画のメールアドレスやパスワードを書いておく
その後
```コマンド
$ python nico.py sm444444
```
などと打つ

→わーいだどん！

### ライセンス
MIT

### 注意点
- ffmpegはMITではなく、商用利用にはお金がかかります。
- ニコニコの仕様が変わったら動かなくなります
- 悪用しないでください

### 書いてある通りにやってもできないんだけど
その通り。このアプリケーションは使えません。
