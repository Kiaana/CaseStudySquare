import os
import requests
import base64
from .models import Assignment, db
from flask import jsonify, Response
from .utils import validate_request, save_and_extract_zip, upload_files, cleanup
from .config import Config


def upload_assignment_service():
    """
    处理上传的 ZIP 文件，保存和解压文件，上传文件到 GitHub 或 Gitee，并更新数据库。

    :return: 成功响应或错误响应。
    """
    student_name, assignment_number, file = validate_request()
    folder_path = os.path.join(assignment_number, student_name)
    extract_directory = save_and_extract_zip(file, student_name, assignment_number)
    upload_response = upload_files(extract_directory, student_name, assignment_number)
    if upload_response:
        return upload_response
    update_database_service(student_name, assignment_number, folder_path)
    cleanup()
    return jsonify({"message": "File uploaded and processed successfully"}), 200

def update_database_service(student_name, assignment_number, folder_path):
    """
    更新数据库以存储上传的作业信息。

    :param student_name: 学生的名字。
    :param assignment_number: 作业的次数。
    :param folder_path: 文件夹的路径。
    """
    assignment = Assignment.query.filter_by(student_name=student_name, assignment_number=assignment_number).first()
    if assignment:
        assignment.folder_path = folder_path
    else:
        new_assignment = Assignment(student_name=student_name, assignment_number=assignment_number, folder_path=folder_path)
        db.session.add(new_assignment)
    db.session.commit()
    
def upload_single(params, app):
    upload_path, filename, content = params
    
    # 创建一个应用上下文
    with app.app_context():
        if Config.GITHUB_OR_GITEE == 'github':
            response = upload_to_github(upload_path, filename, content)
        elif Config.GITHUB_OR_GITEE == 'gitee':
            response = upload_to_gitee(upload_path, filename, content)
    return response

def upload_to_github(upload_path, filename, content):
    url = f"https://api.github.com/repos/{Config.GITHUB_REPO}/contents/{upload_path}"
    headers = {
        'Authorization': f'token {Config.GITHUB_TOKEN}',
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

def upload_to_gitee(upload_path, filename, content):
    url = f"http://gitee.com/api/v5/repos/{Config.GITEE_REPO}/contents/{upload_path}"
    headers = {
        'access_token': Config.GITEE_TOKEN
    }

    # 发送 GET 请求检查文件是否存在
    response = requests.get(url, params=headers)
    if response.status_code == 200:
        file_data = response.json()
        # 检查响应体是否为空
        if not file_data:
            # 文件不存在，创建文件
            data = {
                'access_token': Config.GITEE_TOKEN,
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
                'access_token': Config.GITEE_TOKEN,
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
