# Apacheアクセスログ集計プログラム

## 開発環境  
* python3.6.4

## 使用条件
* python3  
* Apacheのアクセスログファイルは以下のディレクトリにあるものとします。  
    ***/var/log/httpd/***   
    
## 実行方法  
#### 1. プログラムはターミナルを使用し次のように実行します。  
 　`$ python apache_logs_analyzer.py`   

 　期間を指定する場合はコマンドラインオプションを使用し、以下に示す２つの引数を入力してください。 

 　引数１： 期間開始日　形式: *year/month/day*  例） 2017/4/1  
 　引数2： 期間終了日　形式: *year/month/day*  例） 2017/4/30  

 　`$ python apache_logs_analyzer.py 2017/4/1 2017/4/30`  

#### 2. プログラム実行後、/var/log/httpd/内のログファイルが一覧表示されます。  
 　表示されたファイルの中から解析したいログファイルの番号をひとつずつ選択します。  
 　入力を終えたた後、endを入力すると選択が完了します。  

      /var/log/httpd/  
      1. access_log  
      2. access_log2  
      3. error_log  
       アクセスログ(番号)を選択してください (end:入力終了)  
       >> 1  
       >> 2  
       >> end  

#### 3. ログファイルの選択完了後、ログ集計の種類を２種類から選択します。 
 　time : 1時間毎のアクセス件数  
 　host : リモートホスト毎のアクセス件数 

    集計の種類を選択してください　time/host   
    >> time  

#### 4. 総アクセス件数と選択した集計方法に従った件数の一覧が表示されます。  
 　なお、件数の右側には件数に対応した棒グラフが出力されます。（最大値50件分）  
