# 1. Di chuyển vào thư mục dự án đã giải nén
cd dcgf_system

# 2. Khởi tạo và liên kết với repository trên GitHub của bạn
git init
git add .
git commit -m "Update full structure DCGF system"
git branch -M main
git remote add origin https://github.com/ntnguyen983-sketch/dd_engine1.git

# 3. Đẩy code lên GitHub (nếu bị xung đột do repo trên GitHub đã có sẵn README, dùng lệnh push --force)
git push -u origin main --force
