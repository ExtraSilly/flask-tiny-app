@echo off
echo 🚀 Bắt đầu cài đặt Django Project...

REM Kiểm tra Python
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo ❌ Python chưa được cài đặt! Đang tiến hành tải...
    powershell -Command "& {Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.11.0.rc/python-3.11.0.rc-amd64.exe' -OutFile 'python_installer.exe'}"
    echo 🔧 Cài đặt Python...
    start /wait python_installer.exe /quiet InstallAllUsers=1 PrependPath=1
    del python_installer.exe
)

REM Kiểm tra pip
where pip >nul 2>nul
if %errorlevel% neq 0 (
    echo ❌ pip chưa được cài đặt! Cài đặt ngay...
    python -m ensurepip --default-pip
)

REM Cài đặt Django và Pillow
echo 📦 Cài đặt Django và Pillow...
pip install django pillow

REM Tạo Virtual Environment
if not exist venv (
    echo 🔧 Tạo môi trường ảo (venv)...
    python -m venv venv
)

REM Kích hoạt Virtual Environment
echo ✅ Kích hoạt môi trường ảo...
call venv\Scripts\activate.bat

REM Cài đặt dependencies
if exist requirements.txt (
    echo 📥 Cài đặt các package trong requirements.txt...
    pip install -r requirements.txt
) else (
    echo ⚠️ Không tìm thấy requirements.txt. Sử dụng cài đặt mặc định.
    pip install django pillow
)

REM Chạy migrations
echo 📂 Chạy migrations...
python manage.py migrate

REM Hỏi người dùng có muốn tạo superuser không
set /p create_superuser="🛡️ Bạn có muốn tạo superuser ngay bây giờ không? (y/n): "
if /I "%create_superuser%"=="y" (
    python manage.py createsuperuser
)

REM Chạy server
echo 🚀 Chạy server Django...
python manage.py runserver

echo 🎉 Cài đặt hoàn tất! Truy cập http://127.0.0.1:8000/
