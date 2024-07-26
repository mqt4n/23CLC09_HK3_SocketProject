# 23CLC09_HK3_SocketProject
-----------------------------------------------------------------------------------------------------------

**Kịch bản giao tiếp của server và client**

**Vận hành phần I: Chương trình Client/Server cho phép nhiều Client download file từ 1 Server.**
**Server sẽ phục vụ tuần tự từng Client.**

-----------------------------------------------------------------------------------------------------------

**Phía server:**
- Server setup sẵn các địa chỉ IP và cổng để sẵn sàng khởi tạo socket
- Sau khi khởi tạo socket và bind, server sẽ lắng nghe các kết nối của client
- Khi có client kết nối tới server, server sẽ bắt đầu việc truyền tải file
- Đầu tiên, server sẽ có một danh sách các file client có thể tải, lưu các thông tin
  mỗi file vào một mảng.
  
- Sau đó, duyệt qua các từng file trong mảng chứa thông tin mỗi file, server sẽ gửi các thông
  tin cho client lần lượt là tên và kích thước. Khi đã gửi đầy đủ thông tin các file, server
  sẽ gửi từ khóa "END_LIST" nhằm báo hiệu cho client rằng đã gửi hết các file server có thể 
  phục vụ.
  
- Khi đã gửi xong danh sách các file client có thể tải, server sẽ chờ để nhận các yêu cầu
  của client. Mỗi lần nhận yêu cầu, server sẽ nhận tên của 1 file mà client yêu cầu, và kiểm
  tra xem file đó server có thể phục vụ không, nếu không thì thông báo về cho client không
  thể phục vụ file đó, nếu có thì gửi tín hiệu "START" cho client để bắt đầu việc tải file.
  
- Trong quá trình tải file, dung lượng file sẽ chia phần các phần nhỏ để gửi qua cho client,
  
- Đến khi đã tải file xong, server cũng gửi tín hiệu "END" để client biết rằng đã truyền tải
  hết dữ liệu file yêu cầu.
  
- Và sau đó server sẽ tiếp tục lắng nghe yêu cầu mới của client, đến khi client không còn yêu
  cầu nữa và đóng chương trình, server sẽ đóng kết nối với client và chờ để phục vụ các client
  mới kết nối đến.

**Phía client:**
- Client sẽ có các thao tác trước khi kết nối đến server. Kiểm tra đã có folder chứa các file
  tải từ server chưa, nếu chưa thì khởi tạo folder đó. Tiếp để là nhờ các thông tin có được như
  địa chỉ IP và cổng của server, client sẽ tạo socket và kết nối đến server.
  
- Khi đã kết nối đến server, client sẽ nhận lần lượt các tên và kích thước của từng file mà server
  có thể phục vụ. Sau khi nhận được tín hiệu là "END_LIST", đồng nghĩa với việc client đã nhận đủ
  danh sách các file có thể tải từ server, client sẽ in ra màn hình các tên file đó kèm với kích
  thước cho người dùng.
  
- Bên phía client cũng có một file #json# để ghi nhận các yêu cầu tải file của người dùng, khi người
  dùng nhập vào các file yêu cầu, client sẽ load các yêu cầu lên và lưu vào trong mảng các file yêu
  cầu để tiến hành tải các file đó.
  
- Với từng file trong mảng các file yêu cầu, client sẽ kiểm tra xem rằng file đó đã có trong folder
  tải về chưa, nếu có thì sẽ bỏ qua và tiếp tục tải các file tiếp theo, nếu chưa thì sẽ bắt đầu tải
  file đó.
  
- Bắt đầu việc tải file, client sẽ gửi tên file cần tải cho phía server. Nếu client nhận lại phản hồi
  từ phía server là "START", thì sẽ bắt đầu việc tải file đó giữa client và server.
- 

-----------------------------------------------------------------------------------------------------------

**Kịch bản giao tiếp của server và client**

**Vận hành phần II: Chương trình Client/Server cho phép nhiều Client download file từ 1 Server.**
**Server sẽ phục vụ song song các Client.**

