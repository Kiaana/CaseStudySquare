import os
import zipfile
import requests
import base64
from flask import Flask, request, jsonify, render_template, stream_with_context, current_app
from flask_sqlalchemy import SQLAlchemy
import time
import urllib.parse
# import concurrent.futures


GITHUB_TOKEN = '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'
GITHUB_REPO = 'Kiaana/CaseStudySquare'
GITEE_TOKEN = 'd051e3ce8278b926b909543a6721d28d'
GITEE_REPO = 'kiaana/case-square'
BINDER_URL_GITHUB = "https://mybinder.org/v2/gh/{repo}/HEAD?filepath={path}"
# BINDER_URL_GITEE = "https://mybinder.org/v2/git/{urllib.parse.quote('https://gitee.com/' + repo, safe='')}/HEAD?labpath={urllib.parse.quote(path)}"
GITHUB_OR_GITEE = 'gitee'



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'

db = SQLAlchemy(app)

# 数据库模型
class Assignment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_name = db.Column(db.String(50), nullable=False)
    assignment_number = db.Column(db.String(50), nullable=False)
    score = db.Column(db.Integer, nullable=True)
    folder_path = db.Column(db.String(255), nullable=True)

@app.route('/admin')
def index():
    return render_template('admin.html')

# 上传 ZIP 文件
@app.route('/upload_assignment', methods=['POST'])
def upload_zip():
    # 获取学生名字和作业次数
    student_name = request.form.get('student_name')
    assignment_number = request.form.get('assignment_number')
    folder_path = os.path.join(assignment_number, student_name)

    if not student_name or not assignment_number:
        return jsonify({"error": "缺少必要的参数"}), 400

    # 检查是否有文件上传
    if 'file' not in request.files:
        return jsonify({"error": "未上传文件"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "未上传文件"}), 400

    # 创建目录结构： 第几次/名字/文件
    save_directory = os.path.join("uploads", assignment_number, student_name)
    os.makedirs(save_directory, exist_ok=True)
    save_path = os.path.join(save_directory, file.filename)
    
    # 保存 ZIP 文件
    with open(save_path, 'wb') as f:
        # 使用 stream_with_context 读取并保存文件
        stream = stream_with_context(file.stream)
        for chunk in stream:
            f.write(chunk)

    # 解压 ZIP 文件
    extract_directory = os.path.join("extracted_files", assignment_number, student_name)
    os.makedirs(extract_directory, exist_ok=True)
    with zipfile.ZipFile(save_path, 'r') as zip_ref:
        for file_info in zip_ref.infolist():
            # 获取原始文件名
            original_filename = file_info.filename
            # 解压缩文件，但保留原始文件名
            zip_ref.extract(file_info, extract_directory)
            # 将文件名从CP437编码转换为UTF-8编码（解决中文乱码问题）
            extracted_path = os.path.join(extract_directory, original_filename.encode('cp437').decode('utf-8', 'ignore'))
            # 重命名文件
            os.rename(os.path.join(extract_directory, original_filename), extracted_path)

    upload_paths = []
    filenames = []
    contents = []
    # 将文件上传到 GitHub
    for root, _, files in os.walk(extract_directory):
        for filename in files:
            file_path = os.path.join(root, filename)
            relative_path = os.path.relpath(file_path, extract_directory)
            upload_path = os.path.join(assignment_number, student_name, relative_path)
            # 跳过隐藏文件
            if filename.startswith('.'):
                continue
            # 打开和读取文件
            with open(file_path, 'rb') as f:
                content = f.read()
            
            upload_paths.append(upload_path)
            filenames.append(filename)
            contents.append(content)
            
    # 上传单个文件到 GitHub 的函数
    def upload_single(params, app):
        upload_path, filename, content = params
        
        # 创建一个应用上下文
        with app.app_context():
            if GITHUB_OR_GITEE == 'github':
                response = upload_to_github(upload_path, filename, content, GITHUB_REPO, GITHUB_TOKEN)
            elif GITHUB_OR_GITEE == 'gitee':
                response = upload_to_gitee(upload_path, filename, content, GITEE_REPO, GITEE_TOKEN)
        return response
    
    # # 创建一个线程池并并发上传文件
    # with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
    #     # 使用线程池上传文件，并获取结果
    #     results = list(executor.map(upload_single, zip(upload_paths, filenames, contents), [app]*len(upload_paths)))
    
    for params in zip(upload_paths, filenames, contents):
        response = upload_single(params, app)
        time.sleep(0.3)
        if response[1] not in [200, 201]:
            return jsonify({"error": "Error uploading or updating file on GitHub"}), 500
                
    # 存储信息到数据库
    assignment = Assignment.query.filter_by(student_name=student_name, assignment_number=assignment_number).first()
    if assignment:
        assignment.folder_path = folder_path
    else:
        new_assignment = Assignment(student_name=student_name, assignment_number=assignment_number, folder_path=folder_path)
        db.session.add(new_assignment)
    db.session.commit()
    
    # 删除上传的 ZIP 文件和解压后的文件
    os.system("rm -rf extracted_files")
    os.system("rm -rf uploads")

    return jsonify({"message": "File uploaded and processed successfully"}), 200

