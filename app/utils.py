import time
import os
import zipfile
from .services import upload_single
from flask import jsonify, request, stream_with_context
from . import app


# 验证上传请求的参数并检查文件是否上传。
def validate_request():
    """
    验证上传请求的参数并检查文件是否上传。

    :return: 如果验证成功，返回学生名字，作业次数和上传的文件；如果验证失败，返回错误响应。
    """
    student_name = request.form.get('student_name')
    assignment_number = request.form.get('assignment_number')

    # 验证学生名字和作业次数是否提供
    if not student_name or not assignment_number:
        return jsonify({"error": "缺少必要的参数"}), 400

    # 检查文件是否上传
    if 'file' not in request.files or request.files['file'].filename == '':
        return jsonify({"error": "未上传文件"}), 400

    return student_name, assignment_number, request.files['file']

# 保存并解压上传到服务器的 ZIP 文件。
def save_and_extract_zip(file, student_name, assignment_number):
    """
    保存并解压上传到服务器的 ZIP 文件。

    :param file: 上传的文件对象。
    :param student_name: 学生的名字。
    :param assignment_number: 作业的次数。
    :return: 解压文件的目录路径。
    """
    # 创建保存 ZIP 文件的目录
    save_directory = os.path.join("uploads", assignment_number, student_name)
    os.makedirs(save_directory, exist_ok=True)
    save_path = os.path.join(save_directory, file.filename)
    
    # 保存 ZIP 文件
    with open(save_path, 'wb') as f:
        stream = stream_with_context(file.stream)
        for chunk in stream:
            f.write(chunk)
            
    # 解压 ZIP 文件
    extract_directory = os.path.join("extracted_files", assignment_number, student_name)
    os.makedirs(extract_directory, exist_ok=True)
    with zipfile.ZipFile(save_path, 'r') as zip_ref:
        for file_info in zip_ref.infolist():
            original_filename = file_info.filename
            zip_ref.extract(file_info, extract_directory)
            extracted_path = os.path.join(extract_directory, original_filename.encode('cp437').decode('utf-8', 'ignore'))
            os.rename(os.path.join(extract_directory, original_filename), extracted_path)
    
    return extract_directory

# 将解压后的文件上传到 GitHub 或 Gitee。
def upload_files(extract_directory, student_name, assignment_number):
    """
    遍历解压后的文件，并将它们上传到 GitHub 或 Gitee。

    :param extract_directory: 解压文件的目录路径。
    :param student_name: 学生的名字。
    :param assignment_number: 作业的次数。
    :return: 如果上传成功，返回 None；如果上传失败，返回错误响应。
    """
    upload_paths = []
    filenames = []
    contents = []
    for root, _, files in os.walk(extract_directory):
        for filename in files:
            if filename.startswith('.'):
                continue
            file_path = os.path.join(root, filename)
            relative_path = os.path.relpath(file_path, extract_directory)
            upload_path = os.path.join(assignment_number, student_name, relative_path)
            with open(file_path, 'rb') as f:
                content = f.read()
            upload_paths.append(upload_path)
            filenames.append(filename)
            contents.append(content)
    
    for params in zip(upload_paths, filenames, contents):
        response = upload_single(params, app)
        time.sleep(0.3)
        if response[1] not in [200, 201]:
            return jsonify({"error": "Error uploading or updating file on GitHub"}), 500

# 清理临时文件和目录。
def cleanup():
    """
    清理临时文件和目录。
    """
    os.system("rm -rf extracted_files")
    os.system("rm -rf uploads")