-----------------------------------------------------------------------------------------------------------

**Phía server:**

- Cập nhật thư mục data, ghi tên, kích thước của từng file vào file_list.json

- Load nội dung gồm tên, kích thước từ file_list.json và một mảng trong chương trình

- Bind server và listen các kết nối đến từ client

- Thiết lặp một vòng while True và trong đó tiếp nhận các client, phân luồng bằng thread để
phục vụ cho từng client.

- Với mỗi client, server sẽ gửi danh sách các file có thể tải (file_list)

- Sau đó chờ client gửi về số lượng file cần tải và danh sách các tên file cần tải và độ
  ưu tiên của mỗi file.

- Server sẽ nhận danh sách đó và lưu vào một mảng gọi là data_require (tạm dịch là file yêu cầu)

- Sau đó in ra màn hình của server để đảm bảo không thiếu sót yêu cầu.

- Tiếp đến là thiết lập một mảng chứa kích thước của từng file (lengthOfEachFile),
  lưu tất cả kích thước bằng đơn vị bytes, mảng này cũng dùng cập nhật kích thước
  còn lại cần truyền của từng file.

- Sau đó, sẽ mở con trỏ file của tất cả các file yêu cầu từ phía client dưới dạng đọc binary,
  và lưu các con trỏ file này vào mảng file_pointer, để phục vụ cho việc tải song song, duyệt
  từng con trỏ file trong mảng, đọc data trong file và gửi cho client.

- Tiếp theo, sẽ mở một vòng while với điều kiện là khi nào mảng kích thước của từng file
  (lengthOfEachFile) có các phần tử trong mảng đều bằng không, có nghĩa là kích thước còn lại
  cần truyền của mỗi file đều bằng không, khi đó đã truyền file hoàn tất, thì vòng lặp dừng.

- Trong vòng lặp, chúng ta sẽ duyệt từng con trỏ file như đã để cập phía trên để truyền song song,
  kiểm tra kích thước file cần truyền còn hay không, sau đó thiết lập độ ưu tiên cho file đó, sau khi
  thiết lập độ ưu tiên xong, thì sẽ chạy một vòng lặp với số lần lặp đúng bằng độ ưu tiên đó, và gửi
  các phần data nhỏ cho client trong vòng lặp này. Mỗi lần như vậy sẽ cập nhật lại kích thước cần truyền
  của mỗi file.

- Sau mỗi lượt duyệt qua hết các con trỏ file, thì sẽ có thêm một tính năng là kiểm tra sẽ client có yêu
  cầu thêm file nào nữa không, nếu có thì lặp lại các bước tương tự trên, và thêm kích thước, con trỏ của
  các file mới vào các mảng tương ứng và tiếp tục việc truyền file của phía client.

- Sau khi đã truyền xong các file yêu cầu cho client, thì bên phía server sẽ in ra thông báo cho việc đó,
  đồng thời cũng chờ xem client có gửi thêm yêu cầu này hay không, nếu có thì lặp lại các bước ở trên,
  nếu không thì vẫn chờ cho đến khi client ngắt kết nối bằng ctrl+C

- Lưu ý rằng giữa các lần truyền data qua lại với client, đều sẽ chèn các gói ACK để đảm bảo không bị nhận
  dồn hoặc gửi dồn data

- Và server chỉ tắt khi mình tự tắt, đảm bảo tính "always on host" của server.

**Phía client:**

- Đàu tiên, client sẽ kiểm tra sẽ rằng đã tồn tại folder output hay chưa, nếu chưa thì sẽ tạo để chứa các
  file cần tải của client.

- Tiếp theo đó, client sẽ thực hiện kết nối với server thông qua HOST và POST đã biết từ trước

- Client sau khi kết nối sẽ nhận được danh sách các file có thể tải từ phía server

- Sau khi nhận được danh sách các file có thể tải, client sẽ in ra màn hình của client danh sách đó

- Đồng thời, cũng thêm danh sách đó vào một file để lưu trữ (file_list), tiện cho các thao tác lúc sau

