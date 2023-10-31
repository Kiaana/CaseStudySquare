from flask_migrate import upgrade, migrate, init, stamp
from . import app

def db_migrate():
    with app.app_context():
        # 初始化迁移环境（如果尚未初始化）
        if not os.path.exists('./migrations'):
            init()
            # 将数据库标记为最新版本，避免初次迁移时出现问题
            stamp()
            
        # 创建迁移脚本
        migrate()
        # 更新数据库
        upgrade()
