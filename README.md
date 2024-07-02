# PDF翻訳

このツールは、PDF形式の英語文書を日本語に翻訳するツールです。英語のテキストを自動的に抽出し、翻訳を行い、翻訳されたテキストをPDFとして保存します。
できるだけレイアウトを保ったまま翻訳をするようになっています。

こちらの記事を参考にローカルのDocker環境で動くようにしています。
- 参考: [Google Colabで英語の論文を無料で翻訳する方法](https://qiita.com/sakasegawa/items/f50aae7f3acf475411aa)


## 必要な環境

- Docker
- Docker Compose

## セットアップ手順

1. リポジトリをクローンします。

    ```bash
    git clone https://github.com/Shuyawa89/pdf-translation.git
    cd pdf-translation
    ```

2. 必要なDockerイメージをビルドします。

    初回起動時は結構時間がかかるので、気長に放置してください。

    ```bash
    docker compose build
    ```

3. モデルファイル `model_final.pth` をダウンロードし、プロジェクトのルートディレクトリに配置します。

    このファイルは文字や図などの枠を検出するのに利用しています。

    ```bash
    wget -O model_final.pth "https://www.dropbox.com/s/57zjbwv6gh3srry/model_final.pth?dl=1"
    ```

4. 翻訳を行いたいPDFファイルをプロジェクトのルートディレクトリに配置します。例えば、`Improvement of CT Reconstruction Using Scattered X-Rays.pdf` という名前のファイルを配置します。

5. `main.py` の中で、翻訳を行うPDFファイルのパスを指定します。以下のように設定してください。

    ```python
    target_pdf_file_path = r"./Improvement of CT Reconstruction Using Scattered X-Rays.pdf"
    ```

6. Dockerコンテナを起動します。以下のコマンドを実行してください。

    ```bash
    docker compose up
    ```

7. コンテナが起動し、翻訳が完了すると、翻訳済みのPDFファイルが `translated_Improvement of CT Reconstruction Using Scattered X-Rays.pdf` という名前でプロジェクトのルートディレクトリに保存されます。


２回目以降は、Dockerコンテナをbuildする必要はなく、`docker compose up` で翻訳が始まります。
## ファイル構成

- `Dockerfile`: Dockerイメージをビルドするための設定ファイル。
- `docker-compose.yml`: Dockerコンテナの設定ファイル。
- `requirements.txt`: プロジェクトで使用するPythonパッケージのリスト。
- `main.py`: 翻訳処理のメインスクリプト。
- `pdf_processing.py`: PDF処理に関する関数を含むモジュール。
- `translation.py`: 翻訳に関する関数を含むモジュール。

## 注意点

- 翻訳モデルには `Helsinki-NLP/opus-mt-en-ja` を使用しています。他のモデルを使用する場合は、`translation.py` 内の設定を変更してください。
  - 参考 : https://huggingface.co/models?pipeline_tag=translation&sort=downloads&search=en-ja
- 大量のPDFファイルを処理する場合、翻訳時間がかかることがあります。必要に応じて、Dockerコンテナのリソース制限を調整してください。

