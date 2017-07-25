# AWS EC2のイメージバックアップ自動

* AWS EC2のイメージバックアップを自動で取得します。
* 指定した保持期間を過ぎたイメージとスナップショットを削除します。
* 指定したSlackチームに結果を通知します。


## AWS Lambdaで実行します

1. ダウンロードしたコードにrequestsをインストールしてzipにしてLambda関数を作成します。
1. Slackでチームを作成、または既存のSlackでIncoming Webhookを設定します。
1. Slackで #ec2_create_imageチャンネルを作ります。
1. 環境変数を設定します。

### (参考)requestsのインストール

```
$ pip install requests -t .
```


## 環境変数

環境変数名|内容|例
:--|:--|:--
REGION_NAME|リージョン|ap-northeast-1
TARGET_NAME|EC2 Nameタグ|
PURGE_DAYS|イメージの保持日数|7
SLACK_URL|SlackのURL|https://hooks.slack.com/services/~~~
AWS_ACCOUNT_ID|AWSアカウントID|123456789012
