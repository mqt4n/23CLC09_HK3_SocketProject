# 23CLC09_HK3_SocketProject

_link report: https://docs.google.com/document/d/1Y-v9ptRORQNd10V5OXOFEHTUPCYQeIdG/edit_

**Vận hành phần I: Chương trình Client/Server cho phép nhiều Client download file từ 1 Server. Server sẽ phục vụ tuần tự từng Client.**

**Phía server:**

- Server chuẩn bị sẵn các địa chỉ IP và cổng để sẵn sàng khởi tạo socket.
- Sau khi khởi tạo socket và bind, server sẽ lắng nghe các kết nối của client.
- Khi có client kết nối tới server, server sẽ bắt đầu việc truyền tải file.
- Đầu tiên, server sẽ có một danh sách các file client có thể tải, lưu các thông tin mỗi file vào một mảng.
- Sau đó, duyệt qua các từng file trong mảng chứa thông tin mỗi file, server sẽ gửi các thông tin cho client lần lượt là tên và kích thước. Khi đã gửi đầy đủ thông tin các file, server sẽ gửi từ khóa "END_LIST" nhằm báo hiệu cho client rằng đã gửi hết các file server có thể phục vụ.
- Khi đã gửi xong danh sách các file client có thể tải, server sẽ chờ để nhận các yêu cầu của client. Mỗi lần nhận yêu cầu, server sẽ nhận tên của 1 file mà client yêu cầu, và kiểm tra xem file đó server có thể phục vụ không, nếu không thì thông báo về cho client không thể phục vụ file đó, nếu có thì gửi tín hiệu "START" cho client để bắt đầu việc tải file.
- Trong quá trình tải file, dung lượng file sẽ chia phần các phần nhỏ để gửi qua cho client,
- Đến khi đã tải file xong, server cũng gửi tín hiệu "END" để client biết rằng đã truyền tải hết dữ liệu file yêu cầu.
- Và sau đó server sẽ tiếp tục lắng nghe yêu cầu mới của client, đến khi client không còn yêu cầu nữa và đóng chương trình, server sẽ đóng kết nối với client và chờ để phục vụ các client mới kết nối đến.
  
**Phía client:**
  
- Client sẽ có các thao tác trước khi kết nối đến server. Kiểm tra đã có folder chứa các file tải từ server chưa, nếu chưa thì khởi tạo folder đó. Tiếp để là nhờ các thông tin có được như địa chỉ IP và cổng của server, client sẽ tạo socket và kết nối đến server.
- Khi đã kết nối đến server, client sẽ nhận lần lượt các tên và kích thước của từng file mà server có thể phục vụ. Sau khi nhận được tín hiệu là "END_LIST", đồng nghĩa với việc client đã nhận đủ danh sách các file có thể tải từ server, client sẽ in ra màn hình các tên file đó kèm với kích thước cho người dùng.
- Bên phía client cũng có một file txt để ghi nhận các yêu cầu tải file của người dùng, khi người dùng nhập vào các file yêu cầu, client sẽ load các yêu cầu lên và lưu vào trong mảng các file yêu cầu để tiến hành tải các file đó.
- Với từng file trong mảng các file yêu cầu, client sẽ kiểm tra xem rằng file đó đã có trong folder tải về chưa, nếu có thì sẽ bỏ qua và tiếp tục tải các file tiếp theo, nếu chưa thì sẽ bắt đầu tải file đó.
- Bắt đầu việc tải file, client sẽ gửi tên file cần tải cho phía server. Nếu client nhận lại phản hồi từ phía server là "START", thì sẽ bắt đầu việc tải file đó giữa client và server.
- Cho đến khi client nhận được tín hiệu “END” trong các gói tin gửi, việc truyền tải dữ liệu của file đang tải sẽ kết thúc vì đã hoàn thành tải file. Sau đó là hiển thị thông báo đã tải hoàn tất file và tiếp tục tải file tiếp theo.
- Khi đã tải xong các file yêu cầu 1 đợt, sẽ đợi người dùng nhập thêm các file yêu cầu tiếp theo để tiếp tục quá trình tải file.
- Nếu người dùng muốn dừng chương trình thì sẽ nhấn tổ hợp Ctrl + C, chương trình phía client sẽ kết thúc và ngắt kết nối với server.
--------------------------------------------------------------------------------------------------------------------------------------------------------
**Vận hành phần II: Chương trình Client/Server cho phép nhiều Client download file từ Server theo độ ưu tiên. Server phục vụ nhiều Client cùng lúc.**

