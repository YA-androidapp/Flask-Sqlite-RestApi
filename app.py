from flask import Flask, render_template, redirect, request, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String


# Flaskの設定
app = Flask(__name__)
# シークレットキーを設定
app.config['SECRET_KEY'] = 'secret key'
# カレントディレクトリのapp.sqliteを使用
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.sqlite'

# DB設定
db = SQLAlchemy(app)

# モデルの定義


class MEMO_TABLE(db.Model):
    __tablename__ = 'memo_table'

    ID = db.Column(Integer, primary_key=True)
    MEMO = db.Column(String(32))
    PRIORITY = db.Column(Integer)


# DBの準備
db.create_all()


# エンドポイントの定義

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        # フォームから送信されたデータをDBに登録
        memo = request.form['memo']
        priority = request.form['priority']
        record = MEMO_TABLE(MEMO=memo, PRIORITY=priority)
        db.session.add(record)
        db.session.commit()
        db.session.close()
        return redirect(url_for('index'))
    elif request.method == 'GET':
        # レコードを一覧表示
        memos = db.session.query(
            MEMO_TABLE.ID, MEMO_TABLE.MEMO, MEMO_TABLE.PRIORITY).all()
        return render_template('index.html', memos=memos)


@app.route('/<int:id>', methods=['GET', 'DELETE'])
def memo(id=None):
    # HTMLのフォームがDELETEに対応していないため、GETで代用
    # if request.method == 'DELETE':
    if request.method == 'GET':
        # 該当するレコードを検索して先頭の1件を取得
        record = db.session.query(
            MEMO_TABLE).filter_by(ID=id).first()
        db.session.delete(record)
        db.session.commit()
        return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()
