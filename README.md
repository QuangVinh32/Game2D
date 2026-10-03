# 🎮 Game Center - Hand Gesture Controlled Games

## 🌟 Giới thiệu dự án
**Game Center** là một cổng game mini (mini-game hub) được phát triển bằng Python, tập hợp 5 tựa game kinh điển và quen thuộc bao gồm: Flappy Bird, Đào Vàng, CatRun, Geometry Dash và Chrome Dinosaur. 

Điểm nổi bật nhất của dự án này là sự kết hợp với công nghệ **Computer Vision (Thị giác máy tính)**, cho phép người chơi không chỉ điều khiển game bằng bàn phím/chuột thông thường mà còn có thể **điều khiển hoàn toàn bằng cử chỉ bàn tay thông qua Webcam**.

---

## ✨ Các chức năng chính
1. **Menu Tổng hợp (Game Hub):** Giao diện trực quan cho phép người dùng dễ dàng chọn và chuyển đổi giữa 5 trò chơi khác nhau.
2. **Đa dạng trò chơi:**
   - 🐦 **Flappy Bird:** Điều khiển chú chim vượt qua các ống nước.
   - ⛏️ **Đào Vàng (Dao Vang):** Kéo vàng và kim cương để đạt điểm cao.
   - 🐱 **CatRun:** Trò chơi chạy bộ vượt chướng ngại vật.
   - 🟩 **Geometry Dash:** Khối vuông nhảy qua các chông gai.
   - 🦖 **Dino:** Khủng long vượt xương rồng kinh điển.
3. **Chế độ điều khiển bằng cử chỉ tay (Hand Tracking):** Tích hợp trí tuệ nhân tạo để nhận diện khung xương bàn tay theo thời gian thực (Real-time), ánh xạ cử chỉ thành các phím bấm và thao tác chuột để chơi game.
4. **Xử lý đa luồng (Multiprocessing):** Hệ thống camera nhận diện bàn tay và hệ thống game chạy song song trên các luồng khác nhau, giúp game không bị giật lag khi xử lý hình ảnh.

---

## 🛠️ Công nghệ sử dụng
- **Ngôn ngữ lập trình:** Python 3.10
- **Game Engine & UI:** `pygame` (Xử lý đồ họa, âm thanh và vòng lặp game)
- **Computer Vision:** `opencv-python` (cv2 - Thu thập hình ảnh từ Webcam)
- **AI / Hand Tracking:** `mediapipe` (Nhận diện chính xác 21 điểm (landmarks) trên bàn tay)
- **Keyboard & Mouse Simulator:** `pydirectinput` (Giả lập các thao tác bấm phím và click chuột từ tín hiệu bàn tay)
- **Xử lý song song:** Thư viện `multiprocessing` tích hợp sẵn của Python.

---

## 🎮 Hướng dẫn sử dụng & Điều khiển

### 1. Bật/Tắt chế độ Camera (Tại menu chính)
- Phím **`V`**: Bật camera và khởi động chế độ điều khiển bằng bàn tay.
- Phím **`K`**: Tắt chế độ camera.

### 2. Cử chỉ bàn tay (Hand Gestures)
Khi Camera bật, hệ thống sẽ theo dõi các ngón tay của bạn để thực hiện lệnh:
- 🖱️ **Di chuyển chuột:** Di chuyển cả bàn tay qua lại trước camera. Tâm di chuyển được tính bằng gốc ngón giữa.
- 🤏 **Click và giữ chuột (Mouse Down):** Nắm chặt bàn tay (gập tất cả các ngón). Rất hữu ích khi chơi **Đào Vàng** để thả ngàm. Khi duỗi tay ra sẽ là nhả chuột.
- ⬅️ **Phím Mũi tên Trái (Left):** Chỉ duỗi thẳng **ngón trỏ** (các ngón khác gập lại).
- ⬆️ **Phím Space (Nhảy):** Chỉ duỗi thẳng **ngón giữa** (các ngón khác gập lại). Dùng để nhảy trong **Flappy Bird**, **Dino** hoặc **Geometry Dash**.
- ➡️ **Phím Mũi tên Phải (Right):** Chỉ duỗi thẳng **ngón út** (các ngón khác gập lại).

---

## 🚀 Setup & Hướng dẫn khởi chạy

Dự án đã được cấu hình sẵn môi trường ảo (`.venv`) chứa toàn bộ các thư viện cần thiết. Bạn không cần phải tốn công cài đặt dependencies nữa.

### Bước 1: Kích hoạt môi trường ảo
Mở Terminal (Command Prompt hoặc PowerShell) tại thư mục gốc của dự án `c:\Game` và chạy lệnh sau để kích hoạt:

**Trên Windows (PowerShell/CMD):**
```powershell
.\.venv\Scripts\activate
```
*(Bạn sẽ thấy tiền tố `(.venv)` xuất hiện ở đầu dòng lệnh, báo hiệu môi trường đã được bật).*

### Bước 2: Chạy dự án
Sau khi đã kích hoạt môi trường ảo, bạn chỉ cần gõ lệnh:
```powershell
python main.py
```

Cửa sổ Menu Game Center sẽ hiện lên. Bạn có thể dùng chuột click để chọn game trải nghiệm bình thường, hoặc bấm phím `V` để bật camera và bắt đầu "múa tay" để chơi!
