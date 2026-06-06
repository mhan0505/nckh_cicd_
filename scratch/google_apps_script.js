/**
 * GOOGLE APPS SCRIPT - TỰ ĐỘNG KÍCH HOẠT GITHUB ACTIONS KHI CÓ KHẢO SÁT MỚI
 * 
 * HƯỚNG DẪN CẤU HÌNH CHI TIẾT:
 * 
 * BƯỚC 1: TẠO GITHUB PERSONAL ACCESS TOKEN (PAT)
 * 1. Đăng nhập GitHub, click ảnh đại diện -> Settings.
 * 2. Cột bên trái, chọn Developer settings -> Personal access tokens -> Tokens (classic).
 * 3. Chọn Generate new token (classic).
 * 4. Điền mô tả (ví dụ: Google Sheets Survey Webhook).
 * 5. Phần Scopes: Chọn tick vào ô **repo** (và quyền con `repo:status`, `repo_deployment`, `public_repo`) 
 *    hoặc ít nhất tích chọn quyền **actions** (write) và **contents** (write) nếu dùng Fine-grained tokens.
 * 6. Cuộn xuống bấm Generate token. Copy chuỗi token hiển thị (dạng `ghp_xxxx...`) và lưu lại.
 * 
 * BƯỚC 2: CÀI ĐẶT TRÊN GOOGLE SHEETS
 * 1. Mở Google Sheet chứa phản hồi.
 * 2. Tiện ích mở rộng (Extensions) -> Apps Script.
 * 3. Dán đè toàn bộ code dưới đây vào. Thay đổi các biến cấu hình (GITHUB_OWNER, GITHUB_REPO, GITHUB_PAT).
 * 4. Bấm Save (Ctrl + S).
 * 
 * BƯỚC 3: CẤU HÌNH TRIGGER TỰ ĐỘNG
 * 1. Click biểu tượng Trình kích hoạt (hình đồng hồ ở cột bên trái).
 * 2. Click "Thêm trình kích hoạt" (Add Trigger) ở góc dưới bên phải.
 * 3. Chọn hàm chạy: triggerGitHubAction
 *    - Nguồn sự kiện: Từ bảng tính (From spreadsheet)
 *    - Loại sự kiện: Khi gửi biểu mẫu (On form submit)
 * 4. Bấm Lưu và cấp quyền truy cập internet cho script.
 */

// ==========================================
// CẤU HÌNH THÔNG TIN GITHUB CỦA BẠN
// ==========================================
var GITHUB_OWNER = "mhan0505"; // Tên tài khoản GitHub của bạn
var GITHUB_REPO = "nckh_cicd_";    // Tên kho lưu trữ (Repository) của bạn
var GITHUB_PAT = "YOUR_GITHUB_PERSONAL_ACCESS_TOKEN_HERE"; // Thay thế bằng Token ghp_xxx bạn vừa tạo ở Bước 1

/**
 * Hàm gửi request kích hoạt GitHub Actions workflow
 */
function triggerGitHubAction(e) {
  var url = "https://api.github.com/repos/" + GITHUB_OWNER + "/" + GITHUB_REPO + "/dispatches";
  
  var payload = {
    "event_type": "survey_submitted" // Khớp với cấu hình trong run_pipeline.yml
  };
  
  var headers = {
    "Accept": "application/vnd.github+json",
    "Authorization": "Bearer " + GITHUB_PAT,
    "X-GitHub-Api-Version": "2022-11-28",
    "User-Agent": "Google-Apps-Script-Survey-Trigger"
  };
  
  var options = {
    "method": "post",
    "headers": headers,
    "contentType": "application/json",
    "payload": JSON.stringify(payload),
    "muteHttpExceptions": true
  };
  
  try {
    Logger.log("Đang gửi yêu cầu kích hoạt tới GitHub: " + url);
    var response = UrlFetchApp.fetch(url, options);
    var responseText = response.getContentText();
    var responseCode = response.getResponseCode();
    
    Logger.log("Mã phản hồi từ GitHub API: " + responseCode);
    Logger.log("Nội dung: " + responseText);
    
    if (responseCode === 204) {
      Logger.log("Kích hoạt GitHub Actions thành công! (Mã 204 No Content là phản hồi thành công chuẩn của GitHub)");
    } else {
      Logger.log("Lỗi: Server GitHub trả về mã " + responseCode + " - " + responseText);
    }
  } catch (error) {
    Logger.log("Lỗi kết nối mạng: " + error.toString());
  }
}

/**
 * Tạo Menu tùy chỉnh trên Google Sheets để bạn có thể chạy đồng bộ thủ công bất kỳ lúc nào
 */
function onOpen() {
  var ui = SpreadsheetApp.getUi();
  ui.createMenu('📊 GitHub Actions')
      .addItem('🔄 Kích hoạt chạy phân tích (Actions)', 'runManualSync')
      .addToUi();
}

/**
 * Hàm chạy khi chọn Menu thủ công
 */
function runManualSync() {
  var ui = SpreadsheetApp.getUi();
  
  if (GITHUB_PAT === "YOUR_GITHUB_PERSONAL_ACCESS_TOKEN_HERE") {
    ui.alert('⚠️ Cảnh báo', 'Vui lòng mở Apps Script cấu hình GITHUB_PAT của bạn trước khi chạy đồng bộ!', ui.ButtonSet.OK);
    return;
  }
  
  ui.alert('🔄 Gửi tín hiệu', 'Đang gửi tín hiệu kích hoạt GitHub Actions. Vui lòng đợi...', ui.ButtonSet.OK);
  
  // Gọi hàm kích hoạt
  triggerGitHubAction();
  
  ui.alert('🎉 Hoàn tất', 'Yêu cầu kích hoạt đã được gửi! Quá trình phân tích trên GitHub Actions sẽ diễn ra trong khoảng 1-2 phút. Bạn có thể kiểm tra tab Actions trên repository GitHub của mình.', ui.ButtonSet.OK);
}
