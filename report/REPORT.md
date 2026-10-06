# Báo cáo Lab: Self evolving Agentic

## 1. Thông tin nhóm và cấu hình

| Họ tên | Mã sinh viên | Phần đóng góp |
|---|---|---|
| Lương Khánh Toàn | 2A202602836 | 100% (Cài đặt Harness, thực nghiệm 3 điều kiện, curator, phân tích và báo cáo) |

- Nhà cung cấp và mô hình (`LAB_MODEL`, không ghi khóa API), nhiệt độ (`LAB_TEMPERATURE`), `recursion_limit`: `deepseek/deepseek-flash` (qua endpoint LiteLLM tương thích OpenAI), `LAB_TEMPERATURE=0`, `recursion_limit=60`.
- Phiên bản Deep Agents (`pip show deepagents`), hệ điều hành, chạy trực tiếp hay trong Docker: `deepagents 0.7.21`, Windows 11 (Python 3.11 trong venv cục bộ có tích hợp Git shell).
- Số lần chạy tác vụ đã dùng / ngân sách: 12 lần chạy chính thức (3 baseline learn, 3 subagents learn, 3 skills-auto dev learn, chuẩn bị chạy eval).
- Commit của tag `freeze`: Sẽ được cập nhật sau khi tạo tag `freeze`.

## 2. Giả thuyết (commit TRƯỚC tag `freeze`, Phần 4.0)

- H1 (subagents so với baseline): Đa tác tử (`subagents`) đạt điểm kỹ thuật tương đương hoặc thấp hơn một chút so với `baseline` do hiện tượng cô lập ngữ cảnh (context isolation khiến subagent không thấy toàn bộ lịch sử) và chi phí phối hợp lớn, đồng thời tiêu tốn lượng token gấp 2 đến 3 lần và dễ chạm `recursion_limit` khi đệ quy qua nhiều bước. Căn cứ từ quan sát thực nghiệm tập học và bài báo của Anthropic về multi-agent research systems.
- H2 (skills-auto so với baseline): `skills-auto` đạt điểm cao hơn rõ rệt so với `baseline` trên các tác vụ đánh giá có dùng lại quy ước tổ chức (house rules) đã học (như kiểm tra hồi quy, chú thích kiểu, changelog trong họ `code`), nhưng sẽ không cải thiện được các quy ước mới hoàn toàn chưa từng xuất hiện trong tập học (như các quy tắc riêng của từng tác vụ eval). Căn cứ từ nghiên cứu SkillsBench và SkillEvolBench về khả năng chuyển giao tri thức thủ tục của LLM.
- H3 (tác vụ học so với tác vụ đánh giá): Điểm trung bình của `skills-auto` trên tác vụ học sẽ cao hơn đáng kể so với trên tác vụ đánh giá (hiện tượng quá khớp ở tầng ngữ cảnh - context-layer overfitting), do các skill được tối ưu trực tiếp từ vết lỗi của tác vụ học, trong khi tác vụ đánh giá sở hữu tập dữ liệu mới và quy tắc kiểm thử bổ sung.

## 3. Làm quen Deep Agents (Phần 0.3)

1. Tác tử mặc định có 9 công cụ: công cụ tệp (`ls`, `read_file`, `write_file`, `edit_file`, `delete`, `glob`, `grep`), công cụ shell (`execute`), và công cụ điều phối subagent (`task`). Công cụ duy nhất cho phép chạy lệnh thực thi là `execute`.
2. Mô tả của công cụ `task` cho biết subagent `general-purpose` được dùng để nghiên cứu các câu hỏi phức tạp, tìm kiếm tệp và thực thi tác vụ nhiều bước; subagent này có quyền truy cập toàn bộ công cụ như tác tử chính. Về ngữ cảnh: subagent hoàn toàn không trạng thái (stateless), chỉ nhìn thấy nội dung prompt được tác tử chính truyền sang và trả về một báo cáo cuối cùng, không nhìn thấy lịch sử hội thoại trước đó của tác tử chính trừ khi được chỉ định thừa kế.
3. Trích dẫn hướng dẫn hành vi:
   - Từ mô tả công cụ `task`: *"Put full detail in the prompt and state exactly what it should return — unless an agent type below says it inherits your conversation instead."*
   - Từ mô tả công cụ `execute`: *"You MUST avoid using search commands like find and grep. Instead use the grep, glob tools to search. Use read_file rather than cat/head/tail."*

