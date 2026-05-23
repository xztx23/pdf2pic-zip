import fitz
import zipfile
import os
import sys

# ===================== 自动读取传入参数 =====================
if len(sys.argv) < 2:
    print("用法：python3 convert.py 任务ID")
    sys.exit(1)

task_id = sys.argv[1]
pdf_path = f"input_{task_id}.pdf"
output_dir = f"images_{task_id}"
zip_name = f"result_{task_id}.zip"

# ===================== 创建输出目录 =====================
os.makedirs(output_dir, exist_ok=True)

# ===================== 打开 PDF 并逐页转图片 =====================
print(f"[INFO] 开始处理 PDF：{pdf_path}")
doc = fitz.open(pdf_path)

for page_index in range(len(doc)):
    page = doc[page_index]
    pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))  # 高清 2 倍图
    img_num = page_index + 1
    img_path = os.path.join(output_dir, f"{img_num}.png")
    pix.save(img_path)
    print(f"→ 已生成：{img_num}.png")

print(f"[INFO] PDF 总页数：{len(doc)}")

# ===================== 打包所有图片为 ZIP =====================
with zipfile.ZipFile(zip_name, "w", zipfile.ZIP_DEFLATED) as zf:
    for img_file in sorted(os.listdir(output_dir)):
        img_full_path = os.path.join(output_dir, img_file)
        zf.write(img_full_path, img_file)

print(f"[SUCCESS] ZIP 打包完成：{zip_name}")