- Sau khi in ra màn hình danh sách đó, client sẽ cập nhật lại kích thước của mỗi file bằng cách đổi 
  tất cả sang đơn vị bytes để tiện cho việc tải các file.

- Tiếp theo đó, sẽ tạo 2 mảng global là data_require_before và list_file_not_found, 1 biến global là
  total_file. Mục đích của data_require_before là lưu lại danh sách các file đã tải của client từ lúc
  thực thi chương trình, để tránh việc tải lại có file đó. Còn với list_file_not_found cũng khá tương
  tự, lưu lại các file không thể tải từ lúc chạy chương trình, tránh việc thông báo nhiều lần các file
  không thể tải. Biến total_file dùng với mục đích biết được đó lượng các file đã tải thành công từ lúc
  thực thi chương trình.

- Sau công tác tạo các biến để hỗ trợ, client sẽ bước vào một vòng lặp vô tận để phục vụ cho việc tải file,
  vòng lặp này chỉ ngắt khi mà người dùng Ctrl-C.

- Thao tác đầu tiên trong vòng lặp là client đọc file input.txt gồm tên file và độ ưu tiên của từng file, lưu
  vào mảng data_require_after. Mảng này phục vụ cho việc biết được những file cần tải ngay lúc đó.

- Sau đó sẽ có một bước sàn lọc từ phía client, lọc ra các file có thể tải được, các file không dựa trên danh sách
  các file mà server đã gửi trước đó. Sau đó lưu các file có thể tải vào list_download, các file không thể tải vào
  list404 (404 là viết tắt cho file not found).

- Cập nhật lại data_require_after sau khi đọc lọc các file có thể tại

- So sánh data_require_after và data_require_before xem số lượng phần tử (file) của hai mảng này có bằng nhau hay
  không, nếu không thì sẽ tải các file chênh lệch giữa 2 mảng, nếu bằng nhau (áp dụng cho lần yêu cầu thứ 2 trở đi)
  thì có nghĩa là file input.txt chưa được cập nhật các yêu cầu mới đến từ client.

- Nếu có sự chênh lệch giữa các mảng, thì sẽ cập nhật lại mảng data_require_after với các phần tử mới cần tải.

- Tiếp theo, sẽ gửi đi số lượng file cần tải cho file server. Sau đó là gửi các thông tin về tên file cũng như độ ưu
  tiên của từng file cho server.

- Sau khi hoàn tất việc gửi thông tin các file, client sẽ làm thao tác tương tự bên phía server là tạo mảng gồm các con
  trỏ file của tất cả các file yêu cầu, phục vụ cho việc gửi dữ liệu song song. Mảng chứa con trỏ ghi file là file_pointer.

- Phần tiếp theo thực thi tương tự bên phía server trong việc nhận các phần data nhỏ từ phía server.

- Sau mỗi lượt duyệt mảng con trỏ ghi file, client sẽ load lại file input.txt xem người dùng có nhập thêm yêu
  cầu gì hay không, nếu có thì thêm vào mảng con trỏ và mang kích thước mỗi file để chuẩn bị có quá trình tải file
  tiếp theo.

- Ngoài ra, sau mỗi lượt tải file, client sẽ in ra phần trăm hoàn thành của file đó, số dòng sẽ tương ứng với số file
  tải trong lượt đó, và đồng thời sau khi in ra, client cũng xóa các dòng đó để lượt sau in ra trên cùng vị trí, không
  bị in lại nhiều lần tạo tính thẩm mỹ cho chương trình.

- Cuối cùng, khi đã tải hoàn tất các data của mỗi file, sẽ đóng lần lượt các con trỏ ghi file lại, thêm các file vừa tải
  vào mảng các file đã tải, và thông báo ra màn hình cho người dùng.

- In ra thông báo rằng, nếu như muốn tải tiếp thì hãy cập nhật trong file input.txt và Ctrl+S lại, nếu không thì hãy thoát
  chương trình bằng cách Ctrl+C.

-----------------------------------------------------------------------------------------------------------
