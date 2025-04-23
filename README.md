# 顔認証 出勤記録アプリ

アップロードされた顔画像とカメラの映像を比較し本人確認し、出勤時刻を記録するアプリです。  


## 特徴

- 画像アップロードによる顔認証
- 認証成功時に `attendance.csv` に記録

## 起動方法（ローカル）

```bash
pip install -r requirements.txt
known_facesに顔画像をアップロード
python create_known_faces.py 
python app.py