## 4. Đường cơ sở và phân loại lỗi (Phần 2.2)

| Tác vụ | Check thất bại | Nhóm lỗi (A-G) | Bằng chứng (trích ngắn từ `detail` hoặc vết) |
|---|---|---|---|
| `code-learn` | `tests_not_modified` | A (Bỏ qua đặc tả) | `detail`: "the original files in tests/ must not be modified (new test files are allowed)". Tác tử trong quá trình gỡ lỗi đã vô tình can thiệp vào `tests/test_report.py`. |
| `code-learn` | `rule_type_hints` | E (Vi phạm quy ước tổ chức) | `detail`: "RULE: every public function (name not starting with '_') in the package has type annotations on all parameters and on the return value." Đề bài không hề nhắc quy định này. |
| `code-learn` | `rule_regression_tests` | E (Vi phạm quy ước tổ chức) | `detail`: "RULE: add tests/test_regressions.py with one test function per bug you fixed (at least 3); the file must pass." Quy ước kiểm tra hồi quy nội bộ của Acme. |
| `code-learn` | `rule_changelog` | E (Vi phạm quy ước tổ chức) | `detail`: "RULE: record each fix in CHANGELOG.md under the heading '## Unreleased' as a bullet '- fix(<function name>): <short description>' (at least 3 bullets)." Quy ước nhật ký thay đổi nội bộ Acme. |
| `data-learn` | `rule_money_in_cents` | E (Vi phạm quy ước tổ chức) | `detail`: "RULE: money values in answer.json are integer cents (1606.67 USD is written 160667)." Đề bài yêu cầu revenue nhưng bot yêu cầu dạng cent nguyên. |
| `data-learn` | `rule_meta_block` | E (Vi phạm quy ước tổ chức) | `detail`: "RULE: answer.json has an object `meta` = {\"source\": <input file name>, \"rows_in\": <number of data rows>, \"rows_used\": <number of distinct orders>}." Khối metadata theo quy ước Acme. |
| `data-learn` | `rule_clean_csv` | E (Vi phạm quy ước tổ chức) | `detail`: "RULE: write workspace/clean.csv with the header order_id,timestamp_utc,region,amount_cents...". Yêu cầu xuất thêm file làm sạch mà đề bài không nêu. |

Nhận xét:
- Nhóm lỗi chiếm đa số áp đảo là **Nhóm E (Vi phạm quy ước tổ chức - House Rules)**, chiếm 6/7 lỗi thất bại.
- Bằng chứng phủ định: Tất cả các check kỹ thuật thuần túy (thuật toán tính toán, parse ngày tháng, làm sạch chuỗi, gỡ lỗi logic hàm `parse_price`, `apply_discount`, `low_stock`) tác tử đều đạt điểm tuyệt đối (5/5 check kỹ thuật ở `data-learn`, 6/6 check kỹ thuật ở `code-learn`, 9/9 check ở `logs-learn`). Mô hình có năng lực lập trình và phân tích rất mạnh nhưng không thể biết các quy ước nội bộ vô hình của Acme nếu không có cơ chế phản hồi.
- Một skill thủ tục hoàn toàn có thể phòng ngừa nhóm lỗi E bằng cách cung cấp danh sách checklist các quy ước bắt buộc (tạo CHANGELOG, viết test hồi quy, thêm type hints, xuất khối meta, chuẩn hóa số tiền thành cent).

## 5. Điều kiện `subagents` (Phần 2.3)

