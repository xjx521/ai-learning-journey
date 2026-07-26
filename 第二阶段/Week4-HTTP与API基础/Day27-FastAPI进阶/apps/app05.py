from fastapi import APIRouter, File, UploadFile
from typing import List
import os

app05 = APIRouter()


@app05.post("/file")
async def get_file(file: bytes = File()):  # 文件就是字节流
    # 适合小文件上传
    print("file:", file)
    return {"file": len(file)}


@app05.post("/files")
async def get_files(files: List[UploadFile] = File(...)):  # 传多个文件List[bytes]
    # 适合小文件上传
    # print("files:", files)
    for file in files:
        print(len(file))
    return {"files": len(files)}


@app05.post("/uploadFile")
async def get_file(file: UploadFile):  # 文件就是字节流
    print("file:", file)
    path = os.path.join("imgs", file.filename)  # 路径拼接
    with open(path, "wb") as f:
        for line in file.file:
            f.write(line)
    return {"file": file.filename}
