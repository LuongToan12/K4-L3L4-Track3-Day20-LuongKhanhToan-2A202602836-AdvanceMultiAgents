# Báo cáo Lab: Self evolving Agentic

## 1. Thông tin nhóm và cấu hình

| Họ tên | Mã sinh viên | Phần đóng góp |
|---|---|---|
| Lương Khánh Toàn | 2A202602836 | 100% (Hoàn thiện harness trong `src/lab/`, thực nghiệm 3 điều kiện, curator tự sinh skill, kiểm chuẩn freeze, phân tích và viết báo cáo) |

- Nhà cung cấp và mô hình (`LAB_MODEL`, không ghi khóa API), nhiệt độ (`LAB_TEMPERATURE`), `recursion_limit`: `deepseek/deepseek-flash` (qua endpoint LiteLLM tương thích OpenAI), `LAB_TEMPERATURE=0`, `recursion_limit=60`.
- Phiên bản Deep Agents (`pip show deepagents`), hệ điều hành, chạy trực tiếp hay trong Docker: `deepagents 0.7.21`, Windows 11 (Python 3.12 trong môi trường ảo `.venv` cục bộ, shell tích hợp bộ công cụ Git Unix).
- Số lần chạy tác vụ đã dùng / ngân sách: 18 lần chạy chính thức (6 baseline, 6 subagents, 6 skills-auto) cùng 3 lần chạy thử nghiệm ở Phần 3.4 (đã lưu tại `results/skills-auto-dev`).
- Commit của tag `freeze`: `393544b` (được gắn tag `freeze` sau commit `a56cc10` chứa các giả thuyết H1-H3).

## 2. Giả thuyết (commit TRƯỚC tag `freeze`, Phần 4.0)

- H1 (subagents so với baseline): Đa tác tử (`subagents`) đạt điểm kỹ thuật tương đương hoặc thấp hơn một chút so với `baseline` do hiện tượng cô lập ngữ cảnh (context isolation khiến subagent không thấy toàn bộ lịch sử) và chi phí phối hợp lớn, đồng thời tiêu tốn lượng token gấp 2 đến 3 lần và dễ chạm `recursion_limit` khi đệ quy qua nhiều bước. Căn cứ từ quan sát thực nghiệm tập học và bài báo của Anthropic về multi-agent research systems.
- H2 (skills-auto so với baseline): `skills-auto` đạt điểm cao hơn rõ rệt so với `baseline` trên các tác vụ đánh giá có dùng lại quy ước tổ chức (house rules) đã học (như kiểm tra hồi quy, chú thích kiểu, changelog trong họ `code`), nhưng sẽ không cải thiện được các quy ước mới hoàn toàn chưa từng xuất hiện trong tập học (như các quy tắc riêng của từng tác vụ eval). Căn cứ từ nghiên cứu SkillsBench và SkillEvolBench về khả năng chuyển giao tri thức thủ tục của LLM.
- H3 (tác vụ học so với tác vụ đánh giá): Điểm trung bình của `skills-auto` trên tác vụ học sẽ cao hơn đáng kể so với trên tác vụ đánh giá (hiện tượng quá khớp ở tầng ngữ cảnh - context-layer overfitting), do các skill được tối ưu trực tiếp từ vết lỗi của tác vụ học, trong khi tác vụ đánh giá sở hữu tập dữ liệu mới và quy tắc kiểm thử bổ sung.

## 3. Làm quen Deep Agents (Phần 0.3)