- Các subagent đã định nghĩa:
  1. `explorer`: Đọc tài liệu, cấu trúc thư mục, log, mẫu dữ liệu ban đầu, báo cáo sự thật mà không sửa đổi file.
  2. `implementer`: Trực tiếp áp dụng các thay đổi mã nguồn/dữ liệu và chạy test/script kiểm tra qua shell.
  3. `reviewer`: Rà soát độc lập kết quả so với yêu cầu, bắt các ca biên mà không sửa file.
- `subagent_calls` ở từng tác vụ và nhận xét:
  - `data-learn`: `subagent_calls = 1`. Tác tử chính giao việc cho subagent `reviewer` để kiểm chứng độc lập các phép tính doanh thu, số dòng trùng và đơn hàng thiếu. Subagent kiểm tra chéo thành công.
  - `logs-learn`: `subagent_calls = 0`. Tác tử chính tự nhận diện tác vụ phân tích log có tính tuần tự trực tiếp nên tự dùng python script giải quyết trong luồng chính mà không chia nhỏ.
  - `code-learn`: `subagent_calls = 0` (trong luồng chính ghi nhận 0 lượt do chạm `GraphRecursionError` sau 60 bước gọi lặp lại giữa các trạng thái).
- Thông tin giao việc: Trong `data-learn`, tác tử chính truyền đầy đủ đặc tả phép tính và yêu cầu đối chiếu cho reviewer. Tuy nhiên do subagent bị cô lập ngữ cảnh, lượng thông tin cần truyền qua prompt rất dài.
- Ảnh hưởng đến token và thời gian: Chi phí tăng vọt. `data-learn` tốn 849,588 tokens (so với 263,538 tokens của baseline, tăng gấp 3.2 lần) và mất 245.1 giây (so với 50.9 giây của baseline, tăng gần 5 lần). Đa tác tử tạo gánh nặng lớn về chi phí và thời gian trễ trong khi không giúp cải thiện điểm các quy ước ẩn.

## 6. Self-evolving: skill do curator sinh (Phần 3)

- Số lần chạy curator: 1 lần duy nhất (`python -m lab.curator`), sinh thành công 2 skill hợp lệ, không có skill nào bị xóa.

| Skill | Tổng quát hay riêng cho tác vụ học? | Đúng hay sai (nêu chỗ sai nếu có) | Độ dài, `description` và `skills_read` ở Phần 3.4 |
|---|---|---|---|
| `bugfix-package-maintenance` | Rất tổng quát. Đúc kết quy trình sửa lỗi gói Python: không sửa test cũ, thêm test hồi quy vào `tests/test_regressions.py`, thêm type annotations cho hàm public, cập nhật `CHANGELOG.md` dưới `## Unreleased`. | Hoàn toàn đúng, bám sát các tiêu chuẩn kỹ thuật và quy ước nội bộ đã ghi nhận từ feedback của bot. | 12 dòng. `description`: "When fixing defects in a Python package and the task requires type hints, regression tests, and changelog entries." Được đọc trong `code-learn` (`skills_read = 2`). |
| `spec-compliance-verification` | Tổng quát. Đưa ra checklist kiểm tra tính tuân thủ đặc tả: liệt kê quy tắc, kiểm tra schema, xử lý các giá trị đặc biệt, đối chiếu trước khi kết thúc. | Đúng và an toàn, khuyến khích kiểm tra định dạng chính xác. | 11 dòng. `description`: "Before and after any task that has explicit rules, check names, or output schemas." Được đọc trong các tác vụ kiểm thử (`skills_read = 2`). |

## 7. Kết quả so sánh (Phần 4.3, 4.4)

(Sẽ được cập nhật sau khi chạy hoàn tất toàn bộ các tác vụ đánh giá)

## 8. Phân tích

(Sẽ được hoàn thiện dựa trên số liệu bảng tổng hợp)

## 9. Hạn chế và tính hợp lệ

(Sẽ được hoàn thiện)

## 10. Kết luận

(Sẽ được hoàn thiện)

## Phụ lục

- Lệnh đã chạy (theo thứ tự):
- Thử thách mở rộng (nếu có):
- Ghi chú khác:
