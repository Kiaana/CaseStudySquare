import os

class Config:
    GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN') or 'your_github_token'
    GITHUB_REPO = os.environ.get('GITHUB_REPO') or 'your_github_repo'
    GITEE_TOKEN = os.environ.get('GITEE_TOKEN') or 'your_gitee_token'
    GITEE_REPO = os.environ.get('GITEE_REPO') or 'your_gitee_repo'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///students.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    GITHUB_OR_GITEE = os.environ.get('GITHUB_OR_GITEE') or 'gitee'
    PORT = os.environ.get('PORT') or 1753

class DevelopmentConfig(Config):
    DEBUG = True
    # 开发环境特有的配置

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    # 测试环境特有的配置

class ProductionConfig(Config):
    DEBUG = False
    # 生产环境特有的配置