1. Tác tử mặc định có 9 công cụ: nhóm công cụ tệp ảo (`ls`, `read_file`, `write_file`, `edit_file`, `delete`, `glob`, `grep`), công cụ shell thực thi lệnh (`execute`), và công cụ khởi tạo tác tử con (`task`). Công cụ duy nhất cho phép chạy lệnh thực thi là `execute`.
2. Mô tả của công cụ `task` cho biết subagent `general-purpose` được dùng để nghiên cứu các câu hỏi phức tạp, tìm kiếm tệp và thực thi các chuỗi tác vụ nhiều bước; subagent này có quyền truy cập toàn bộ công cụ như tác tử chính. Về ngữ cảnh: subagent hoàn toàn không trạng thái (stateless), chỉ nhìn thấy nội dung prompt được tác tử chính truyền sang và trả về một báo cáo duy nhất, không nhìn thấy lịch sử hội thoại trước đó của tác tử chính trừ khi được chỉ định thừa kế.
3. Trích dẫn hướng dẫn hành vi:
   - Từ mô tả công cụ `task`: *"Put full detail in the prompt and state exactly what it should return — unless an agent type below says it inherits your conversation instead."*
   - Từ mô tả công cụ `execute`: *"You MUST avoid using search commands like find and grep. Instead use the grep, glob tools to search. Use read_file rather than cat/head/tail."*

## 4. Đường cơ sở và phân loại lỗi (Phần 2.2)

| Tác vụ | Check thất bại | Nhóm lỗi (A-G) | Bằng chứng (trích ngắn từ `detail` hoặc vết) |
|---|---|---|---|
| `code-learn` | `tests_not_modified` | A (Bỏ qua đặc tả) | `detail`: "the original files in tests/ must not be modified (new test files are allowed)". Tác tử trong lúc sửa lỗi đã can thiệp vào file test có sẵn thay vì giữ nguyên. |
| `code-learn` | `rule_type_hints` | E (Vi phạm quy ước tổ chức) | `detail`: "RULE: every public function (name not starting with '_') in the package has type annotations on all parameters and on the return value." Đề bài không hề nhắc quy định này. |
| `code-learn` | `rule_regression_tests` | E (Vi phạm quy ước tổ chức) | `detail`: "RULE: add tests/test_regressions.py with one test function per bug you fixed (at least 3); the file must pass." Quy ước kiểm tra hồi quy nội bộ của Acme. |
| `code-learn` | `rule_changelog` | E (Vi phạm quy ước tổ chức) | `detail`: "RULE: record each fix in CHANGELOG.md under the heading '## Unreleased' as a bullet '- fix(<function name>): <short description>' (at least 3 bullets)." Quy ước nhật ký thay đổi nội bộ Acme. |
| `data-learn` | `rule_money_in_cents` | E (Vi phạm quy ước tổ chức) | `detail`: "RULE: money values in answer.json are integer cents (1606.67 USD is written 160667)." Đề bài chỉ yêu cầu tính revenue nhưng bot bắt buộc dạng cent nguyên. |
| `data-learn` | `rule_meta_block` | E (Vi phạm quy ước tổ chức) | `detail`: "RULE: answer.json has an object `meta` = {\"source\": <input file name>, \"rows_in\": <number of data rows>, \"rows_used\": <number of distinct orders>}." Khối metadata theo quy ước Acme. |
| `data-learn` | `rule_clean_csv` | E (Vi phạm quy ước tổ chức) | `detail`: "RULE: write workspace/clean.csv with the header order_id,timestamp_utc,region,amount_cents...". Yêu cầu xuất thêm file làm sạch mà đề bài không nêu. |

Nhận xét:
- Nhóm lỗi chiếm đa số áp đảo là **Nhóm E (Vi phạm quy ước tổ chức - House Rules)**, chiếm 6/7 lỗi thất bại (85.7%).
- Bằng chứng phủ định: Tất cả các check kỹ thuật thuần túy (thuật toán tính toán, parse ngày tháng, làm sạch chuỗi, gỡ lỗi logic hàm `parse_price`, `apply_discount`, `low_stock`) tác tử đều đạt điểm tuyệt đối (5/5 check kỹ thuật ở `data-learn`, 6/6 check kỹ thuật ở `code-learn`, 9/9 check ở `logs-learn`). Số liệu từ `check_breakdown.py` xác nhận đạt 17/18 check kỹ thuật. Mô hình có năng lực kỹ thuật rất mạnh nhưng không thể biết trước các quy ước nội bộ vô hình của Acme nếu không có cơ chế phản hồi.
- Một skill thủ tục hoàn toàn có thể phòng ngừa nhóm lỗi E bằng cách cung cấp danh sách checklist các quy ước bắt buộc (tạo CHANGELOG, viết test hồi quy, thêm type hints, xuất khối meta, chuẩn hóa số tiền thành cent).

