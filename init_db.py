from app import create_app, db
from app.models import Account, Category
import os

app = create_app()

with app.app_context():
    # 確保資料表已建立
    db.create_all()
    
    # 檢查是否已有資料
    if not Category.query.first():
        print("正在初始化預設分類...")
        categories = [
            ('餐飲', 'expense'),
            ('交通', 'expense'),
            ('娛樂', 'expense'),
            ('購物', 'expense'),
            ('薪資', 'income'),
            ('獎金', 'income')
        ]
        for name, type in categories:
            Category.create(name=name, type=type)
            
    if not Account.query.first():
        print("正在初始化預設帳戶...")
        Account.create(name='現金錢包', balance=1000.0)
        Account.create(name='銀行帳戶', balance=5000.0)
        
    print("資料庫初始化完成！")
