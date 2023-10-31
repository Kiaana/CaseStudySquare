from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
import os
from .utils import validate_request, save_and_extract_zip, upload_files, cleanup
from .models import Assignment
from .services import upload_assignment_service

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
db = SQLAlchemy(app)


# 管理员页面
@app.route('/admin')
def index():
    return render_template('admin.html')

# 上传 ZIP 文件
@app.route('/upload_zip', methods=['POST'])
def upload_assignment():
    """
    处理上传的 ZIP 文件，保存和解压文件，上传文件到 GitHub 或 Gitee，并更新数据库。

    :return: 成功响应或错误响应。
    """
    return upload_assignment_service()

# 更新分数
@app.route('/update_score', methods=['POST'])
def update_score():
    data = request.json
    student_name = data.get('student_name')
    assignment_number = data.get('assignment_number')
    new_score = data.get('score')
    
    assignment = Assignment.query.filter_by(student_name=student_name, assignment_number=assignment_number).first()
    if assignment:
        assignment.score = new_score
        db.session.commit()
        return jsonify({"message": "Score updated successfully"}), 200
    else:
        return jsonify({"error": "作业未找到"}), 404

# 列出所有作业
@app.route('/list_assignments', methods=['GET'])
def list_assignments():
    assignments = Assignment.query.order_by(Assignment.score.desc()).all()
    assignment_list = []
    for a in assignments:
        if GITHUB_OR_GITEE == 'github':
            binder_link = BINDER_URL_GITHUB.format(repo=GITHUB_REPO, path=f"{a.folder_path}/")
        elif GITHUB_OR_GITEE == 'gitee':
            repo_url = urllib.parse.quote(f'https://gitee.com/{GITHUB_REPO}', safe='')
            binder_link = f"https://mybinder.org/v2/git/{repo_url}/HEAD?labpath={a.folder_path}"
        assignment_list.append({
            "student_name": a.student_name,
            "assignment_number": a.assignment_number,
            "score": a.score,
            "binder_link": binder_link
        })
    
    return jsonify({"assignments": assignment_list}), 200

# 删除作业
@app.route('/delete_assignment', methods=['DELETE'])
def delete_assignment():
    student_name = request.args.get('student_name')
    assignment_number = request.args.get('assignment_number')

    # 从数据库中删除记录
    assignment = Assignment.query.filter_by(student_name=student_name, assignment_number=assignment_number).first()
    if assignment:
        db.session.delete(assignment)
        db.session.commit()
    else:
        return jsonify({"success": False, "error": "作业在数据库中未找到"})

    # 从GitHub删除文件夹
    folder_path = os.path.join(assignment_number, student_name)
    if GITHUB_OR_GITEE == 'github':
        if not delete_folder_from_github(folder_path):
            return jsonify({"success": False, "error": "从GitHub删除文件夹失败"})
    elif GITHUB_OR_GITEE == 'gitee':
        if not delete_folder_from_gitee(folder_path):
            return jsonify({"success": False, "error": "从Gitee删除文件夹失败"})

    return jsonify({"success": True})

# 主页
@app.route('/')
def homework_list():
    return render_template('index.html')

# 用于清空数据库的路由
@app.route('/clear_db')
def clear_db():
    db.drop_all()
    db.create_all()
    return jsonify({"message": "Database cleared successfully"}), 200