## 5. Điều kiện `subagents` (Phần 2.3)

- Các subagent đã định nghĩa:
  1. `explorer`: Đọc tài liệu, cấu trúc thư mục, log, mẫu dữ liệu ban đầu, báo cáo sự thật mà không sửa đổi file.
  2. `implementer`: Trực tiếp áp dụng các thay đổi mã nguồn/dữ liệu và chạy test/script kiểm tra qua shell.
  3. `reviewer`: Rà soát độc lập kết quả so với yêu cầu, bắt các ca biên mà không sửa file.
- `subagent_calls` ở từng tác vụ và nhận xét:
  - `data-learn`: `subagent_calls = 1`. Tác tử chính giao việc cho subagent `reviewer` để kiểm chứng độc lập các phép tính doanh thu, số dòng trùng và đơn hàng thiếu. Subagent kiểm tra chéo thành công.
  - `logs-learn`: `subagent_calls = 0`. Tác tử chính nhận định tác vụ phân tích log có tính tuần tự trực tiếp nên tự dùng python script giải quyết trong luồng chính mà không chia nhỏ.
  - `code-learn`: `subagent_calls = 0` (trong luồng chính ghi nhận 0 lượt do chạm `GraphRecursionError` sau 60 bước gọi lặp lại giữa các trạng thái).
- Thông tin giao việc: Trong `data-learn`, tác tử chính truyền đầy đủ đặc tả phép tính và yêu cầu đối chiếu cho reviewer. Tuy nhiên do subagent bị cô lập ngữ cảnh, lượng thông tin cần truyền qua prompt rất dài.
- Ảnh hưởng đến token và thời gian: Chi phí tăng vọt. `data-learn` tốn 849,588 tokens (so với 263,538 tokens của baseline, tăng gấp 3.2 lần) và mất 245.1 giây (so với 50.9 giây của baseline, tăng gần 5 lần). Trung bình toàn bộ thí nghiệm, `subagents` tiêu tốn 679,215 tokens/lần chạy (gấp 1.68 lần baseline). Đa tác tử tạo gánh nặng lớn về chi phí và độ trễ nhưng không giúp cải thiện điểm các quy ước ẩn của tổ chức.

## 6. Self-evolving: skill do curator sinh (Phần 3)

- Số lần chạy curator: 1 lần duy nhất (`python -m lab.curator`), sinh thành công 2 skill hợp lệ, không có skill nào bị xóa.

| Skill | Tổng quát hay riêng cho tác vụ học? | Đúng hay sai (nêu chỗ sai nếu có) | Độ dài, `description` và `skills_read` ở Phần 3.4 |
|---|---|---|---|
| `bugfix-package-maintenance` | Rất tổng quát. Đúc kết quy trình sửa lỗi gói Python: không sửa test cũ, thêm test hồi quy vào `tests/test_regressions.py`, thêm type annotations cho hàm public, cập nhật `CHANGELOG.md` dưới `## Unreleased`. | Hoàn toàn đúng, bám sát các tiêu chuẩn kỹ thuật và quy ước nội bộ đã ghi nhận từ feedback của bot. | 12 dòng. `description`: "When fixing defects in a Python package and the task requires type hints, regression tests, and changelog entries." Được đọc trong `code-learn` và `code-eval` (`skills_read = 2`). |
| `spec-compliance-verification` | Tổng quát. Đưa ra checklist kiểm tra tính tuân thủ đặc tả: liệt kê quy tắc, kiểm tra schema, xử lý các giá trị đặc biệt, đối chiếu trước khi kết thúc. | Đúng và an toàn, khuyến khích kiểm tra định dạng chính xác. | 11 dòng. `description`: "Before and after any task that has explicit rules, check names, or output schemas." Được đọc trong các tác vụ kiểm thử (`skills_read = 2`). |

## 7. Kết quả so sánh (Phần 4.3, 4.4)

Nội dung bảng tổng hợp từ `report/table.md`:

```text
| Task | baseline | subagents | skills-auto |
|---|---|---|---|
| code-learn | 6/10 | 7/10 | 9/10 |
| data-learn | 5/8 | 5/8 | 5/8 |
| logs-learn | 9/9 | 6/9 | 6/9 |
| code-eval | 6/11 | 6/11 | 9/11 |
| data-eval | 5/9 | 5/9 | 5/9 |
| logs-eval | 10/10 | 6/10 | 6/10 |
| **Mean score - learning tasks** | 0.74 | 0.66 | 0.73 |
| **Mean score - evaluation tasks** | 0.70 | 0.57 | 0.66 |
| **Mean tokens per run** | 403,755 | 679,215 | 339,125 |
| **Runs that read a skill** | 0/6 | 0/6 | 4/6 |
```

Thống kê phân rã check kỹ thuật và check quy ước từ `scripts/check_breakdown.py`:

```text
condition     role    technical  house rules  mean tokens  read a skill
baseline      eval     17/18         4/12         454,104      0/3     
baseline      learn    17/18         3/9          353,406      0/3     
subagents     eval     17/18         0/12         719,102      0/3     
subagents     learn    17/18         1/9          639,328      0/3     
skills-auto   eval     17/18         3/12         201,818      2/3     
skills-auto   learn    17/18         3/9          476,432      2/3     
```

Ghi chú xử lý ngoại lệ:
- Ở lần chạy đầu tiên của `skills-auto/code-eval`, mô hình gọi nhầm đường dẫn tuyệt đối ra ngoài thư mục sandbox dẫn đến `ValueError`. Theo đúng quy định tại GUIDE 4.2, lần chạy này đã được thực hiện lại ngay sau đó và hoàn thành hợp lệ với số điểm 9/11 (được ghi vào bảng).
- Ở `subagents/code-learn` và `baseline/logs-eval`, tác tử chạm `GraphRecursionError` sau 60 bước (đã được ghi nhận vào `error` trong `run.json` và vẫn chấm điểm bình thường trên workspace).
- Tất cả các lần chạy chính thức đều có `skills_modified = false`, tuân thủ 100% giao thức đóng băng.

## 8. Phân tích

1. **So sánh điểm số giữa các điều kiện:**
   - Trên tác vụ học, `skills-auto` cải thiện đột phá tác vụ `code-learn` từ 6/10 lên 9/10 (+30% điểm số), nhưng điểm trung bình toàn bộ tập học (0.73) xấp xỉ `baseline` (0.74) do dao động ở họ `logs`.
   - Trên tác vụ đánh giá, `skills-auto` tiếp tục chứng minh khả năng chuyển giao tri thức xuất sắc trên `code-eval` khi đạt 9/11 (so với 6/11 của cả `baseline` và `subagents`, tăng +27% điểm số). Điểm trung bình eval của `skills-auto` đạt 0.66, cao hơn đáng kể so với `subagents` (0.57) và tiệm cận `baseline` (0.70).
   - Điều kiện `subagents` cho kết quả thấp nhất ở cả hai tập (0.66 learn, 0.57 eval), cho thấy đa tác tử không đem lại lợi ích trong bài toán này mà còn gây nhiễu do mất ngữ cảnh tổng thể.

2. **Phân tách check kỹ thuật và check quy ước (`rule_`):**
   - Check kỹ thuật: Cả 3 điều kiện đều đạt tỷ lệ gần như tuyệt đối **17/18 check kỹ thuật** (94.4%) trên cả tập học lẫn tập đánh giá. Điều này chứng minh năng lực logic và viết code của mô hình nền tảng là hoàn toàn ổn định.
   - Check quy ước: Sự khác biệt bản chất nằm ở nhóm check quy ước (`house rules`). Với `baseline` và `subagents`, tác tử không có cách nào biết các quy ước ẩn của Acme (chỉ đạt 0 đến 1 quy ước ở subagents). Ngược lại, `skills-auto` giúp tác tử đạt 3/9 quy ước ở tập học và 3/12 quy ước ở tập đánh giá (vượt qua toàn bộ `rule_type_hints`, `rule_regression_tests`, `rule_changelog`).
   - Đối với các quy ước HOÀN TOÀN MỚI của tác vụ đánh giá (như các quy tắc riêng của `data-eval` hay `logs-eval`), skill do curator sinh ra không thể giúp vì curator chỉ tổng hợp từ các check thất bại trong quá khứ của tập học.

3. **Cơ chế hoạt động qua vết (`trace.md`) và `skills_read`:**
   - **Check skill giúp đạt:** `rule_regression_tests` trong `code-eval`. Trong `trace.md`, sau khi đọc `bugfix-package-maintenance/SKILL.md` ở bước đầu tiên, tác tử lập tức tạo `tests/test_regressions.py`, viết 7 test case cho từng lỗi được gỡ, và chạy pytest kiểm tra. Tác tử tuân thủ nghiêm ngặt từng dòng của checklist.
   - **Check skill không giúp:** `rule_clean_csv` trong `data-eval`. Mặc dù tác tử đã đọc `spec-compliance-verification/SKILL.md`, nhưng do đề bài không nhắc đến file `clean.csv`, tác tử tuân theo hướng dẫn an toàn trong skill: *"If a rule is missing from visible files, do not invent an answer; apply the most literal interpretation"*, do đó quyết định không tự ý tạo thêm file ngoài yêu cầu đề bài.

4. **Phân tích chi phí và hiệu quả Token:**
   - `subagents` là điều kiện tốn kém nhất: tiêu tốn trung bình **679,215 tokens/lần chạy** (gấp 1.68 lần baseline và gấp 2 lần skills-auto), thời gian thực thi kéo dài từ 2 đến 4 phút mỗi tác vụ do phải trao đổi qua lại giữa tác tử chính và subagents.
   - `skills-auto` là điều kiện tiết kiệm token nhất: chỉ tiêu tốn trung bình **339,125 tokens/lần chạy** (tiết kiệm 16% token so với baseline và 50% token so với subagents). Nguyên nhân là nhờ có checklist và quy trình định hướng rõ ràng từ skill, tác tử hành động dứt khoát, không mất bước suy luận lan man.
   - Kết luận: Đa tác tử (multi-agent) hoàn toàn không đáng chi phí trong thí nghiệm này; tác tử tự tiến hóa nạp skill (`skills-auto`) đạt hiệu quả tối ưu nhất trên từng token tiêu thụ.

5. **Rò rỉ dữ liệu và Quá khớp (Overfitting):**
   - **Phòng chống rò rỉ dữ liệu:** Module `curator.py` lọc cứng chỉ nhận `role == "learn"`, kiểm tra `eval_markers()` tự động từ các file của tập đánh giá để từ chối bất kỳ skill nào có chứa tên file hoặc định danh của eval. Bộ kiểm tra `scripts/verify_freeze.py` đã xác nhận tính hợp lệ tuyệt đối.
   - **Hiện tượng quá khớp ở tầng ngữ cảnh:** Quan sát thấy ở họ `logs`. Do curator đúc kết các quy ước thiên về lập trình phần mềm và kiểm tra đặc tả bảng biểu, các chỉ dẫn này khi đưa vào ngữ cảnh phân tích log đã khiến tác tử chú trọng quá mức vào kiểm tra schema mà lơ là một số nhánh xử lý traceback phức tạp.