# 将文件上传到 GitHub
def upload_to_github(upload_path, filename, content, GITHUB_REPO, GITHUB_TOKEN):
    url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{upload_path}"
    headers = {
        'Authorization': f'token {GITHUB_TOKEN}',
        'Content-Type': 'application/json'
    }
    
    # 发送 GET 请求检查文件是否存在
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        # 文件存在，获取文件的 sha 值
        file_data = response.json()
        sha = file_data.get('sha')
        # 删除文件
        data = {
            "message": f"Delete {filename}",
            "sha": sha
        }
        response = requests.delete(url, headers=headers, json=data)
        if response.status_code != 200:
            return jsonify({"error": "Error deleting file on GitHub"}), 500
        
        # 发送 PUT 请求来创建文件
        data = {
            "message": f"Add {filename}",
            "content": base64.b64encode(content).decode('utf-8')  # 将内容转换为Base64编码的字符串
        }
        response = requests.put(url, headers=headers, json=data)
        
    elif response.status_code == 404:
        # 文件不存在，需要创建文件的数据
        data = {
            "message": f"Add {filename}",
            "content": base64.b64encode(content).decode('utf-8')  # 将内容转换为Base64编码的字符串
        }
        # 发送 PUT 请求来创建文件
        response = requests.put(url, headers=headers, json=data)
        
    else:
        return jsonify({"error": "Error checking file existence on GitHub"}), 500

    if response.status_code in [200, 201]:
        return jsonify({"message": "File uploaded and processed successfully"}), 200
    else:
        return jsonify({"error": "Error uploading or updating file on GitHub"}), 500

# 将文件上传到 Gitee
def upload_to_gitee(upload_path, filename, content, GITEE_REPO, GITEE_TOKEN):
    url = f"https://gitee.com/api/v5/repos/{GITEE_REPO}/contents/{upload_path}"
    headers = {
        'access_token': GITEE_TOKEN
    }

    # 发送 GET 请求检查文件是否存在
    response = requests.get(url, params=headers)
    if response.status_code == 200:
        file_data = response.json()
        # 检查响应体是否为空
        if len(file_data) == 0:
            # 文件不存在，创建文件
            data = {
                'access_token': GITEE_TOKEN,
                "message": f"Add {filename}",
                "content": base64.b64encode(content).decode('utf-8')  # 将内容转换为Base64编码的字符串
            }
            response = requests.post(url, json=data)
            if response.status_code not in [200, 201]:
                return jsonify({"error": "Error creating file on Gitee"}), 500
        else:
            # 文件存在，更新文件
            sha = file_data.get('sha')
            data = {
                'access_token': GITEE_TOKEN,
                "message": f"Update {filename}",
                "content": base64.b64encode(content).decode('utf-8'),  # 将内容转换为Base64编码的字符串
                "sha": sha
            }
            response = requests.put(url, json=data)
            if response.status_code not in [200, 201]:
                return jsonify({"error": "Error updating file on Gitee"}), 500
    else:
        # 处理其他错误
        return jsonify({"error": "Error accessing Gitee API"}), 500

    return jsonify({"message": "File uploaded and processed successfully"}), 200

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
            repo_url = urllib.parse.quote(f'https://gitee.com/{GITEE_REPO}', safe='')
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

# 从GitHub删除文件夹
def delete_folder_from_github(folder_path):
    # 设置GitHub API的URL和headers
    url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{folder_path}"
    headers = {
        'Authorization': f'token {GITHUB_TOKEN}',
        'Content-Type': 'application/json'
    }

    # 获取文件夹中所有文件的信息
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return False

    # 遍历文件夹中的所有文件，并逐个删除
    files = response.json()
    for file in files:
        if file['type'] == 'file':
            delete_url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{file['path']}"
            data = {
                "message": f"Delete {file['name']}",
                "sha": file['sha']
            }
            response = requests.delete(delete_url, headers=headers, json=data)
            if response.status_code != 200:
                return False
        elif file['type'] == 'dir':
            if not delete_folder_from_github(file['path']):
                return False
    
    # 删除文件夹
    data = {
        "message": f"Delete {folder_path}"
    }
    response = requests.delete(url, headers=headers, json=data)

    return True

# 从Gitee删除文件夹
def delete_folder_from_gitee(folder_path):
    url = f"https://gitee.com/api/v5/repos/{GITEE_REPO}/contents/{folder_path}"
    
    # 获取文件夹中所有文件的信息
    response = requests.get(url, data={'access_token': f'{GITEE_TOKEN}'})
    if response.status_code != 200:
        return False
    
    # 遍历文件夹中的所有文件，并逐个删除
    files = response.json()
    for file in files:
        if file['type'] == 'file':
            delete_url = f"https://gitee.com/api/v5/repos/{GITEE_REPO}/contents/{file['path']}"
            data = {
                "access_token": f"{GITEE_TOKEN}",
                "message": f"Delete {file['name']}",
                "sha": file['sha']
            }
            response = requests.delete(delete_url, json=data)
            if response.status_code != 200:
                return False
        elif file['type'] == 'dir':
            if not delete_folder_from_gitee(file['path']):
                return False
        
    # 删除文件夹
    data = {
        "access_token": f"{GITEE_TOKEN}",
        "message": f"Delete {folder_path}"
    }
    response = requests.delete(url, json=data)
    return True
    
# 作业列表页面
@app.route('/')
def homework_list():
    return render_template('index.html')

# 清除数据库
@app.route('/clear_db')
def clear_db():
    db.drop_all()
    db.create_all()
    return jsonify({"message": "Database cleared successfully"}), 200

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(port=1753)