**Phía server:**

- Server sẽ thiết lập trước các nội dung cần thiết cho quá trình phục vụ tải file từ các client như có trước địa chỉ IP và cổng kết nối, kiểm tra xem trong thư mục chứa các file phục vụ client có những file nào, cập nhật và ghi lên một file chứa các thông tin về các file cho client tải.
- Sau khi đã hoàn thành các công tác chuẩn bị, server sẽ load file chứa thông tin các file phục vụ client vào chương trình và thực hiện khởi tạo socket với địa chỉ IP và số cổng đã chuẩn bị từ trước.
- Với mỗi client kết nối thông qua socket đã khởi tạo từ server, server sẽ tạo một luồng (hay có thể nói là một kết nối dành riêng cho client đó) để có thể phục vụ song song nhiều client cùng một lúc.
- Xem xét quá trình phục vụ cho một client, sau khi kết nối với client, server sẽ gửi cho client số lượng và danh sách các file có thể tải từ phía server.
- Trong quá trình gửi dữ liệu giữa client và server, sẽ có các lần gửi và nhận tín hiệu “ACK” để tránh việc dữ liệu không được truyền như mong muốn (ví dụ như việc bị gửi dồn dữ liệu, 3 lần gửi mà chỉ cần 1 lần nhận).
- Sau khi đã nhận gửi danh sách các file có thể tải, server sẽ chờ đợi các yêu cầu từ phía client.
- Server sẽ nhận được số lượng các file cần tải từ phía client, sau đó lần lượt nhận các thông tin như tên và độ ưu tiên của file đó, lưu vào một mảng dữ liệu để sử dụng cho việc truyền tải file.
- Sau khi đã có được những yêu cầu của client, server sẽ thiết lập một số thứ để chuẩn bị cho việc tải các file client yêu cầu, cụ thể như là mảng kích thước hiện tại của file để cập nhật tiến trình tải file, mảng các con trỏ file để phục vụ cho việc tải song song nhiều file cùng một lúc, đọc một lúc nhiều file.
- Sau các công tác trước việc truyền tải, server sẽ bắt đầu truyền dữ liệu đến phía client. Server sẽ truyền dữ liệu bằng cách truyền từng khúc dữ liệu nhỏ của mỗi file yêu cầu một cách tuần tự. Và mỗi file sẽ có độ ưu tiên khác nhau, tùy vào độ ưu tiên đó mà trong lượt truyền dữ liệu có file đó, server sẽ truyền nhiều lần từng khúc dữ liệu nhỏ của file đó để đảm bảo tính ưu tiên của file đó.
- Trong quá trình truyền tải file, sau mỗi lần duyệt qua các file và đã truyền các khúc dữ liệu nhỏ tương ứng, server sẽ lắng nghe tín hiệu từ client để xem client có yêu cầu thêm các file mới không.
- Nếu có thì server sẽ cập nhật lại các file yêu cầu cần tải, chuẩn bị cho quá trình tải của các file yêu cầu mới, và tiếp tục tải file cho đến khi truyền tải xong dữ liệu của tất cả các file.
- Sau khi đã tải xong 1 đợt các file yêu cầu từ phía client, server sẽ tiếp tục lắng nghe các yêu cầu mới để phục vụ cho client. Nếu có các yêu cầu mới thì lặp lại các bước ở trên và tiếp tục quá trình truyền tải file.
- Cho đến khi client chủ động ngắt kết nối, thì server sẽ ngắt kết nối với client và kết thúc quá trình truyền tải giữa server và client đó.
- Server sẽ bật cho đến khi người dùng bên phía server tắt, để đảm bảo tính “always on host” của server và phục vụ cho client mọi lúc.
  
**Phía client:**

- Đầu tiên, client sẽ thiết lập một số thứ trước khi kết nối đến server, như là địa chỉ IP của server và số cổng kết nối, kiểm tra thư mục chứa các file yêu cầu có chưa để khởi tạo.
- Sau đó, client sẽ thực hiện kết nối đến server thông qua địa chỉ IP và số cổng đã chuẩn bị từ trước. Khởi tạo một socket để phục vụ cho việc tiếp nhận các dữ liệu tải về từ phía server.
- Khi đã hoàn tất việc kết nối, client sẽ nhận được danh sách các file có thể tải đến từ phía server, và lúc này các thông tin nhận được sẽ lưu vào một mảng để tiện cho việc xử lí về sau, đồng thời cũng in ra màn hình phía client danh sách đó để người dùng có thể xem và nhập vào các file muốn tải.
- Sau khi đã nhận được danh sách các file có thể tải từ phía server, bên phía client sẽ có một file hỗ trợ là file “input.txt” để người dùng ghi vào đó các file muốn tải và độ ưu tiên cho file đó. Khi đã ghi xong thì lưu bằng tổ hợp phím Ctrl + S.
- Khi đã ghi xong các file muốn tải vào file “input.txt”, chương trình phía client sẽ quét xem các yêu cầu trong file “input.txt” là gì, lưu các yêu cầu đó vào chương trình để xử lý. Ngoài ra, cũng gửi các yêu cầu đó cho phía server để server có thể chuẩn bị cho việc cung cấp các file yêu cầu của phía client.
- Chương trình client đồng thời cũng thiết lập một “đồng hồ”, để sau một khoảng thời gian nhất định (theo yêu cầu đề bài là 2s) thì sẽ kiểm tra xem người dùng có yêu cầu thêm các file mới hay không, để cập nhật và tải thêm các file đó.
- Trước quá trình truyền tải file thì client cũng có một số thứ cần chuẩn bị để phục vụ cho việc tải file như kiểm tra các file nào đã tải rồi, các file không được phục vụ từ phía server, mở con trỏ file của các file yêu cầu để ghi dữ liệu vào, kích thước còn lại của file cần tải để hiển thị tiến trình tải file theo phần trăm …
- Sau các công tác chuẩn bị đã đề cập ở trên, client bắt đầu quá trình nhận các dữ liệu từ phía server. Quá trình này sẽ tải cùng một lúc tất cả các file yêu cầu của người dùng, và đồng thời cũng cập nhật các yêu cầu mới.
- Tương tự bên server thì client cũng sẽ nhận lần lượt các dữ liệu nhỏ của mỗi file, tùy vào mức độ ưu tiên của file đó mà dữ liệu nhận sẽ tương ứng với độ ưu tiên đó.
- Trong quá trình tải các file thì phía client cũng hiển thị tiến trình tải file thông qua phần trăm được tính bằng lượng dữ liệu đã nhận trên tổng lượng dữ liệu của file đó.
- Khi đã hoàn thành xong 1 đợt yêu cầu tải file, thì người dùng có thể tiếp tục yêu cầu thêm các file khác bằng cách ghi vào file “input.txt” và server sẽ tiếp tục phục vụ việc tải các file theo yêu cầu mới, lặp lại các quá trình đã đề cập ở trên.
- Sau khi nhận đủ các file mong muốn, người dùng phía client có thể kết thúc chương trình bằng tổ hợp phím Ctrl + C.
