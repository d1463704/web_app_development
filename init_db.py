from app import create_app, db
from app.models import Account, Category

app = create_app()
with app.app_context():
    # 建立所有資料表
    db.create_all()
    
    # 檢查是否已有預設資料
    if not Account.query.first():
        print("Initializing default accounts...")
        Account.create(name="現金錢包", balance=1000.0)
        Account.create(name="銀行帳戶", balance=50000.0)
    
    if not Category.query.first():
        print("Initializing default categories...")
        # 支出分類
        Category.create(name="餐飲", type="expense")
        Category.create(name="交通", type="expense")
        Category.create(name="娛樂", type="expense")
        Category.create(name="購物", type="expense")
        # 收入分類
        Category.create(name="薪資", type="income")
        Category.create(name="獎金", type="income")
        
    print("Database initialized successfully.")