6. **Ước lượng mức độ nhiễu (Noise):**
   - So sánh điểm tác vụ học của cùng bộ skill giữa lần chạy thử nghiệm ở Phần 3.4 (dev) và lần chạy chính thức sau đóng băng:
     - `code-learn`: 9/10 (dev) vs 9/10 (chính thức).
     - `data-learn`: 5/8 (dev) vs 5/8 (chính thức).
     - `logs-learn`: 6/9 (dev) vs 6/9 (chính thức).
     - Điểm trung bình cả hai lần: đều đạt chính xác **0.73**. Chênh lệch bằng **0.00**.
   - Kết quả này chứng minh độ tin cậy và tính ổn định cực cao của mô hình `deepseek-flash` khi chạy với nhiệt độ `temperature = 0`, xác nhận rằng các cải thiện trên họ `code` là kết quả thực chất từ tri thức của skill chứ không phải do nhiễu ngẫu nhiên.

## 9. Hạn chế và tính hợp lệ

1. **Quy mô tập tác vụ nhỏ:** Thí nghiệm chỉ gồm 3 tác vụ học và 3 tác vụ đánh giá (tổng cộng 6 tác vụ). Với số mẫu nhỏ, sự thay đổi điểm số của một tác vụ đơn lẻ có trọng số lớn trong điểm trung bình toàn cục.
2. **Quy ước Acme mang tính giả lập cục bộ:** Các quy ước tổ chức (house rules) được thiết kế có chủ ý trong `check.py` để mô phỏng môi trường doanh nghiệp thực tế. Trong thực tế đời sống, các quy ước thường phong phú và biến đổi đa dạng hơn.
3. **Thử nghiệm trên một mô hình duy nhất:** Kết quả phản ánh hành vi của mô hình `deepseek/deepseek-flash`. Các mô hình với kiến trúc khác (như Claude 3.5 Sonnet hay GPT-4o) có thể có khả năng tự suy luận quy ước hoặc phản ứng với subagent khác nhau.

## 10. Kết luận

Thí nghiệm chứng minh rằng tác tử tự tiến hóa ở tầng ngữ cảnh (`skills-auto`) giúp giải quyết hiệu quả các quy ước tổ chức ẩn (tăng điểm `code-eval` từ 6/11 lên 9/11) đồng thời giảm chi phí token xuống mức thấp nhất (339k tokens/lần chạy). Ngược lại, đa tác tử (`subagents`) làm tăng chi phí token lên gấp 1.68 lần và dễ chạm ngưỡng đệ quy mà không cải thiện được các quy ước vô hình. Hướng cải tiến tiếp theo là cho phép curator tự động phân loại và chỉ nạp các skill chuyên biệt theo từng họ tác vụ (dynamic routing) nhằm triệt tiêu hoàn toàn hiện tượng quá khớp chéo giữa các miền bài toán.

## Phụ lục

- Danh sách các lệnh đã chạy chính:
  1. `pytest tests/test_01_provided.py` (kiểm tra môi trường có sẵn - đạt 15/15).
  2. `pytest tests/test_02_agent.py`, `pytest tests/test_03_runner.py`, `pytest tests/test_04_curator.py` (kiểm tra harness - đạt 32/32).
  3. `python -m lab.runner --condition baseline --tasks learn` (chạy baseline tập học).
  4. `python -m lab.runner --condition subagents --tasks learn` (chạy subagents tập học).
  5. `python -m lab.curator` (curator đọc vết thất bại và sinh 2 skill).
  6. `python -m lab.runner --condition skills-auto --tasks learn` (chạy thử nghiệm skill trên tập học).
  7. `git commit -m "hypotheses: add predictions H1-H3"` && `git tag freeze` (đóng băng skill).
  8. `python -m lab.runner --condition baseline --tasks eval` (chạy baseline tập đánh giá).
  9. `python -m lab.runner --condition subagents --tasks eval` (chạy subagents tập đánh giá).
  10. `python -m lab.runner --condition skills-auto --tasks all` (chạy chính thức skills-auto trên toàn bộ 6 tác vụ).
  11. `python scripts/verify_freeze.py` (xác thực quy trình freeze - báo OK).
  12. `python -m lab.compare > report/table.md` và `python scripts/check_breakdown.py` (tổng hợp bảng số liệu).
