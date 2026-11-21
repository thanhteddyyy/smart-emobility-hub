# **I. Đặc tả phương thức (Method Description)** 

## **1.1. Use Case UC1 - Tìm phương tiện và Hub phù hợp** 

### **_1.1.1. searchVehicleAndHub()_** 

|**Thuộc tính**|**Nội dung chi tiết**|
|---|---|
|**Tênphương thức**|searchVehicleAndHub()|
|**Mục đích**|Tìm các phương tiện điện dùng chung hoặc Mobility Hub phù hợp<br>với vị trí và tiêu chí tìm kiếm của sinh viên, hỗ trợ cả 2 kiểu tìm<br>(theophươngtiện - Normal Flow, hoặc theo Hub - AF2).|
|**Tham số đầu vào**<br>**(@param)**|location: Location - vị trí tìm kiếm (GPS hoặc chọn thủ công, AF1);<br>radiusKm: double - bán kính tìm; searchType: SearchType<br>{VEHICLE, HUB}; vehicleType: String - loại xe mong muốn (chỉ<br>áp dụng khi searchType=VEHICLE); minBatteryLevel: double -<br>mứcpin tối thiểu(chỉ ápdụngkhi searchType=VEHICLE).|
|**Giá trị trả về (@return)**|List<SearchResultDTO> - danh sách kết quả sắp xếp theo khoảng<br>cách tăng dần, kèm trạng thái và thời điểm cập nhật; danh sách rỗng<br>nếu khôngcó kếtquảphù hợp (AF3).|
|**Ngoại lệ (@exception)**|InvalidLocationException (EX1); InvalidSearchCriteriaException<br>(EX2); MapServiceUnavailableException (EX3);<br>DataSourceUnavailableException(EX4).|
|**Tiền điều kiện (Pre-**<br>**conditions)**|Hệ thống đã cấu hình danh mục và toạ độ các Hub thuộc phạm vi<br>phục vụ; khôngbắt buộc sinh viên đăngnhập.|
|**Hậu điều kiện (Post-**<br>**conditions)**|Trả về kết quả phù hợp kèm thời điểm cập nhật, hoặc danh sách<br>rỗng; không ghi/sửa bất kỳdữ liệu nào(thao tác chỉ đọc).|
||function searchVehicleAndHub(location, radiusKm, searchType,<br>vehicleType, minBatteryLevel):<br>if location == null: throw InvalidLocationException<br>if radiusKm <= 0: throw InvalidSearchCriteriaException<br>try:<br>candidates = dataAccess.findWithinRadius(<br>location, radiusKm, searchType)<br>catch DataAccessError:|
|**Luồng thuật toán**<br>**(Pseudo-code)**|throw DataSourceUnavailableException<br>if searchType == VEHICLE:<br>results = filter(candidates,<br>type==vehicleType AND battery>=minBatteryLevel<br>AND status==AVAILABLE)<br>else:<br>results = candidates<br>// kèm số xe/chỗ đỗ/cổng sạc khả dụng mỗi Hub<br>sort results by distance(location) ascending<br>return results|



### **_1.1.2. resolveSearchLocation()_** 

|**Thuộc tính**|**Nội dung chi tiết**|
|---|---|
|**Tênphương thức**|resolveSearchLocation()|
|**Mục đích**|Xác định vị trí dùng làm tâm tìm kiếm: ưu tiên vị trí do Sinh viên<br>chọn thủ công trên bản đồ (AF1), nếu không có thì dùng toạ độ GPS<br>của thiết bị(bước 3-4 của UC1).|
|**Tham số đầu vào**<br>**(@param)**|gpsLocation: Location (nullable) - toạ độ GPS lấy từ thiết bị;<br>manualLocation: Location (nullable) - vị trí, khu vực hoặc Hub Sinh<br>viên chọn trên bản đồ.|
|**Giá trị trả về (@return)**|Location - vị trí tìm kiếm hợp lệ, nằm trong phạm vi phục vụ của<br>khu đô thị ĐHQG-HCM.|
|**Ngoại lệ (@exception)**|InvalidLocationException (EX1) - khi cả 2 tham số đều null hoặc vị<br>trí nằm ngoàiphạm viphục vụ.|
|**Tiền điều kiện (Pre-**<br>**conditions)**|Giao diện tìm kiếm đang hiển thị; phạm vi phục vụ<br>(SERVICE_AREA)đã được cấu hình.|
|**Hậu điều kiện (Post-**<br>**conditions)**|Trả về đúng 1 vị trí tìm kiếm để hiển thị trên bản đồ (bước 4); không<br>lưu vị trí của Sinh viên vào cơ sở dữ liệu.|
|**Luồng thuật toán**<br>**(Pseudo-code)**|function resolveSearchLocation(gpsLocation, manualLocation):<br>if manualLocation != null:<br>location = manualLocation        // AF1: ưu tiên chọn tay<br>else if gpsLocation != null:<br>location = gpsLocation<br>else:<br>throw InvalidLocationException   // EX1<br>if not SERVICE_AREA.contains(location):<br>throw InvalidLocationException<br>return location|



### **_1.1.3. validateSearchCriteria()_** 

|**Thuộc tính**|**Nội dung chi tiết**|
|---|---|
|**Tênphương thức**|validateSearchCriteria()|
|**Mục đích**|Kiểm tra tính hợp lệ của tiêu chí tìm kiếm trước khi truy vấn dữ liệu<br>(bước 6 của UC1), tránh truy vấn vô nghĩa và chỉ rõ trường cần sửa<br>cho Sinh viên(EX2).|
|**Tham số đầu vào**<br>**(@param)**|criteria: SearchCriteria - gồm radiusKm: double, searchType:<br>SearchType, vehicleType: String (nullable), minBatteryLevel:<br>double(nullable).|
|**Giá trị trả về (@return)**|void - không trả giá trị; phương thức kết thúc bình thường nghĩa là<br>tiêu chí hợplệ.|
|**Ngoại lệ (@exception)**|InvalidSearchCriteriaException (EX2) - kèm danh sách các trường<br>khônghợplệ đểgiao diện đánh dấu.|
|**Tiền điều kiện (Pre-**<br>**conditions)**|Sinh viên đã nhập tiêu chí và gửi yêu cầu tìm kiếm (bước 5).|
|**Hậu điều kiện (Post-**<br>**conditions)**|Nếu hợp lệ, luồng tiếp tục truy vấn dữ liệu; nếu không hợp lệ, không<br>có truyvấn nào đượcgửi xuốngtầngdữ liệu.|



|**Thuộc tính**|**Nội dung chi tiết**|
|---|---|
||function validateSearchCriteria(criteria):<br>errors = []<br>if criteria.radiusKm <= 0 OR<br>criteria.radiusKm > MAX_SEARCH_RADIUS_KM:<br>errors.add("radiusKm")|
|**Luồng thuật toán**<br>**(Pseudo-code)**|if criteria.searchType == null: errors.add("searchType")<br>if criteria.searchType == VEHICLE:<br>if criteria.minBatteryLevel != null AND<br>(minBatteryLevel < 0 OR minBatteryLevel > 100):<br>errors.add("minBatteryLevel")<br>if errors not empty:<br>throw InvalidSearchCriteriaException(errors)|



### **_1.1.4. displayResultsOnMap()_** 

|**Thuộc tính**|**Nội dung chi tiết**|
|---|---|
|**Tênphương thức**|displayResultsOnMap()|
|**Mục đích**|Gửi danh sách kết quả tới Map API để hiển thị vị trí Hub trên bản đồ<br>(bước 7 của UC1); khi Map API không khả dụng thì chuyển sang<br>chế độ hiển thị danh sách(EX3).|
|**Tham số đầu vào**<br>**(@param)**|results: List<SearchResultDTO> - kết quả tìm kiếm đã sắp xếp;<br>searchLocation: Location - tâm tìm kiếm.|
|**Giá trị trả về (@return)**|MapViewModel - dữ liệu hiển thị gồm các điểm đánh dấu (marker)<br>trên bản đồ, hoặc chế độ LIST_ONLY nếu bản đồ lỗi.|
|**Ngoại lệ (@exception)**|Không ném ngoại lệ ra ngoài: MapServiceUnavailableException từ<br>MapAdapter được bắt và xử lýbằngchế độ dựphòng.|
|**Tiền điều kiện (Pre-**<br>**conditions)**|Đã có kết quả từ searchVehicleAndHub (có thể là danh sách rỗng).|
|**Hậu điều kiện (Post-**<br>**conditions)**|Sinh viên luôn nhận được kết quả, dạng bản đồ hoặc dạng danh sách;<br>khôngthayđổi dữ liệu.|
|**Luồng thuật toán**<br>**(Pseudo-code)**|function displayResultsOnMap(results, searchLocation):<br>view = new MapViewModel(results)<br>try:<br>markers = mapAdapter.renderMarkers(<br>searchLocation, results.hubLocations)<br>view.setMarkers(markers)<br>view.mode = MAP<br>catch MapServiceUnavailableException:   // EX3<br>view.mode = LIST_ONLY<br>view.notice = "Bản đồ tạm thời không khả dụng"<br>return view|



## **1.2. Use Case UC2 - Xem trạng thái phương tiện và Hub** 

### **_1.2.1. getResourceStatus()_** 

|**Thuộc tính**|**Nội dung chi tiết**|
|---|---|
|**Tênphương thức**|getResourceStatus()|
|**Mục đích**|Lấy trạng thái gần thời gian thực của 1 phương tiện hoặc 1 Mobility<br>Hub cụ thể, phục vụ sinh viên ra quyết định tiếp theo (đặt<br>xe/chỗ/sạc).|
|**Tham số đầu vào**<br>**(@param)**|resourceType: ResourceType {VEHICLE, HUB}; resourceId: String<br>- mã định danh tài nguyên.|
|**Giá trị trả về (@return)**|ResourceStatusDTO - trạng thái chi tiết kèm thời điểm cập nhật gần<br>nhất; đánh dấu "stale" nếu dữ liệuquá cũ(EX4).|
|**Ngoại lệ (@exception)**|ResourceNotFoundException (EX2);<br>DataSourceUnavailableException(EX3).|
|**Tiền điều kiện (Pre-**<br>**conditions)**|resourceId hợp lệ, đã chọn từ kết quả UC1 hoặc nhập trực tiếp; hệ<br>thốngcó hoặc truyxuất được dữ liệu trạngthái.|
|**Hậu điều kiện (Post-**<br>**conditions)**|Trả về đúng trạng thái và thời điểm cập nhật của tài nguyên; không<br>ghi/sửa dữ liệu.|
|**Luồng thuật toán**<br>**(Pseudo-code)**|function getResourceStatus(resourceType, resourceId):<br>if resourceId is empty: throw InvalidArgumentException<br>try:<br>resource = dataAccess.findById(resourceType, resourceId)<br>catch DataAccessError:<br>throw DataSourceUnavailableException<br>if resource == null: throw ResourceNotFoundException<br>status = buildStatusDTO(resource)<br>if resource.lastUpdatedAt older than STALE_THRESHOLD:<br>status.markAsStale()<br>return status|



### **_1.2.2. buildVehicleStatus()_** 

|**Thuộc tính**|**Nội dung chi tiết**|
|---|---|
|**Tênphương thức**|buildVehicleStatus()|
|**Mục đích**|Tổng hợp thông tin trạng thái chi tiết của một phương tiện để hiển<br>thị cho Sinh viên(bước 3 của UC2 - nhánh 1a).|
|**Tham số đầu vào**<br>**(@param)**|vehicle: Vehicle - thực thể phương tiện đã truy xuất từ cơ sở dữ liệu.|
|**Giá trị trả về (@return)**|VehicleStatusDTO - gồm loại xe, trạng thái, mức pin, Hub hiện tại,<br>thời điểm cậpnhật và cờ isAvailable.|
|**Ngoại lệ (@exception)**|Khôngcó.|
|**Tiền điều kiện (Pre-**<br>**conditions)**|vehicle khác null (đã kiểm tra tồn tại trong getResourceStatus).|
|**Hậu điều kiện (Post-**<br>**conditions)**|Trả về DTO chỉ đọc; không thay đổi thực thể Vehicle.|



|**Thuộc tính**|**Nội dung chi tiết**|
|---|---|
|**Luồng thuật toán**<br>**(Pseudo-code)**|function buildVehicleStatus(vehicle):<br>dto = new VehicleStatusDTO()<br>dto.vehicleType = vehicle.vehicleType<br>dto.status = vehicle.status<br>dto.batteryLevel = vehicle.batteryLevel<br>dto.currentHub = vehicle.currentHub.name<br>dto.lastUpdatedAt = vehicle.lastUpdatedAt<br>dto.isAvailable = (vehicle.status == AVAILABLE)<br>return dto|



### **_1.2.3. buildHubStatus()_** 

|**Thuộc tính**|**Nội dung chi tiết**|
|---|---|
|**Tênphương thức**|buildHubStatus()|
|**Mục đích**|Tổng hợp trạng thái của một Mobility Hub: số phương tiện khả<br>dụng, chỗ đỗ trống, cổng sạc khả dụng và mức độ sử dụng (bước 3<br>của UC2 - nhánh 1b).|
|**Tham số đầu vào**<br>**(@param)**|hub: MobilityHub - thực thể Hub kèm danh sách phương tiện, chỗ<br>đỗ và cổngsạc.|
|**Giá trị trả về (@return)**|HubStatusDTO - gồm availableVehicles, emptySpots,<br>availablePorts, usageRate(0-1)và lastUpdatedAt.|
|**Ngoại lệ (@exception)**|Khôngcó.|
|**Tiền điều kiện (Pre-**<br>**conditions)**|hub khác null; hub.capacity đã được cấu hình.|
|**Hậu điều kiện (Post-**<br>**conditions)**|Trả về DTO chỉ đọc; không thay đổi thực thể MobilityHub.|
|**Luồng thuật toán**<br>**(Pseudo-code)**|function buildHubStatus(hub):<br>dto = new HubStatusDTO()<br>dto.availableVehicles = count(hub.vehicles,<br>status==AVAILABLE)<br>dto.emptySpots = count(hub.parkingSpots, status==EMPTY)<br>dto.availablePorts = count(hub.chargingPorts,<br>status==AVAILABLE)<br>dto.usageRate = (hub.capacity - dto.emptySpots) / hub.capacity<br>dto.lastUpdatedAt = hub.lastUpdatedAt<br>return dto|



### **_1.2.4. isStatusStale()_** 

|**Thuộc tính**|**Nội dung chi tiết**|
|---|---|
|**Tênphương thức**|isStatusStale()|
|**Mục đích**|Xác định dữ liệu trạng thái của tài nguyên đã quá cũ hay chưa, làm<br>cơ sở để đánh dấu "chưa đáng tin cậy" và không khẳng định tài<br>nguyên còn khả dụng (EX4 của UC2; liênquan NFR02).|
|**Tham số đầu vào**<br>**(@param)**|lastUpdatedAt: DateTime (nullable) - thời điểm cập nhật gần nhất<br>của tài nguyên.|
|**Giá trị trả về (@return)**|boolean - true nếu dữ liệu quá cũ hoặc chưa xác định, false nếu còn<br>mới.|



|**Thuộc tính**|**Nội dung chi tiết**|
|---|---|
|**Ngoại lệ (@exception)**|Khôngcó.|
|**Tiền điều kiện (Pre-**<br>**conditions)**|Hằng số STALE_THRESHOLD đã được cấu hình (ví dụ 15 giây<br>theo NFR02, hoặc ngưỡngdo nhómquyđịnh).|
|**Hậu điều kiện (Post-**<br>**conditions)**|Không thay đổi dữ liệu; kết quả được dùng để gắn cờ stale cho DTO.|
|**Luồng thuật toán**|function isStatusStale(lastUpdatedAt):<br>if lastUpdatedAt == null:|
|**(Pseudo-code)**|return true          // trạng thái chưa xác định<br>return(now()- lastUpdatedAt)> STALE_THRESHOLD|



## **1.3. Use Case UC3, UC4, UC5, UC17 - Đặt chỗ và Xác thực** 

### **_1.3.1. BookingConfirmModal.confirmBooking()_** 

|**Thuộc tính**|**Nội dung chi tiết**|
|---|---|
|**Tên phương thức**|+ confirmBooking(sessionId: String, request: BookingRequest):<br>Booking|
|**Mục đích**|Gửiyêu cầu xác nhận đặt xe hoặc chỗ đỗ.|
|**Tham số đầu vào**<br>**(@param)**|sessionId: String – mã phiên đăng nhập.<br>request: BookingRequest – dữ liệu yêu cầu đặt chỗ, gồm tài nguyên,<br>Hub, thờigian và mãyêu cầu để đối soát khi thử lại.|
|**Giá trị trả về(@return)**|Booking– Đơn đặt chỗ sau khi xử lý.|
|**Ngoại lệ (@exception)**|AuthenticationRequired: phiên không hợp lệ;<br>ValidationError: dữ liệu sai;<br>BookingConflict: tài nguyên không còn khả dụng;<br>StorageError: lỗi lưu hoặc chưa xác định kếtquả.|
|**Tiền điều kiện (Pre-**<br>**conditions)**|Người dùng đã chọn tài nguyên và đăng nhập.|
|**Hậu điều kiện (Post-**<br>**conditions)**|Hiển thị đơn đã lưu hoặc thông báo lỗi.|
|**Luồng thuật toán**<br>**(Pseudo-code)**|1. Đọc lựa chọn của người dùng.<br>2. Gửi yêu cầu đến phương thức đặt xe hoặc đặt chỗ đỗ tương ứng.<br>3. Hiển thị kếtquả; chỉ báo thành côngkhi đơn đã lưu.|



### **_1.3.2. BookingConfirmModal.cancelBooking()_** 

|**Thuộc tính**|**Nội dung chi tiết**|
|---|---|
|**Tênphương thức**|+ cancelBooking(): void|
|**Mục đích**|Hủylựa chọn trước khi xác nhận.|
|**Tham số đầu vào**<br>**(@param)**|Không có.|
|**Giá trị trả về(@return)**|void – Khôngtrả vềgiá trị.|
|**Ngoại lệ (@exception)**|Không.|
|**Tiền điều kiện (Pre-**<br>**conditions)**|Yêu cầu chưa được gửi để lưu.|
|**Hậu điều kiện (Post-**<br>**conditions)**|Đóng hộp thoại; không tạo hay hủy đơn đã lưu.|



|**Thuộc tính**|**Nội dung chi tiết**|
|---|---|
|**Luồng thuật toán**|1. Xóa lựa chọn tạm.<br>|
|**(Pseudo-code)**|2. Đónghộpthoại và trở về màn hình trước.|



### **_1.3.3. BookingController.bookVehicle()_** 

|**Thuộc tính**|**Nội dung chi tiết**|
|---|---|
|**Tên phương thức**|+ bookVehicle(sessionId: String, request: BookingRequest):<br>Booking|
|**Mục đích**|Kiểm tra và lưu đơn đặt xe.|
|**Tham số đầu vào**<br>**(@param)**|sessionId: String – mã phiên đăng nhập.<br>request: BookingRequest – dữ liệu yêu cầu đặt chỗ, gồm tài nguyên,<br>Hub, thờigian và mãyêu cầu để đối soát khi thử lại.|
|**Giá trị trả về(@return)**|Booking– Đơn đặt chỗ sau khi xử lý.|
|**Ngoại lệ (@exception)**|AuthenticationRequired: chưa xác thực;<br>BookingConflict: xe không khả dụng;<br>StorageError: lỗi lưu hoặc chưa xác định kếtquả.|
|**Tiền điều kiện (Pre-**<br>**conditions)**|Có yêu cầu đặt xe; người dùng có phiên sinh viên hợp lệ.|
|**Hậu điều kiện (Post-**<br>**conditions)**|Tạo đơn CONFIRMED, giữ xe RESERVED và ghi lịch sử cùng<br>giao dịch.|
|**Luồng thuật toán**<br>**(Pseudo-code)**|1. Kiểm tra phiên bằng Session.isValid và quyền bằng User.hasRole;<br>kiểm tra và quyền sinh viên. Nếu hết phiên, giữ lựa chọn tạm và yêu<br>cầu SSO; xóa lựa chọn nếu xác thực thất bại hoặc bị hủy.<br>2. Khóa xe và gọi Vehicle.isAvailable và kiểm tra lại trạng thái khả<br>dụng, Hub và sự cố.<br>3. Trong cùng giao dịch, tạo đơn, giữ xe và ghi AuditLog; nếu lỗi<br>trước commit thì hoàn tác.<br>4. Nếu mất phản hồi, đối soát requestId trước khi thử lại.<br>5. Trả đơn đã lưu vàgửi thôngbáo xác nhận khi cần.|



### **_1.3.4. BookingController.bookParking()_** 

|**Thuộc tính**|**Nội dung chi tiết**|
|---|---|
|**Tên phương thức**|+ bookParking(sessionId: String, request: BookingRequest):<br>Booking|
|**Mục đích**|Kiểm tra và lưu đơngiữ chỗ đỗ.|
|**Tham số đầu vào**<br>**(@param)**|sessionId: String – mã phiên đăng nhập.<br>request: BookingRequest – dữ liệu yêu cầu đặt chỗ, gồm tài nguyên,<br>Hub, thờigian và mãyêu cầu để đối soát khi thử lại.|
|**Giá trị trả về(@return)**|Booking– Đơn đặt chỗ sau khi xử lý.|
|**Ngoại lệ (@exception)**|AuthenticationRequired;<br>ValidationError;<br>BookingConflict: chỗ đỗ không còn phù hợp;<br>StorageError.|
|**Tiền điều kiện (Pre-**<br>**conditions)**|Sinh viên đã đăng nhập và chọn Hub, chỗ đỗ, khoảng thời gian.|
|**Hậu điều kiện (Post-**<br>**conditions)**|Lưu đơn và khoảng giữ chỗ không trùng; ghi AuditLog.|



|**Thuộc tính**|**Nội dung chi tiết**|
|---|---|
|**Luồng thuật toán**<br>**(Pseudo-code)**|1. Kiểm tra phiên bằng Session.isValid và quyền bằng User.hasRole;<br>kiểm tra, quyền và dữ liệu; thời điểm kết thúc phải sau bắt đầu.<br>2. Khóa chỗ đỗ và kiểm tra lại Hub, khả dụng và các khoảng giữ đã<br>lưu.<br>3. Nếu có khoảng giao nhau, từ chối yêu cầu.<br>4. Lưu đơn, giữ khoảng thời gian và ghi lịch sử trong cùng giao dịch.<br>5. Nếu lỗi, hoàn tác hoặc đối soát requestId khi chưa rõ kết quả; trả<br>thôngbáophù hợp.|



### **_1.3.5. ActiveRideScreen.confirmPickup()_** 

|**Thuộc tính**|**Nội dung chi tiết**|
|---|---|
|**Tên phương thức**|+ confirmPickup(sessionId: String, bookingId: String, hubId:<br>String): Booking|
|**Mục đích**|Tiếpnhận xác nhận nhận xe môphỏng.|
|**Tham số đầu vào**<br>**(@param)**|sessionId: String – mã phiên đăng nhập.<br>bookingId: String – mã đơn đặt xe.<br>hubId: String– mã Hub nhận xe.|
|**Giá trị trả về(@return)**|Booking– Đơn đặt chỗ sau khi xử lý.|
|**Ngoại lệ (@exception)**|AuthenticationRequired;<br>InvalidBooking;<br>ResourceUnavailable;<br>StorageError.|
|**Tiền điều kiện (Pre-**<br>**conditions)**|Người dùng đã chọn đơn xe và Hub nhận.|
|**Hậu điều kiện (Post-**<br>**conditions)**|Hiển thị kết quả nhận xe hoặc lỗi.|
|**Luồng thuật toán**<br>**(Pseudo-code)**|1. Gửi mã đơn và Hub đến TripController.<br>2. Chờ kết quả xác nhận.<br>3. Hiển thị thành công khi đơn chuyển PICKED_UP; nếu chưa hoàn<br>tất, thôngbáo liên hệ vận hành.|



### **_1.3.6. ActiveRideScreen.cancelPickup()_** 

|**Thuộc tính**|**Nội dung chi tiết**|
|---|---|
|**Tênphương thức**|+ cancelPickup(): void|
|**Mục đích**|Dừngnhận xe trước xác nhận.|
|**Tham số đầu vào**<br>**(@param)**|Không có.|
|**Giá trị trả về(@return)**|void – Khôngtrả vềgiá trị.|
|**Ngoại lệ (@exception)**|Không.|
|**Tiền điều kiện (Pre-**<br>**conditions)**|Chưa gửi xác nhận nhận xe.|
|**Hậu điều kiện (Post-**<br>**conditions)**|Đơn đặt xe và trạng thái xe không đổi.|
|**Luồng thuật toán**<br>**(Pseudo-code)**|1. Đóng màn hình xác nhận.<br>2. Trở về danh sách đơn đặt xe.|



### **_1.3.7. TripController.confirmPickup()_** 

|**Thuộc tính**|**Nội dung chi tiết**|
|---|---|
|**Tên phương thức**|+ confirmPickup(sessionId: String, bookingId: String, hubId:<br>String): Booking|
|**Mục đích**|Xác minh vàghi nhận việc nhận xe môphỏng.|
|**Tham số đầu vào**<br>**(@param)**|sessionId: String – mã phiên đăng nhập.<br>bookingId: String – mã đơn đặt xe.<br>hubId: String– mã Hub nhận xe.|
|**Giá trị trả về(@return)**|Booking– Đơn đặt chỗ sau khi xử lý.|
|**Ngoại lệ (@exception)**|AuthenticationRequired;<br>InvalidBooking: sai chủ đơn, Hub hoặc hết hạn;<br>ResourceUnavailable: xe có sự cố;<br>StorageError.|
|**Tiền điều kiện (Pre-**<br>**conditions)**|Có phiên sinh viên và đơn đặt xe.|
|**Hậu điều kiện (Post-**<br>**conditions)**|Thành công: xe IN_USE, đơn PICKED_UP, lưu người và thời gian<br>nhận.|
|**Luồng thuật toán**<br>**(Pseudo-code)**|1. Kiểm tra phiên bằng Session.isValid và quyền bằng User.hasRole;<br>kiểm tra, chủ đơn, hiệu lực đặt xe bằng Booking.isValid, Hub và tình<br>trạng xe dưới khóa.<br>2. Ghi nhận thao tác mô phỏng và chặn đặt lại xe.<br>3. Cập nhật xe, đơn và AuditLog; trả đơn khi hoàn tất.<br>4. Nếu lỗi sau khi ghi nhận, giữ thông tin nhận và chặn đặt lại,<br>chuyển vận hành kiểm tra; không báo thành công.<br>5. Khi gửi lại yêu cầu, kiểm tra kết quả đã lưu để không nhận xe hai<br>lần.|



### **_1.3.8. LoginScreen.login()_** 

|**Thuộc tính**|**Nội dung chi tiết**|
|---|---|
|**Tênphương thức**|+ login(returnTarget: String): String|
|**Mục đích**|Mở trangđăngnhậpSSO.|
|**Tham số đầu vào**<br>**(@param)**|returnTarget: String – vị trí nội bộ trở về sau đăng nhập.|
|**Giá trị trả về(@return)**|String– URL đăngnhậpSSO.|
|**Ngoại lệ (@exception)**|SsoUnavailable: khôngkết nối được SSO.|
|**Tiền điều kiện (Pre-**<br>**conditions)**|Người dùng chọn đăng nhập hoặc cần xác thực để đặt xe.|
|**Hậu điều kiện (Post-**<br>**conditions)**|Trình duyệt chuyển đến SSO.|
|**Luồng thuật toán**<br>**(Pseudo-code)**|1. Lưu vị trí cần trở về.<br>2. Lấy URL đăng nhập từ cấu hình SSO.<br>3. Chuyển người dùng sang SSO để nhập thông tin; không lưu mật<br>khẩu tại Hub.|



### **_1.3.9. LoginScreen.completeLogin()_** 

|**Thuộc tính**|**Nội dung chi tiết**|
|---|---|
|**Tênphương thức**|+ completeLogin(credential: String): Session|
|**Mục đích**|Tiếpnhận kếtquả SSO và hiển thịgiao diệnphù hợp.|
|**Tham số đầu vào**<br>**(@param)**|credential: String – kết quả xác thực do SSO trả về.|
|**Giá trị trả về(@return)**|Session – Phiên đăngnhậphợplệ.|
|**Ngoại lệ (@exception)**|AuthenticationFailed;<br>AccessDenied;<br>SsoUnavailable;<br>StorageError.|
|**Tiền điều kiện (Pre-**<br>**conditions)**|SSO trả kết quả xác thực.|
|**Hậu điều kiện (Post-**<br>**conditions)**|Có phiên hợp lệ hoặc thông báo lỗi.|
|**Luồng thuật toán**<br>**(Pseudo-code)**|1. Gửi kết quả SSO đến AuthController.<br>2. Khi thành công, trở về chức năng đang dùng hoặc trang theo vai<br>trò.<br>3. Khi thất bại, báo lỗi; nếu người dùng hủy thì về trang chủ và xóa<br>lựa chọn tạm.|



### **_1.3.10. AuthController.authenticate()_** 

|**Thuộc tính**|**Nội dung chi tiết**|
|---|---|
|**Tênphương thức**|+ authenticate(credential: String): Session|
|**Mục đích**|Xác minh kếtquả SSO và tạophiên người dùng.|
|**Tham số đầu vào**<br>**(@param)**|credential: String – kết quả xác thực do SSO trả về.|
|**Giá trị trả về(@return)**|Session – Phiên đăngnhậphợplệ.|
|**Ngoại lệ (@exception)**|AuthenticationFailed: SSO từ chối hoặc kết quả không hợp lệ;<br>AccessDenied: thiếu quyền;<br>SsoUnavailable;<br>StorageError.|
|**Tiền điều kiện (Pre-**<br>**conditions)**|Nhận kết quả từ luồng SSO hợp lệ.|
|**Hậu điều kiện (Post-**<br>**conditions)**|Tạo phiên gắn người dùng và quyền; ghi lịch sử đăng nhập.|
|**Luồng thuật toán**<br>**(Pseudo-code)**|1. Xác minh kết quả với SSO, bao gồm nguồn trả về và hiệu lực.<br>2. Tìm tài khoản Hub tương ứng và kiểm tra quyền STUDENT hoặc<br>OPERATOR.<br>3. Tạo và lưu phiên cùng lịch sử đăng nhập.<br>4. Trả phiên; nếu bị từ chối, hết thời gian chờ hoặc lỗi lưu thì không<br>cấp phiên mới.|



### **_1.3.11. Booking.isValid()_** 

|**Thuộc tính**|**Nội dung chi tiết**|
|---|---|
|**Tênphương thức**|+ isValid(now: DateTime): Boolean|
|**Mục đích**|Kiểm tra đơn còn hiệu lực.|
|**Tham số đầu vào**<br>**(@param)**|now: DateTime – Thời gian máy chủ.|
|**Giá trị trả về(@return)**|Boolean – true khi thỏa điều kiện; false khi khôngthỏa.|
|**Ngoại lệ (@exception)**|Không.|
|**Tiền điều kiện (Pre-**<br>**conditions)**|Đơn được đọc từ dữ liệu hiện tại.|
|**Hậu điều kiện (Post-**<br>**conditions)**|Trả true khi đơn đã xác nhận và thời gian hiện tại còn trong khoảng<br>hiệu lực.|
|**Luồng thuật toán**<br>**(Pseudo-code)**|1. Kiểm tra trạng thái đơn đã xác nhận.<br>2. So sánh thời gian hiện tại với thời gian bắt đầu và kết thúc.<br>3. Trả true nếu hợplệ, ngược lại trả false.|



### **_1.3.12. Vehicle.isAvailable()_** 

|**Thuộc tính**|**Nội dung chi tiết**|
|---|---|
|**Tênphương thức**|+ isAvailable(): Boolean|
|**Mục đích**|Kiểm tra xe có thể được đặt.|
|**Tham số đầu vào**<br>**(@param)**|Không có.|
|**Giá trị trả về(@return)**|Boolean – true khi thỏa điều kiện; false khi khôngthỏa.|
|**Ngoại lệ (@exception)**|Không.|
|**Tiền điều kiện (Pre-**<br>**conditions)**|Trạng thái xe đã được cập nhật; kiểm tra dưới khóa khi lưu đơn.|
|**Hậu điều kiện (Post-**<br>**conditions)**|Không thay đổi dữ liệu xe.|
|**Luồng thuật toán**<br>**(Pseudo-code)**|1. Kiểm tra trạng thái xe là AVAILABLE và xe không bị chặn đặt.<br>2. Trả true nếu thỏa mãn, ngược lại trả false.|



### **_1.3.13. Session.isValid()_** 

|**Thuộc tính**|**Nội dung chi tiết**|
|---|---|
|**Tênphương thức**|+ isValid(now: DateTime): Boolean|
|**Mục đích**|Kiểm tra thời hạnphiên.|
|**Tham số đầu vào**<br>**(@param)**|now: DateTime – Thời gian máy chủ.|
|**Giá trị trả về(@return)**|Boolean – true khi thỏa điều kiện; false khi khôngthỏa.|
|**Ngoại lệ (@exception)**|Không.|
|**Tiền điều kiện (Pre-**<br>**conditions)**|Phiên tồn tại; dùng thời gian máy chủ.|
|**Hậu điều kiện (Post-**<br>**conditions)**|Không thay đổi phiên.|



|**Thuộc tính**|**Nội dung chi tiết**|
|---|---|
|**Luồng thuật toán**|1. So sánh thời gian hiện tại với expiresAt.|
|**(Pseudo-code)**|2. Trả true nếu chưa đến thời điểm hết hạn; ngược lại trả false.|



### **_1.3.14. User.hasRole()_** 

|**Thuộc tính**|**Nội dung chi tiết**|
|---|---|
|**Tênphương thức**|+ hasRole(requiredRole: String): Boolean|
|**Mục đích**|Kiểm tra vai trò cần thiết.|
|**Tham số đầu vào**<br>**(@param)**|requiredRole: String – Vai trò cần kiểm tra.|
|**Giá trị trả về(@return)**|Boolean – true khi thỏa điều kiện; false khi khôngthỏa.|
|**Ngoại lệ (@exception)**|Không.|
|**Tiền điều kiện (Pre-**<br>**conditions)**|Thông tin vai trò lấy từ hệ thống, không lấy từ dữ liệu tự khai của<br>giao diện.|
|**Hậu điều kiện (Post-**<br>**conditions)**|Không thay đổi quyền.|
|**Luồng thuật toán**<br>**(Pseudo-code)**|1. Đối chiếu role với vai trò yêu cầu.<br>2. Trả true nếuphù hợp, ngược lại trả false.|



## **1.4. Use Case UC6 - Trả phương tiện** 

### **_1.4.1. returnVehicle()_** 

|**Thuộc tính**|**Nội dung chi tiết**|
|---|---|
|**Tênphương thức**|returnVehicle|
|**Mục đích**|Thực hiện giao dịch trả phương tiện: kiểm tra hợp lệ, ghi audit log,<br>kết thúc lượt mượn, cậpnhật trạngthái xe vàgửi xác nhận.|
|**Tham số đầu vào**<br>**(@param)**|studentId: string, mã định danh sinh viên trả xe.<br>vehicleId: string, mã định danh phương tiện được trả.<br>hubId: string, mã định danh Hub nơi được trảphươngtiện.|
|**Giá trị trả về (@return)**|ReturnRecord: lớp thực thể lưu bản ghi trả xe, bao gồm mã bản ghi<br>thuê và trả xe, sinh viên, phương tiện, mã Hub nhận phương tiện trả<br>về, thờigian trả và trạngthái củaphươngtiện sau khi trả.|
|**Ngoại lệ (@exception)**|InvalidReturnException: không nhận diện được xe hoặc lượt mượn,<br>hoặc Hub không thể tiếp nhận.<br>ReturnRecordException: lỗi kết nối hoặc lưu, giao dịch bị hủy. Lỗi<br>gửi thôngbáo khôngném ngoại lệ.|
|**Tiền điều kiện (Pre-**<br>**conditions)**|Sinh viên có phiên đăng nhập hợp lệ và đang sử dụng phương tiện.<br>Phương tiện phải có RentalRecord và đang trong trạng thái IN_USE.<br>Hub nhận có khả năng tiếp nhận (hasCapacityFor trả về True) hoặc<br>sinh viên đã đặt chỗ đỗ.|
|**Hậu điều kiện (Post-**<br>**conditions)**|Một bản ghi ReturnRecord và AuditLog được tạo.<br>RentalRecord.status = ENDED; Vehicle.status thuộc<br>{‘AVAILABLE’, ‘WAITING_CHARGE’, ‘MAINTENANCE’},<br>Vehicle.currentHubId = hubId.|



|**Thuộc tính**|**Nội dung chi tiết**|
|---|---|
|**Luồng thuật toán**<br>**(Pseudo-code)**|rental = validateReturn(studentId, vehicleId);<br>if (!canHubAcceptReturn)<br>throw InvalidReturnException;<br>writeAuditLog(...);<br>rental.endRental(now);<br>status = determineVehicleStatus(vehicleId);<br>vehicle.updateStatus(status);<br>record = new ReturnRecord(...);<br>if(!canCreateReturnRecord)<br>throw ReturnRecordException;<br>if(!ReturnRecordException){<br>try { NotificationService.sendNotification(...) };<br>catch { logError() };<br>}<br>return record;|



## **1.5. Use Case UC7 - Đăng ký sạc** 

### **_1.5.1. registerCharging()_** 

|**Thuộc tính**|**Nội dung chi tiết**|
|---|---|
|**Tênphương thức**|registerCharging|
|**Mục đích**|Thực hiện giao dịch đăng ký chỗ sạc: kiểm tra khung giờ, tạo bản<br>ghi đăngký,giữ cổngsạc, lưu AuditLog.|
|**Tham số đầu vào**<br>**(@param)**|studentId: string, mã sinh viên.<br>vehicleId: string, mã phương tiện đang sử dụng.<br>portId: string, mã cổng sạc muốn mượn.<br>startTime: LocalDateTime, thời gian đăng ký bắt đầu sạc.<br>endTime: LocalDateTime, thờigian đăngkýkết thúc sạc.|
|**Giá trị trả về (@return)**|ChargingRegistration: lớp bản ghi đăng ký sạc, bao gồm thông tin<br>đầu vào, mã định danh bản đăng ký, trạng thái đăng ký để ở<br>CONFIRMED và thờigian tạo bản đăngký.|
|**Ngoại lệ (@exception)**|IllegalArgumentException: end không sau start.<br>SlotConflictException: khung giờ vừa được người khác đặt.<br>RegistrationSaveException: khônglưu được đăngký.|
|**Tiền điều kiện (Pre-**<br>**conditions)**|Sinh viên có phiên đăng nhập hợp lệ.<br>Phương tiện đang có trạng thái sử dụng bởi sinh viên<br>Cổngsạc tồn tại và khôngở trạngthái FAULTY.|
|**Hậu điều kiện (Post-**<br>**conditions)**|Bản ghi ChargingRegistration và AuditLog được tạo.<br>Cổng được giữ trong khung giờ đã chọn.<br>Yêu cầu thông báo được tạo.<br>Thất bại: mọi thay đổi tạm thời bị hủy, không có đăng ký nào được<br>tạo.|



|**Thuộc tính**|**Nội dung chi tiết**|
|---|---|
|**Luồng thuật toán**<br>**(Pseudo-code)**|if (end <= start)<br>throw IllegalArgumentException;<br>if (!port.isAvailableDuring(start, end))<br>throw SlotConflictException;<br>reg = new ChargingRegistration(...);<br>port.reserve();<br>writeAuditLog(...);<br>return reg;|



## **1.6. Use Case UC8 - Giám sát mạng lưới Mobility Hub** 

### **_1.6.1. getNetworkOverview()_** 

|**Thuộc tính**|**Nội dung chi tiết**|
|---|---|
|**Tênphương thức**|getNetworkOverview()|
|**Mục đích**|Cung cấp cho Đơn vị vận hành cái nhìn tổng quan, gần thời gian<br>thực về toàn bộ mạng lưới Mobility Hub để quyết định có cần theo<br>dõi chi tiết hoặc điềuphối.|
|**Tham số đầu vào**<br>**(@param)**|filter: OverviewFilter (nullable) - lọc theo khu vực/trạng thái hoạt<br>động/mức độ sử dụng (AF1).|
|**Giá trị trả về (@return)**|NetworkOverviewDTO - số Hub hoạt động, số phương tiện/chỗ<br>đỗ/cổng sạc khả dụng, mức độ sử dụng từng Hub, thời điểm cập nhật<br>gần nhất.|
|**Ngoại lệ (@exception)**|UnauthorizedException (EX1); DataSourceUnavailableException<br>(EX2).|
|**Tiền điều kiện (Pre-**<br>**conditions)**|Người dùng đã xác thực qua SSO với vai trò Đơn vị vận hành; các<br>Hub đã được cấu hình.|
|**Hậu điều kiện (Post-**<br>**conditions)**|Trả về dashboard tổng quan; Hub/tài nguyên dữ liệu chưa xác định<br>được đánh dấu riêng (EX3); khôngthayđổi dữ liệu vận hành.|
|**Luồng thuật toán**<br>**(Pseudo-code)**|function getNetworkOverview(filter):<br>if !session.valid OR session.role != OPERATOR:<br>throw UnauthorizedException<br>try:<br>hubs = dataAccess.getAllHubsWithLatestState()<br>catch DataAccessError:<br>throw DataSourceUnavailableException<br>if filter != null: hubs = applyFilter(hubs, filter)<br>for hub in hubs:<br>if hub.config invalid:<br>mark hub "needs review", skip usage calc<br>else:<br>hub.usageRate = computeUsage(hub)<br>return buildOverviewDTO(hubs)|



### **_1.6.2. validateOperatorAccess()_** 

|**Thuộc tính**|**Nội dung chi tiết**|
|---|---|
|**Tênphương thức**|validateOperatorAccess()|
|**Mục đích**|Kiểm tra phiên làm việc còn hiệu lực và người dùng có vai trò Đơn<br>vị vận hành trước khi cho phép truy cập dashboard (bước 2 của<br>UC8; NFR10).|
|**Tham số đầu vào**<br>**(@param)**|session: UserSession - phiên đăng nhập hiện tại lấy từ SSO.|
|**Giá trị trả về(@return)**|void - kết thúc bình thườngnghĩa là đượcphéptruycập.|
|**Ngoại lệ (@exception)**|UnauthorizedException (EX1) - phiên hết hạn, không tồn tại, hoặc<br>vai trò không phải OPERATOR.|
|**Tiền điều kiện (Pre-**<br>**conditions)**|Người dùng đã gửi yêu cầu mở chức năng giám sát.|
|**Hậu điều kiện (Post-**<br>**conditions)**|Nếu bị từ chối, không có dữ liệu giám sát nào được truy xuất; lần<br>truycậpbị từ chối đượcghi vào AuditLog (NFR11).|
|**Luồng thuật toán**<br>**(Pseudo-code)**|function validateOperatorAccess(session):<br>if session == null OR session.isExpired():<br>auditLog.record("ACCESS_DENIED", session)<br>throw UnauthorizedException<br>if session.role != OPERATOR:<br>auditLog.record("ACCESS_DENIED", session)<br>throw UnauthorizedException|



### **_1.6.3. applyOverviewFilter()_** 

|**Thuộc tính**|**Nội dung chi tiết**|
|---|---|
|**Tênphương thức**|applyOverviewFilter()|
|**Mục đích**|Lọc danh sách Hub trên dashboard theo khu vực, trạng thái hoạt<br>động hoặc mức độ sử dụng (AF1 của UC8); hỗ trợ trường hợp không<br>có Hubphù hợp (AF5).|
|**Tham số đầu vào**<br>**(@param)**|hubs: List<HubOverview> - danh sách Hub đã tổng hợp; filter:<br>OverviewFilter - gồm area: String (nullable), operationStatus:<br>HubStatus(nullable), minUsageRate: double(nullable).|
|**Giá trị trả về (@return)**|List<HubOverview> - danh sách Hub thoả bộ lọc; danh sách rỗng<br>nếu khôngcó Hubphù hợp (AF5).|
|**Ngoại lệ (@exception)**|Khôngcó.|
|**Tiền điều kiện (Pre-**<br>**conditions)**|Dashboard đã tải dữ liệu thành công (bước 5).|
|**Hậu điều kiện (Post-**<br>**conditions)**|Bộ lọc được giữ nguyên trên giao diện để Đơn vị vận hành điều<br>chỉnh hoặc xoá; khôngthayđổi dữ liệu vận hành.|



|**Thuộc tính**|**Nội dung chi tiết**|
|---|---|
|**Luồng thuật toán**<br>**(Pseudo-code)**|function applyOverviewFilter(hubs, filter):<br>result = hubs<br>if filter.area != null:<br>result = filter(result, hub.area == filter.area)<br>if filter.operationStatus != null:<br>result = filter(result,<br>hub.status == filter.operationStatus)<br>if filter.minUsageRate != null:<br>result = filter(result,<br>hub.usageRate >= filter.minUsageRate)<br>return result     // rỗng->giao diện báo AF5|



### **_1.6.4. computeHubUsage()_** 

|**Thuộc tính**|**Nội dung chi tiết**|
|---|---|
|**Tênphương thức**|computeHubUsage()|
|**Mục đích**|Tính mức độ sử dụng và trạng thái hoạt động của từng Hub (bước 4<br>của UC8); xử lý Hub có cấu hình không hợp lệ (EX4) và Hub mất<br>kết nối hoặc dữ liệuquá cũ(EX3, NFR05).|
|**Tham số đầu vào**<br>**(@param)**|hub: MobilityHub - Hub kèm trạng thái mới nhất của phương tiện,<br>chỗ đỗ và cổngsạc.|
|**Giá trị trả về (@return)**|HubOverview - gồm usageRate, availableVehicles, emptySpots,<br>availablePorts và cờ trạng thái dữ liệu (OK / NEEDS_REVIEW /<br>UNKNOWN).|
|**Ngoại lệ (@exception)**|Không ném ngoại lệ ra ngoài: Hub lỗi được đánh dấu để không làm<br>gián đoạn các Hub còn lại(NFR05).|
|**Tiền điều kiện (Pre-**<br>**conditions)**|Dữ liệu Hub đã được truy xuất (bước 3).|
|**Hậu điều kiện (Post-**<br>**conditions)**|Hub lỗi cấu hình được đánh dấu NEEDS_REVIEW và không tham<br>gia tính tổng; Hub mất kết nối được đánh dấu UNKNOWN, hiển thị<br>dữ liệugần nhất.|
||function computeHubUsage(hub):<br>overview = new HubOverview(hub.id, hub.name)<br>if hub.capacity == null OR hub.capacity <= 0:   // EX4<br>overview.dataFlag = NEEDS_REVIEW<br>return overview<br>if isStatusStale(hub.lastUpdatedAt):             // EX3<br>overview.dataFlag = UNKNOWN<br>|
|**Luồng thuật toán**<br>**(Pseudo-code)**|else:<br>overview.dataFlag = OK<br>overview.availableVehicles =<br>count(hub.vehicles, status==AVAILABLE)<br>overview.emptySpots = count(hub.parkingSpots, status==EMPTY)<br>overview.availablePorts =<br>count(hub.chargingPorts, status==AVAILABLE)<br>overview.usageRate =<br>(hub.capacity - overview.emptySpots) / hub.capacity<br>return overview|



## **1.7. Use Case UC9 - Theo dõi tài nguyên** 

### **_1.7.1. getResourceStatus()_** 

|**Thuộc tính**|**Nội dung chi tiết**|
|---|---|
|**Tênphương thức**|getResourceStatus|
|**Mục đích**|Truy xuất trạng thái tài nguyên của một Hub (số xe, chỗ đỗ, cổng sạc<br>khả dụng và danh sách từng tài nguyên) cùng thời điểm cập nhật;<br>đánh dấu dữ liệuquá cũ hoặc chưa xác định.|
|**Tham số đầu vào**<br>**(@param)**|hubId: string, mã hub cần được theo dõi|
|**Giá trị trả về (@return)**|HubResource: lớp bao gồm số tài nguyên khả dụng mỗi loại, thời<br>gian cậpnhật, và trạngthái dữ liệu.|
|**Ngoại lệ (@exception)**|HubNotFoundException: Hub không tồn tại.<br>DataUnavailableException: Dữ liệu tài nguyên khôngthể truyxuất.|
|**Tiền điều kiện (Pre-**<br>**conditions)**|UC8 đang chạy, người dùng có phiên hợp lệ với quyền Đơn vị vận<br>hành.<br>Hub có dữ liệu trạngthái hoặc có thể truyxuất.|
|**Hậu điều kiện (Post-**<br>**conditions)**|Trả về trạng thái hiện tại của Hub. Không có dữ liệu vận hành nào bị<br>thayđổi. Dòngcó lastUpdatedquá cũ được đánh dấu stale.|
|**Luồng thuật toán**<br>**(Pseudo-code)**|hub = hubRepo.find(hubId);<br>if(hub = null) throw HubNotFoundException;<br>items = resourceRepo.findByHub(hubId);<br>if(item=null) throw DataUnavailableException;<br>status = new HubResource(hub, items);<br>for(ResourceItem in HubResource.resources){<br>availableResourceItems = count(item.status == AVAILABLE for<br>each ResourceType);<br>status.lastUpdated = max(item.lastUpdated);<br>dataState = status.evaluateData(now);<br>return status;|



## **1.8. Use Case UC10 - Xem cảnh báo quá tải** 

### **_1.8.1. evaluateHubLoad()_** 

|**Thuộc tính**|**Nội dung chi tiết**|
|---|---|
|**Tênphương thức**|evaluateHubLoad|
|**Mục đích**|So sánh mức sử dụng từng loại tài nguyên (chỗ đỗ, cổng sạc) của<br>Hub với ngưỡng; tạo hoặc cập nhật cảnh báo quá tải với mức nguy<br>hiểm Medium / High.|
|**Tham số đầu vào**<br>**(@param)**|hubId: string, mã hub cần được đánh giá.|
|**Giá trị trả về(@return)**|List<OverloadAlert>, các cảnh báo đangACTIVE của Hub.|
|**Ngoại lệ (@exception)**|HubNotFoundException: Hub không tồn tại.<br>DataUnavailableException: Dữ liệu tài nguyên không thể truy xuất<br>hoặc ở trạngthái stale.|



|**Thuộc tính**|**Nội dung chi tiết**|
|---|---|
|**Tiền điều kiện (Pre-**<br>**conditions)**|UC8 đang chạy, người dùng có phiên hợp lệ với quyền Đơn vị vận<br>hành.<br>Hub tồn tại và HubResource có DataState = FRESH.<br>Đã có OverloadThreshold cho từngUtilizationType.|
|**Hậu điều kiện (Post-**<br>**conditions)**|Mỗi loại vượt ngưỡng có đúng một cảnh báo ACTIVE (không tạo<br>trùng). Cảnh báo có utilization, threshold, severity, expectedCause,<br>detectedAt. Yêu cầu thôngbáo đượcgửi khi cần ngoài ứngdụng.|
|**Luồng thuật toán**<br>**(Pseudo-code)**|hub = hubRepo.find(hubId);<br>if(hub=null) throw HubNotFoundException;<br>status = getResourceStatus(hubId);<br>if(status.dataState != FRESH) throw DataUnavailableException;<br>for(type in [PARKING_SPOT, CHARGING_PORT]){<br>rate = status.getUtilization(type);<br>t = thresholdRepo.find(type);<br>if(t.isExceeded(rate)){<br>existing = alertRepo.findActive(hubId, type);<br>if(existing = null){<br>existing = new OverloadAlert( hubId, type, rate,<br>t.threshold, t.classify(rate), now);<br>notifyOperator(alert);<br>} else existing.update(rate, t.classify(rate));<br>return alertRepo.findActiveByHub(hubId);|



## **1.9. Use Case UC11 – Điều phối phương tiện (Vehicle Dispatch)** 

### **_1.9.1. loadDispatchView()_** 

|**Thuộc tính**|**Nội dung chi tiết**|
|---|---|
|**Tênphương thức**|loadDispatchView()|
|**Mục đích**|Khởi tạo và hiển thị màn hình điều phối phương tiện, kiểm tra quyền<br>truy cập Đơn vị vận hành và tải bản đồ/bảng cân bằng trạng thái các<br>Hub.|
|**Tham số đầu vào**<br>**(@param)**|Không có.|
|**Giá trị trả về(@return)**|void – Khôngtrả vềgiá trị; cậpnhậtgiao diện màn hình điềuphối.|
|**Ngoại lệ (@exception)**|UnauthorizedException – Xảy ra khi người dùng không có vai trò<br>Operator (NFR10). DataSourceUnavailableException – Xảy ra khi<br>khôngthể tải danh sách Hub vàphươngtiện.|
|**Tiền điều kiện (Pre-**<br>**conditions)**|Người dùng đã xác thực qua SSO và chọn chức năng 'Điều phối<br>phươngtiện' trên Web Dashboard.|
|**Hậu điều kiện (Post-**<br>**conditions)**|Giao diện bản đồ/bảng cân bằng Hub và danh sách phương tiện khả<br>dụngtại Hub nguồn được hiển thị.|
|**Luồng thuật toán**<br>**(Pseudo-code)**|1. Gọi DispatchController.getDispatchHubData(null, null) để kiểm<br>tra quyền và tải trạng thái các Hub.<br>2. Nếu kiểm tra quyền thất bại -> gọi<br>displayDispatchFeedback("Không đủ quyền truy cập", true).<br>3. Nếu tải thành công -> hiển thị bản đồ mạng lưới Hub, danh sách<br>Hub nguồn/đích và chophépOperator thao tác.|



### **_1.9.2. prefillFromSimulation(sourceHubId, destHubId, vehicleIds)_** 

|**Thuộc tính**|**Nội dung chi tiết**|
|---|---|
|**Tênphương thức**|prefillFromSimulation(sourceHubId, destHubId, vehicleIds)|
|**Mục đích**|Tự động điền sẵn thông tin Hub nguồn, Hub đích và danh sách xe đề<br>xuất khi Đơn vị vận hành chuyển tiếp phương án từ mô phỏng What-<br>If(UC14 – AF1).|
|**Tham số đầu vào**<br>**(@param)**|sourceHubId: String – Mã Hub xuất phát được đề xuất.<br>destHubId: String – Mã Hub đích được đề xuất.<br>vehicleIds: List<String> – Danh sách mãphươngtiện cần điềuphối.|
|**Giá trị trả về(@return)**|void – Khôngtrả vềgiá trị.|
|**Ngoại lệ (@exception)**|InvalidArgumentException – Xảy ra khi tham số đề xuất từ UC14 bị<br>thiếu hoặc rỗng.|
|**Tiền điều kiện (Pre-**<br>**conditions)**|Đơn vị vận hành chọn 'Áp dụng vào thực tế' từ báo cáo mô phỏng<br>UC14 với đề xuất điềuphối xe.|
|**Hậu điều kiện (Post-**<br>**conditions)**|Các thuộc tính selectedSourceHubId, selectedDestHubId,<br>selectedVehicleIds được gán sẵn trên form để Operator kiểm tra<br>trước khi xác nhận.|
|**Luồng thuật toán**<br>**(Pseudo-code)**|1. Kiểm tra tính hợp lệ của sourceHubId, destHubId và vehicleIds.<br>2. Gán selectedSourceHubId = sourceHubId; selectedDestHubId =<br>destHubId; selectedVehicleIds = vehicleIds.<br>3. Gọi DispatchController.getDispatchHubData(sourceHubId,<br>destHubId) để nạp trạng thái thực tế mới nhất.<br>4. Hiển thị biểu mẫu đã điền sẵn để Operator rà soát hoặc chỉnh sửa.|



### **_1.9.3. submitDispatchOrder(sourceHubId, destHubId, vehicleIds)_** 

|**Thuộc tính**|**Nội dung chi tiết**|
|---|---|
|**Tênphương thức**|submitDispatchOrder(sourceHubId, destHubId, vehicleIds)|
|**Mục đích**|Tiếp nhận thao tác xác nhận lệnh điều phối của Đơn vị vận hành và<br>gửiyêu cầu xử lý giao dịch nguyên tử tới DispatchController.|
|**Tham số đầu vào**<br>**(@param)**|sourceHubId: String – Mã Hub nguồn.<br>destHubId: String – Mã Hub đích.<br>vehicleIds: List<String> – Danh sách mã các phương tiện được chọn<br>để điềuphối.|
|**Giá trị trả về(@return)**|void – Khôngtrả vềgiá trị.|
|**Ngoại lệ (@exception)**|VehicleConflictException – Xe đã bị Sinh viên đặt trước (EX1).<br>HubCapacityExceededException – Hub đích không đủ chỗ đỗ trống<br>(EX2).|
|**Tiền điều kiện (Pre-**<br>**conditions)**|Đơn vị vận hành đã chọn Hub nguồn, Hub đích hợp lệ và ít nhất một<br>phươngtiện khả dụng.|
|**Hậu điều kiện (Post-**<br>**conditions)**|Yêu cầu điều phối được xử lý; giao diện hiển thị kết quả thành công<br>hoặc cảnh báo xungđột/quá tải.|



|**Thuộc tính**|**Nội dung chi tiết**|
|---|---|
|**Luồng thuật toán**<br>**(Pseudo-code)**|1. Kiểm tra danh sách vehicleIds khác rỗng và sourceHubId !=<br>destHubId.<br>2. Gọi order =<br>DispatchController.processDispatch(currentOperatorId,<br>sourceHubId, destHubId, vehicleIds).<br>3. Nếu thành công -> gọi displayDispatchFeedback("Tạo lệnh điều<br>phối " + order.id + " thành công", false).<br>4. Nếu có ngoại lệ xung đột hoặc hết chỗ -> gọi<br>displayDispatchFeedback(err.message, true) và làm mới danh sách<br>xe/chỗ đỗ.|



### **_1.9.4. cancelPendingOrder(orderId)_** 

|**Thuộc tính**|**Nội dung chi tiết**|
|---|---|
|**Tênphương thức**|cancelPendingOrder(orderId)|
|**Mục đích**|Tiếp nhận yêu cầu hủy lệnh điều phối đang ở trạng thái chờ xử lý<br>trước khi vận chuyển(UC11 – AF2).|
|**Tham số đầu vào**<br>**(@param)**|orderId: String – Mã định danh lệnh điều phối cần hủy.|
|**Giá trị trả về(@return)**|void – Khôngtrả vềgiá trị.|
|**Ngoại lệ (@exception)**|InvalidStateException – Xảy ra khi lệnh điều phối không ở trạng thái<br>PENDING hoặc đã bắt đầu vận chuyển.|
|**Tiền điều kiện (Pre-**<br>**conditions)**|Đơn vị vận hành chọn một lệnh điều phối có trạng thái PENDING<br>và nhấn 'Hủylệnh'.|
|**Hậu điều kiện (Post-**<br>**conditions)**|Yêu cầu hủy được chuyển đến DispatchController; giao diện cập<br>nhật trạngthái lệnh và các xe liênquan.|
|**Luồng thuật toán**<br>**(Pseudo-code)**|1. Gọi result =<br>DispatchController.cancelDispatchOrder(currentOperatorId,<br>orderId).<br>2. Nếu result == true -> gọi displayDispatchFeedback("Đã hủy lệnh<br>điều phối " + orderId, false).<br>3. Nếu phát sinh lỗi -> gọi displayDispatchFeedback("Không thể<br>hủylệnh: " + err.message, true).|



### **_1.9.5. displayDispatchFeedback(message, isError)_** 

|**Thuộc tính**|**Nội dung chi tiết**|
|---|---|
|**Tênphương thức**|displayDispatchFeedback(message, isError)|
|**Mục đích**|Hiển thị thông báo kết quả tạo/hủy lệnh điều phối hoặc thông báo lỗi<br>(xungđột xe, Hub đích đầychỗ)lêngiao diện.|
|**Tham số đầu vào**<br>**(@param)**|message: String – Nội dung thông báo cần hiển thị.<br>isError: boolean – Cờ phân biệt thông báo lỗi (true) hay thành công<br>(false).|
|**Giá trị trả về(@return)**|void – Khôngtrả vềgiá trị.|
|**Ngoại lệ (@exception)**|Khôngcó.|
|**Tiền điều kiện (Pre-**<br>**conditions)**|Hệ thống đã hoàn tất xử lý nghiệp vụ hoặc bắt được ngoại lệ từ<br>DispatchController.|



|**Thuộc tính**|**Nội dung chi tiết**|
|---|---|
|**Hậu điều kiện (Post-**<br>**conditions)**|Thông báo rõ ràng được hiển thị tới Đơn vị vận hành trên màn hình<br>DispatchScreen.|
|**Luồng thuật toán**|1. Nếu isError == true -> hiển thị banner cảnh báo màu đỏ kèm<br>message và giữ nguyên lựa chọn hiện tại để thử lại.|
|**(Pseudo-code)**|2. Ngược lại -> hiển thị thông báo thành công màu xanh kèm<br>message và cậpnhật lại bảngdữ liệu Hub.|



### **_1.9.6. getDispatchHubData(sourceHubId, destHubId)_** 

|**Thuộc tính**|**Nội dung chi tiết**|
|---|---|
|**Tênphương thức**|getDispatchHubData(sourceHubId, destHubId)|
|**Mục đích**|Kiểm tra quyền Operator (NFR10) và truy xuất dữ liệu cân bằng<br>phươngtiện, mứcpin tại Hub nguồn và sức chứa trốngtại Hub đích.|
|**Tham số đầu vào**<br>**(@param)**|sourceHubId: String (nullable) – Mã Hub nguồn cần xem xe khả<br>dụng.<br>destHubId: String (nullable)– Mã Hub đích cần xem chỗ đỗ trống.|
|**Giá trị trả về (@return)**|DispatchHubDataDTO – Đối tượng tổng hợp danh sách Hub, các<br>SharedVehicle khả dụng kèm % pin tại Hub nguồn và availableSpots<br>của Hub đích.|
|**Ngoại lệ (@exception)**|UnauthorizedException – Người dùng không có quyền Operator.<br>HubNotFoundException – Khôngtìm thấyHub theo mã cungcấp.|
|**Tiền điều kiện (Pre-**<br>**conditions)**|Phiên làm việc SSO đang hoạt động; dữ liệu trạng thái các Hub đã<br>được đồngbộ từ UC16.|
|**Hậu điều kiện (Post-**<br>**conditions)**|Trả về dữ liệu chỉ đọc phục vụ hiển thị; không thay đổi trạng thái<br>phươngtiện hayHub.|
|**Luồng thuật toán**<br>**(Pseudo-code)**|1. Xác thực phiên SSO và vai trò OPERATOR; nếu không hợp lệ -><br>ném UnauthorizedException.<br>2. Nạp danh sách toàn bộ MobilityHub đang ở trạng thái ACTIVE.<br>3. Nếu sourceHubId != null -> truy vấn các SharedVehicle có<br>currentHubId == sourceHubId và status == AVAILABLE.<br>4. Nếu destHubId != null -> đọc availableSpots hiện tại của Hub<br>đích.<br>5. Đóng gói vào DispatchHubDataDTO và trả về.|



### **_1.9.7. processDispatch(operatorId, sourceHubId, destHubId, vehicleIds)_** 

|**Thuộc tính**|**Nội dung chi tiết**|
|---|---|
|**Tênphương thức**|processDispatch(operatorId, sourceHubId, destHubId, vehicleIds)|
|**Mục đích**|Thực thi quy trình điều phối phương tiện nguyên tử: khóa giao dịch<br>(NFR09), kiểm tra sức chứa Hub đích, chống race condition với đặt<br>xe của sinh viên, tạo DispatchOrder, ghi AuditLog (NFR11) và gửi<br>thôngbáo tới đội vận chuyển.|
|**Tham số đầu vào**<br>**(@param)**|operatorId: String – Mã định danh Đơn vị vận hành.<br>sourceHubId: String – Mã Hub xuất phát.<br>destHubId: String – Mã Hub đích.<br>vehicleIds: List<String> – Danh sách mã xe cần điềuphối.|
|**Giá trị trả về (@return)**|DispatchOrder – Bản ghi lệnh điều phối mới được tạo với trạng thái<br>PENDING.|



|**Thuộc tính**|**Nội dung chi tiết**|
|---|---|
|**Ngoại lệ (@exception)**|VehicleConflictException (EX1) – Một hoặc nhiều xe vừa được<br>Sinh viên đặt trước (status != AVAILABLE).<br>HubCapacityExceededException (EX2) – Hub đích không đủ chỗ đỗ<br>trống.<br>TransactionException – Lỗi khóa hoặc lưugiao dịch.|
|**Tiền điều kiện (Pre-**<br>**conditions)**|Đơn vị vận hành có quyền hợp lệ; sourceHubId != destHubId;<br>vehicleIds khôngrỗng.|
|**Hậu điều kiện (Post-**<br>**conditions)**|Thành công: Các xe chuyển sang DISPATCHING; sức chứa dự kiến<br>của Hub nguồn/đích được điều chỉnh; DispatchOrder và AuditLog<br>được lưu; NotificationService nhận yêu cầu gửi thông báo.<br>Thất bại: Rollback toàn bộ thayđổi, khôngkhóa xe nào.|
|**Luồng thuật toán**<br>**(Pseudo-code)**|1. Bắt đầu giao dịch nguyên tử (Transaction Lock với timeout =<br>LOCK_TIMEOUT_SECONDS).<br>2. Kiểm tra destHub.hasAvailableCapacity(vehicleIds.size()); nếu<br>false -> rollback và ném HubCapacityExceededException.<br>3. Với mỗi vId trong vehicleIds:<br>a. Khóa hàng bản ghi SharedVehicle(vId) (SELECT FOR<br>UPDATE).<br>b. Nếu !vehicle.isAvailable() hoặc vehicle.currentHubId !=<br>sourceHubId -> thêm vId vào conflictList.<br>4. Nếu conflictList không rỗng -> rollback giao dịch và ném<br>VehicleConflictException(conflictList).<br>5. Cập nhật từng SharedVehicle sang status = DISPATCHING; gọi<br>sourceHub.adjustExpectedCapacity(+count) và<br>destHub.adjustExpectedCapacity(-count).<br>6. Tạo DispatchOrder(operatorId, sourceHubId, destHubId,<br>vehicleIds, PENDING) và lưu CSDL.<br>7. Gọi AuditLog.record(operatorId, "CREATE_DISPATCH",<br>order.id, "Dispatch " + vehicleIds.size() + " vehicles").<br>8. Commit giao dịch.<br>9. Gọi NotificationService.sendNotification("FIELD_TEAM",<br>"Lệnh điều phối mới: " + order.id).<br>10. Trả về order.|



### **_1.9.8. cancelDispatchOrder(operatorId, orderId)_** 

|**Thuộc tính**|**Nội dung chi tiết**|
|---|---|
|**Tênphương thức**|cancelDispatchOrder(operatorId, orderId)|
|**Mục đích**|Hủy lệnh điều phối đang chờ xử lý, mở khóa và khôi phục trạng thái<br>các xe về AVAILABLE tại Hub nguồn, hoàn lại sức chứa dự kiến và<br>ghi AuditLog (UC11 – AF2).|
|**Tham số đầu vào**<br>**(@param)**|operatorId: String – Mã Đơn vị vận hành thực hiện hủy.<br>orderId: String– Mã lệnh điềuphối cần hủy.|
|**Giá trị trả về(@return)**|boolean – Trả về true nếu hủythành công.|
|**Ngoại lệ (@exception)**|ResourceNotFoundException – Không tìm thấy DispatchOrder.<br>InvalidStateException – Lệnh điều phối đã chuyển sang<br>IN_TRANSIT hoặc COMPLETED nên khôngthể hủy.|
|**Tiền điều kiện (Pre-**<br>**conditions)**|Đơn vị vận hành có quyền hợp lệ; DispatchOrder tồn tại và đang ở<br>trạngthái PENDING.|



|**Thuộc tính**|**Nội dung chi tiết**|
|---|---|
|**Hậu điều kiện (Post-**<br>**conditions)**|DispatchOrder.status = CANCELLED; các xe trong lệnh trở về trạng<br>thái AVAILABLE; sức chứa dự kiến của 2 Hub được hoàn tác;<br>AuditLogđượcghi nhận.|
|**Luồng thuật toán**<br>**(Pseudo-code)**|1. Bắt đầu giao dịch nguyên tử.<br>2. Tìm DispatchOrder theo orderId; nếu null -> ném<br>ResourceNotFoundException.<br>3. Nếu order.status != PENDING -> rollback và ném<br>InvalidStateException.<br>4. Gọi order.markCancelled().<br>5. Với mỗi vId trong order.vehicleIds: cập nhật<br>SharedVehicle.updateStatus(AVAILABLE, now()).<br>6. Hoàn tác sức chứa dự kiến: sourceHub.adjustExpectedCapacity(-<br>count); destHub.adjustExpectedCapacity(+count).<br>7. Gọi AuditLog.record(operatorId, "CANCEL_DISPATCH",<br>orderId, "Order cancelled before transit").<br>8. Commitgiao dịch và trả về true.|



### **_1.9.9. markCancelled()_** 

|**Thuộc tính**|**Nội dung chi tiết**|
|---|---|
|**Tênphương thức**|markCancelled()|
|**Mục đích**|Chuyển trạng thái của đối tượng lệnh điều phối sang CANCELLED<br>khi lệnh bị hủytrước khi vận chuyển.|
|**Tham số đầu vào**<br>**(@param)**|Không có.|
|**Giá trị trả về(@return)**|void – Khôngtrả vềgiá trị.|
|**Ngoại lệ (@exception)**|InvalidStateException – Xảyra nếu status hiện tại khác PENDING.|
|**Tiền điều kiện (Pre-**<br>**conditions)**|Đối tượng DispatchOrder đang ở trạng thái PENDING.|
|**Hậu điều kiện (Post-**<br>**conditions)**|Thuộc tính status được cập nhật thành<br>DispatchStatus.CANCELLED.|
|**Luồng thuật toán**<br>**(Pseudo-code)**|1. Nếu this.status != DispatchStatus.PENDING -> ném<br>InvalidStateException.<br>2. Gán this.status = DispatchStatus.CANCELLED.|



### **_1.9.10. markCompleted()_** 

|**Thuộc tính**|**Nội dung chi tiết**|
|---|---|
|**Tênphương thức**|markCompleted()|
|**Mục đích**|Đánh dấu lệnh điều phối đã hoàn tất sau khi đội vận chuyển đưa xe<br>đến Hub đích an toàn.|
|**Tham số đầu vào**<br>**(@param)**|Không có.|
|**Giá trị trả về(@return)**|void – Khôngtrả vềgiá trị.|
|**Ngoại lệ (@exception)**|InvalidStateException – Xảy ra nếu status hiện tại là CANCELLED<br>hoặc COMPLETED.|
|**Tiền điều kiện (Pre-**<br>**conditions)**|Đối tượng DispatchOrder đang ở trạng thái PENDING hoặc<br>IN_TRANSIT.|



|**Thuộc tính**|**Nội dung chi tiết**|
|---|---|
|**Hậu điều kiện (Post-**<br>**conditions)**|Thuộc tính status được cập nhật thành<br>DispatchStatus.COMPLETED.|
|**Luồng thuật toán**<br>**(Pseudo-code)**|1. Nếu this.status == CANCELLED hoặc this.status ==<br>COMPLETED -> ném InvalidStateException.<br>2. Gán this.status = DispatchStatus.COMPLETED.|



## **1.10. Use Case UC12 – Xử lý các sự cố (Incident Handling)** 

### **_1.10.1. displayIncidentList(incidents)_** 

|**Thuộc tính**|**Nội dung chi tiết**|
|---|---|
|**Tênphương thức**|displayIncidentList(incidents)|
|**Mục đích**|Hiển thị danh sách các sự cố mới ghi nhận kèm vị trí Hub, loại tài<br>nguyên, trạng thái và mức độ ưu tiên để Đơn vị vận hành lựa chọn<br>xử lý.|
|**Tham số đầu vào**<br>**(@param)**|incidents: List<Incident> – Danh sách sự cố đã được sắp xếp theo<br>mức độ ưu tiên.|
|**Giá trị trả về(@return)**|void – Khôngtrả vềgiá trị.|
|**Ngoại lệ (@exception)**|DisplayException – Xảy ra khi giao diện không thể render danh sách<br>sự cố.|
|**Tiền điều kiện (Pre-**<br>**conditions)**|Đơn vị vận hành mở chức năng Xử lý sự cố trên Web Dashboard.|
|**Hậu điều kiện (Post-**<br>**conditions)**|Danh sách sự cố hiển thị rõ ràng, phân biệt mức ưu tiên<br>(LOW/MEDIUM/HIGH/CRITICAL)và trạngthái.|
|**Luồng thuật toán**<br>**(Pseudo-code)**|1. Kiểm tra danh sách incidents; nếu rỗng -> hiển thị trạng thái<br>'Không có sự cố tồn đọng'.<br>2. Với mỗi Incident, hiển thị hubId, resourceId, type, priority, status<br>và reportedAt.<br>3. Gắn sự kiện chọn dòngđể mở chi tiết sự cố.|



### **_1.10.2. submitPauseResource(incidentId, reason, fixingMethod)_** 

|**Thuộc tính**|**Nội dung chi tiết**|
|---|---|
|**Tênphương thức**|submitPauseResource(incidentId, reason, fixingMethod)|
|**Mục đích**|Tiếp nhận thao tác chọn phương án 'Tạm ngưng hoạt động tài<br>nguyên' kèm mô tả nguyên nhân và hướng khắc phục từ Đơn vị vận<br>hành.|
|**Tham số đầu vào**<br>**(@param)**|incidentId: String – Mã sự cố cần xử lý.<br>reason: String – Mô tả nguyên nhân sự cố.<br>fixingMethod: String– Phươngán kỹthuật khắcphục.|
|**Giá trị trả về(@return)**|void – Khôngtrả vềgiá trị.|
|**Ngoại lệ (@exception)**|InvalidArgumentException – Xảy ra khi reason hoặc fixingMethod<br>rỗng.|
|**Tiền điều kiện (Pre-**<br>**conditions)**|Đơn vị vận hành đang xem chi tiết một sự cố có trạng thái<br>UNCHECKED hoặc IN_PROGRESS.|
|**Hậu điều kiện (Post-**<br>**conditions)**|Yêu cầu tạm ngưng tài nguyên được chuyển tới IncidentController<br>vàgiao diện cậpnhật kếtquả.|



|**Thuộc tính**|**Nội dung chi tiết**|
|---|---|
|**Luồng thuật toán**|1. Kiểm tra reason và fixingMethod không được để trống; nếu trống<br>-> gọi displayIncidentAlert("Vui lòng nhập nguyên nhân và hướng<br>khắc phục", HIGH) và dừng.<br>2. Gọi updated =|
|**(Pseudo-code)**|IncidentController.handlePauseResource(currentOperatorId,<br>incidentId, reason, fixingMethod).<br>3. Hiển thị thông báo 'Đã khóa tài nguyên và chuyển sang Bảo trì' và<br>làm mới chi tiết sự cố.|



### **_1.10.3. submitResolveIncident(incidentId)_** 

|**Thuộc tính**|**Nội dung chi tiết**|
|---|---|
|**Tênphương thức**|submitResolveIncident(incidentId)|
|**Mục đích**|Tiếp nhận thao tác nhấn 'Hoàn tất xử lý' sau khi đội kỹ thuật đã sửa<br>chữa xongtài nguyên bị sự cố(UC12 – AF1).|
|**Tham số đầu vào**<br>**(@param)**|incidentId: String – Mã sự cố đã khắc phục xong.|
|**Giá trị trả về(@return)**|void – Khôngtrả vềgiá trị.|
|**Ngoại lệ (@exception)**|InvalidStateException – Xảy ra khi sự cố chưa ở trạng thái<br>IN_PROGRESS.|
|**Tiền điều kiện (Pre-**<br>**conditions)**|Tài nguyên liên quan đang ở trạng thái MAINTENANCE và đội kỹ<br>thuật đã hoàn tất sửa chữa.|
|**Hậu điều kiện (Post-**<br>**conditions)**|Yêu cầu khôi phục tài nguyên được gửi tới IncidentController và<br>giao diện hiển thị xác nhận.|
|**Luồng thuật toán**<br>**(Pseudo-code)**|1. Gọi resolved =<br>IncidentController.completeIncident(currentOperatorId, incidentId).<br>2. Cập nhật giao diện hiển thị trạng thái sự cố RESOLVED và trạng<br>thái tài nguyên AVAILABLE.<br>3. Hiển thị thôngbáo 'Hoàn tất xử lýsự cố thành công'.|



### **_1.10.4. displayIncidentAlert(message, priority)_** 

|**Thuộc tính**|**Nội dung chi tiết**|
|---|---|
|**Tênphương thức**|displayIncidentAlert(message,priority)|
|**Mục đích**|Hiển thị cảnh báo sự cố khẩn cấp (đặc biệt khi một Hub mất kết nối<br>hoàn toàn – EX1)hoặc thôngbáo lỗi thao tác trêngiao diện.|
|**Tham số đầu vào**<br>**(@param)**|message: String – Nội dung cảnh báo.<br>priority: PriorityLevel – Mức độ nghiêm trọngcủa cảnh báo.|
|**Giá trị trả về(@return)**|void – Khôngtrả vềgiá trị.|
|**Ngoại lệ (@exception)**|Khôngcó.|
|**Tiền điều kiện (Pre-**<br>**conditions)**|Hệ thống phát hiện lỗi thao tác hoặc kích hoạt cơ chế cô lập Hub<br>(NFR05).|
|**Hậu điều kiện (Post-**<br>**conditions)**|Cảnh báo nổi bật đúng mức ưu tiên được hiển thị cho Đơn vị vận<br>hành.|
|**Luồng thuật toán**<br>**(Pseudo-code)**|1. Ánh xạ priority sang màu sắc/nhãn cảnh báo (CRITICAL/HIGH<br>-> đỏ, MEDIUM -> cam, LOW -> xanh).<br>2. Hiển thị hộpthoại/banner cảnh báo kèm nội dungmessage.|



### **_1.10.5. getPrioritizedIncidents()_** 

|**Thuộc tính**|**Nội dung chi tiết**|
|---|---|
|**Tênphương thức**|getPrioritizedIncidents()|
|**Mục đích**|Kiểm tra quyền Operator (NFR10) và truy xuất danh sách sự cố hiện<br>có, ưu tiên các sự cố CRITICAL (như mất kết nối toàn Hub) lên đầu<br>danh sách.|
|**Tham số đầu vào**<br>**(@param)**|Không có.|
|**Giá trị trả về (@return)**|List<Incident> – Danh sách các sự cố được sắp xếp theo mức độ ưu<br>tiêngiảm dần và thờigianphát hiện mới nhất.|
|**Ngoại lệ (@exception)**|UnauthorizedException – Người dùng không có quyền Operator.<br>DataSourceUnavailableException – Lỗi truyxuất CSDL.|
|**Tiền điều kiện (Pre-**<br>**conditions)**|Đơn vị vận hành đã đăng nhập hợp lệ qua SSO.|
|**Hậu điều kiện (Post-**<br>**conditions)**|Trả về danh sách sự cố đã sắp xếp; không làm thay đổi dữ liệu trạng<br>thái tài nguyên.|
|**Luồng thuật toán**<br>**(Pseudo-code)**|1. Kiểm tra quyền OPERATOR (NFR10); nếu không hợp lệ -> ném<br>UnauthorizedException.<br>2. Truy xuất các Incident từ kho dữ liệu.<br>3. Sắp xếp theo priority giảm dần (CRITICAL > HIGH > MEDIUM<br>> LOW), sau đó theo reportedAt giảm dần.<br>4. Trả về danh sách kếtquả.|



### **_1.10.6. handlePauseResource(operatorId, incidentId, reason, fixingMethod)_** 

|**Thuộc tính**|**Nội dung chi tiết**|
|---|---|
|**Tênphương thức**|handlePauseResource(operatorId, incidentId, reason, fixingMethod)|
|**Mục đích**|Khóa tài nguyên bị lỗi sang trạng thái MAINTENANCE, hủy tự<br>động các đơn đặt xe/lịch sạc đang hoạt động của Sinh viên liên quan<br>tới tài nguyên đó,gửi thôngbáo xin lỗi và lưu AuditLog (NFR11).|
|**Tham số đầu vào**<br>**(@param)**|operatorId: String – Mã Đơn vị vận hành.<br>incidentId: String – Mã sự cố.<br>reason: String – Nguyên nhân sự cố.<br>fixingMethod: String– Hướngkhắcphục.|
|**Giá trị trả về (@return)**|Incident – Bản ghi sự cố sau khi đã cập nhật sang trạng thái<br>IN_PROGRESS.|
|**Ngoại lệ (@exception)**|UnauthorizedException – Thiếu quyền Operator.<br>ResourceNotFoundException – Không tìm thấy Incident hoặc<br>Resource.<br>TransactionException – Lỗi cậpnhật nguyên tử.|
|**Tiền điều kiện (Pre-**<br>**conditions)**|Sự cố tồn tại; tài nguyên liên quan chưa ở trạng thái RESOLVED.|
|**Hậu điều kiện (Post-**<br>**conditions)**|Resource.status = MAINTENANCE (loại khỏi tìm kiếm/đặt chỗ);<br>các VehicleBooking hoặc ChargingRegistration đang hiệu lực bị<br>hủy; Sinh viên nhận thông báo; AuditLog được lưu tối thiểu 90 ngày<br>(AUDIT_RETENTION_DAYS).|



|**Thuộc tính**|**Nội dung chi tiết**|
|---|---|
||1. Xác thực quyền OPERATOR. Bắt đầu giao dịch nguyên tử.<br>2. Tìm Incident(incidentId) và Resource(incident.resourceId); nếu<br>null -> ném ResourceNotFoundException.<br>3. Gọi incident.pauseAndAssign(reason, fixingMethod).<br>4. Gọi resource.updateStatus(ResourceStatus.MAINTENANCE,<br>now()).<br>5. Kiểm tra các VehicleBooking đang ACTIVE cho resource.id -><br>gọi booking.cancelByIncident(incidentId) và lưu danh sách<br>studentId bị ảnh hưởng.|
|**Luồng thuật toán**<br>**(Pseudo-code)**|<br>6. Kiểm tra các ChargingRegistration đang CONFIRMED cho<br>resource.id -> gọi reg.cancelByIncident(incidentId) và lưu danh sách<br>studentId bị ảnh hưởng.<br>7. Gọi AuditLog.record(operatorId,<br>"PAUSE_RESOURCE_INCIDENT", resource.id, reason + " | " +<br>fixingMethod).<br>8. Commit giao dịch.<br>9. Với mỗi studentId bị ảnh hưởng -> gọi<br>NotificationService.sendNotification(studentId, "Lượt đặt bị hủy do<br>sự cố bảo trì tài nguyên").<br>10. Trả về incident.|



### **_1.10.7. completeIncident(operatorId, incidentId)_** 

|**Thuộc tính**|**Nội dung chi tiết**|
|---|---|
|**Tênphương thức**|completeIncident(operatorId, incidentId)|
|**Mục đích**|Xác nhận hoàn tất khắc phục sự cố, khôi phục trạng thái tài nguyên<br>từ MAINTENANCE về AVAILABLE và ghi AuditLog thời điểm<br>hoàn tất(UC12 – AF1).|
|**Tham số đầu vào**<br>**(@param)**|operatorId: String – Mã Đơn vị vận hành.<br>incidentId: String– Mã sự cố cần đóng.|
|**Giá trị trả về (@return)**|Incident – Bản ghi sự cố với trạng thái RESOLVED và resolvedAt<br>đã cậpnhật.|
|**Ngoại lệ (@exception)**|UnauthorizedException – Thiếu quyền Operator.<br>ResourceNotFoundException – Không tìm thấy sự cố.<br>InvalidStateException – Sự cố đã được đóngtrước đó.|
|**Tiền điều kiện (Pre-**<br>**conditions)**|Sự cố đang ở trạng thái IN_PROGRESS và tài nguyên đang ở trạng<br>thái MAINTENANCE.|
|**Hậu điều kiện (Post-**<br>**conditions)**|Incident.status = RESOLVED; Resource.status = AVAILABLE;<br>AuditLog ghi nhận thao tác khôiphục tài nguyên.|
|**Luồng thuật toán**<br>**(Pseudo-code)**|1. Xác thực quyền OPERATOR. Bắt đầu giao dịch.<br>2. Tìm Incident(incidentId) và Resource(incident.resourceId).<br>3. Nếu incident.status == RESOLVED -> ném<br>InvalidStateException.<br>4. Gọi incident.resolve().<br>5. Gọi resource.updateStatus(ResourceStatus.AVAILABLE, now()).<br>6. Gọi AuditLog.record(operatorId, "RESOLVE_INCIDENT",<br>resource.id, "Restored to AVAILABLE").<br>7. Commitgiao dịch và trả về incident.|



### **_1.10.8. isolateDisconnectedHub(hubId)_** 

|**Thuộc tính**|**Nội dung chi tiết**|
|---|---|
|**Tênphương thức**|isolateDisconnectedHub(hubId)|
|**Mục đích**|Kích hoạt kiến trúc cô lập lỗi (NFR05) khi phát hiện một Hub mất<br>kết nối hoàn toàn: tạm ngưng giao dịch riêng tại Hub đó, gán sự cố<br>mức CRITICAL và khônglàmgián đoạn các Hub khác.|
|**Tham số đầu vào**<br>**(@param)**|hubId: String – Mã MobilityHub bị mất kết nối.|
|**Giá trị trả về(@return)**|void – Khôngtrả vềgiá trị.|
|**Ngoại lệ (@exception)**|ResourceNotFoundException – Không tìm thấy MobilityHub theo<br>hubId.|
|**Tiền điều kiện (Pre-**<br>**conditions)**|Hệ thống giám sát/đồng bộ phát hiện Hub ngừng phản hồi quá<br>ngưỡng quyđịnh.|
|**Hậu điều kiện (Post-**<br>**conditions)**|MobilityHub.status = ISOLATED; một Incident mới với priority =<br>CRITICAL được tạo (nếu chưa có); các Hub khác vẫn hoạt động<br>bình thường; AuditLog ghi nhận sự kiện cô lập.|
|**Luồng thuật toán**<br>**(Pseudo-code)**|1. Tìm MobilityHub(hubId); nếu null -> ném<br>ResourceNotFoundException.<br>2. Gọi hub.isolateHub() (chỉ khóa giao dịch tại hubId, không chặn<br>luồng của các Hub khác).<br>3. Tạo Incident mới với type = "HUB_DISCONNECTED", priority<br>= CRITICAL, status = UNCHECKED.<br>4. Gọi AuditLog.record("SYSTEM", "ISOLATE_HUB", hubId,<br>"Fault isolation triggered (NFR05)").<br>5. Gọi<br>NotificationService.sendNotification("OPERATOR_ON_DUTY",<br>"Cảnh báo CRITICAL: Hub " + hubId + " mất kết nối và đã được cô<br>lập").|



### **_1.10.9. Incident.pauseAndAssign(reason, resolution)_** 

|**Thuộc tính**|**Nội dung chi tiết**|
|---|---|
|**Tênphương thức**|Incident.pauseAndAssign(reason, resolution)|
|**Mục đích**|Cập nhật nguyên nhân, hướng khắc phục và chuyển trạng thái sự cố<br>sangIN_PROGRESS.|
|**Tham số đầu vào**<br>**(@param)**|reason: String – Nguyên nhân gây ra sự cố.<br>resolution: String– Biệnphápkhắcphục.|
|**Giá trị trả về(@return)**|void – Khôngtrả vềgiá trị.|
|**Ngoại lệ (@exception)**|InvalidArgumentException – Khi reason hoặc resolution bị rỗng.|
|**Tiền điều kiện (Pre-**<br>**conditions)**|Incident chưa ở trạng thái RESOLVED.|
|**Hậu điều kiện (Post-**<br>**conditions)**|rootCause = reason; resolutionNote = resolution; status =<br>IncidentStatus.IN_PROGRESS.|
|**Luồng thuật toán**<br>**(Pseudo-code)**|1. Kiểm tra reason và resolution khác rỗng.<br>2. Gán this.rootCause = reason; this.resolutionNote = resolution.<br>3. Gán this.status = IncidentStatus.IN_PROGRESS.|



### **_1.10.10. Incident.resolve()_** 

|**Thuộc tính**|**Nội dung chi tiết**|
|---|---|
|**Tênphương thức**|Incident.resolve()|
|**Mục đích**|Đánh dấu sự cố đã được khắc phục hoàn toàn và ghi nhận mốc thời<br>giangiảiquyết.|
|**Tham số đầu vào**<br>**(@param)**|Không có.|
|**Giá trị trả về(@return)**|void – Khôngtrả vềgiá trị.|
|**Ngoại lệ (@exception)**|InvalidStateException – Nếu sự cố đã ở trạngthái RESOLVED.|
|**Tiền điều kiện (Pre-**<br>**conditions)**|Incident đang ở trạng thái IN_PROGRESS hoặc UNCHECKED.|
|**Hậu điều kiện (Post-**<br>**conditions)**|status = IncidentStatus.RESOLVED; resolvedAt = thời điểm hiện<br>tại.|
|**Luồng thuật toán**<br>**(Pseudo-code)**|1. Nếu this.status == IncidentStatus.RESOLVED -> ném<br>InvalidStateException.<br>2. Gán this.status = IncidentStatus.RESOLVED; this.resolvedAt =<br>now().|



### **_1.10.11. VehicleBooking.cancelByIncident(incidentId)_** 

|**Thuộc tính**|**Nội dung chi tiết**|
|---|---|
|**Tênphương thức**|VehicleBooking.cancelByIncident(incidentId)|
|**Mục đích**|Hủy tự động lượt đặt xe dùng chung của Sinh viên khi xe gặp sự cố<br>phải đưa vào bảo trì(UC12 – Bước 6).|
|**Tham số đầu vào**<br>**(@param)**|incidentId: String – Mã sự cố làm cơ sở hủy lượt đặt.|
|**Giá trị trả về (@return)**|boolean – Trả về true nếu lượt đặt đang hiệu lực được hủy thành<br>công, false nếu lượt đặt đã kết thúc trước đó.|
|**Ngoại lệ (@exception)**|Khôngcó.|
|**Tiền điều kiện (Pre-**<br>**conditions)**|Lượt đặt xe đang gắn với phương tiện bị tạm ngưng hoạt động.|
|**Hậu điều kiện (Post-**<br>**conditions)**|Nếu đang PENDING/CONFIRMED -> status chuyển sang<br>CANCELLED_BY_INCIDENT.|
|**Luồng thuật toán**<br>**(Pseudo-code)**|1. Nếu this.status không nằm trong {"PENDING", "CONFIRMED"}<br>-> trả về false.<br>2. Gán this.status = "CANCELLED_BY_INCIDENT".<br>3. Trả về true.|



### **_1.10.12. ChargingRegistration.cancelByIncident(incidentId)_** 

|**Thuộc tính**|**Nội dung chi tiết**|
|---|---|
|**Tênphương thức**|ChargingRegistration.cancelByIncident(incidentId)|
|**Mục đích**|Hủy tự động lịch đăng ký sạc của Sinh viên khi cổng sạc gặp sự cố<br>phải tạm ngưngbảo trì(UC12 – Bước 6).|
|**Tham số đầu vào**<br>**(@param)**|incidentId: String – Mã sự cố làm cơ sở hủy lịch sạc.|



|**Thuộc tính**|**Nội dung chi tiết**|
|---|---|
|**Giá trị trả về (@return)**|boolean – Trả về true nếu lịch sạc đang CONFIRMED được hủy<br>thành công, false nếu không.|
|**Ngoại lệ (@exception)**|Khôngcó.|
|**Tiền điều kiện (Pre-**<br>**conditions)**|Lịch đăng ký sạc thuộc về cổng sạc bị tạm ngưng hoạt động.|
|**Hậu điều kiện (Post-**<br>**conditions)**|Nếu đang CONFIRMED -> status chuyển sang<br>CANCELLED_BY_INCIDENT.|
|**Luồng thuật toán**<br>**(Pseudo-code)**|1. Nếu this.status != "CONFIRMED" -> trả về false.<br>2. Gán this.status = "CANCELLED_BY_INCIDENT".<br>3. Trả về true.|



## **1.11. Use Case UC13 - Lập lịch sạc thông minh** 

### **_1.11.1. displaySchedule()_** 

|**Thuộc tính**|**Nội dung chi tiết**|
|---|---|
|**Tênphương thức**|displaySchedule()|
|**Mục đích**|Hiển thị lịch sạc thông minh do hệ thống đề xuất, bao gồm phương<br>tiện, cổng sạc, thời điểm bắt đầu, thời điểm kết thúc và mức độ ưu<br>tiên.|
|**Tham số đầu vào**<br>**(@param)**|schedule: ChargingSchedule – Lịch sạc cần hiển thị.|
|**Giá trị trả về(@return)**|void – Khôngtrả vềgiá trị.|
|**Ngoại lệ (@exception)**|DisplayException – Xảy ra khi giao diện không thể hiển thị dữ liệu<br>lịch sạc.|
|**Tiền điều kiện (Pre-**<br>**conditions)**|Hệ thống đã tạo được lịch sạc và dữ liệu lịch hợp lệ.|
|**Hậu điều kiện (Post-**<br>**conditions)**|Lịch sạc được hiển thị đầy đủ trên giao diện để Đơn vị vận hành xem<br>xét.|
|**Luồng thuật toán**<br>**(Pseudo-code)**|1. Tiếp nhận dữ liệu lịch sạc. 2. Trích xuất thông tin phương tiện,<br>cổng sạc, thời gian và mức độ ưu tiên. 3. Hiển thị lịch sạc trên giao<br>diện.|



### **_1.11.2. editSchedule()_** 

|**Thuộc tính**|**Nội dung chi tiết**|
|---|---|
|**Tênphương thức**|editSchedule()|
|**Mục đích**|Cho phép Đơn vị vận hành chỉnh sửa vị trí Hub hoặc thời gian sạc<br>của một sốphươngtiện trước khiphê duyệt lịch.|
|**Tham số đầu vào**<br>**(@param)**|scheduleId: String – Mã lịch sạc cần chỉnh sửa. updatedData:<br>Map<String, Object> – Thông tin điều chỉnh về Hub hoặc thời gian<br>sạc.|
|**Giá trị trả về(@return)**|void – Khôngtrả vềgiá trị.|
|**Ngoại lệ (@exception)**|InvalidScheduleException – Xảy ra khi thông tin lịch sạc hoặc dữ<br>liệu điều chỉnh khônghợplệ.|
|**Tiền điều kiện (Pre-**<br>**conditions)**|Lịch sạc đã được tạo và hiển thị; lịch chưa được phê duyệt chính<br>thức.|



|**Thuộc tính**|**Nội dung chi tiết**|
|---|---|
|**Hậu điều kiện (Post-**<br>**conditions)**|Thông tin điều chỉnh được tiếp nhận và chuyển đến bộ điều khiển để<br>kiểm tra tính hợplệ.|
|**Luồng thuật toán**|1. Đơn vị vận hành chọn lịch cần chỉnh sửa. 2. Nhập thông tin Hub<br>hoặc thời gian sạc mới. 3. Gửi dữ liệu điều chỉnh đến<br>|
|**(Pseudo-code)**|ChargingScheduleController. 4. Tiếp nhận kết quả kiểm tra và hiển<br>thị thôngbáo tươngứng.|



### **_1.11.3. approveSchedule()_** 

|**Thuộc tính**|**Nội dung chi tiết**|
|---|---|
|**Tênphương thức**|approveSchedule()|
|**Mục đích**|Tiếp nhận thao tác phê duyệt lịch sạc của Đơn vị vận hành sau khi<br>xem xét lịch đề xuất.|
|**Tham số đầu vào**<br>**(@param)**|scheduleId: String – Mã lịch sạc cần phê duyệt.|
|**Giá trị trả về(@return)**|void – Khôngtrả vềgiá trị.|
|**Ngoại lệ (@exception)**|ApprovalException – Xảy ra khi yêu cầu phê duyệt không hợp lệ<br>hoặc khôngthể xử lý.|
|**Tiền điều kiện (Pre-**<br>**conditions)**|Lịch sạc đã được tạo, hiển thị và đáp ứng điều kiện phê duyệt.|
|**Hậu điều kiện (Post-**<br>**conditions)**|Yêu cầu phê duyệt được chuyển đến ChargingScheduleController để<br>xử lý.|
|**Luồng thuật toán**<br>**(Pseudo-code)**|1. Đơn vị vận hành chọn chức năng phê duyệt. 2. Gửi mã lịch sạc<br>đến bộ điều khiển. 3. Chờ kết quả xử lý. 4. Hiển thị thông báo tương<br>ứngtrêngiao diện.|



### **_1.11.4. displayWarning()_** 

|**Thuộc tính**|**Nội dung chi tiết**|
|---|---|
|**Tênphương thức**|displayWarning()|
|**Mục đích**|Hiển thị cảnh báo khi hệ thống phát hiện tình trạng quá tải tài<br>nguyên sạc hoặc lỗi truyxuất dữ liệu.|
|**Tham số đầu vào**<br>**(@param)**|warningMessage: String – Nội dung cảnh báo cần hiển thị.|
|**Giá trị trả về(@return)**|void – Khôngtrả vềgiá trị.|
|**Ngoại lệ (@exception)**|DisplayException – Xảy ra khi giao diện không thể hiển thị thông<br>báo cảnh báo.|
|**Tiền điều kiện (Pre-**<br>**conditions)**|Hệ thống đã phát hiện lỗi hoặc tình trạng bất thường và xác định<br>được nội dungcảnh báo.|
|**Hậu điều kiện (Post-**<br>**conditions)**|Đơn vị vận hành nhận được thông tin cảnh báo trên giao diện.|
|**Luồng thuật toán**<br>**(Pseudo-code)**|1. Tiếp nhận nội dung cảnh báo. 2. Xác định loại cảnh báo. 3. Hiển<br>thị thông báo trên màn hình. 4. Hướng dẫn Đơn vị vận hành thực<br>hiện thao tácphù hợp.|



### **_1.11.5. generateSchedule()_** 

|**Thuộc tính**|**Nội dung chi tiết**|
|---|---|
|**Tênphương thức**|generateSchedule()|
|**Mục đích**|Thu thập dữ liệu trạng thái tài nguyên và xây dựng lịch sạc ưu tiên<br>dựa trên mức pin, nhu cầu sử dụng dự kiến, thời gian chờ, trạng thái<br>cổngsạc và sức chứa Hub.|
|**Tham số đầu vào**<br>**(@param)**|Không có. Hệ thống tự truy xuất dữ liệu trạng thái đã được cập nhật<br>từ UC16.|
|**Giá trị trả về(@return)**|ChargingSchedule – Lịch sạc được hệ thốngđề xuất.|
|**Ngoại lệ (@exception)**|DataRetrievalException – Xảy ra khi không thể truy xuất dữ liệu từ<br>simulator hoặc cảm biến. ResourceOverloadException – Xảy ra khi<br>số lượng phương tiện cần sạc khẩn cấp vượt quá số cổng sạc khả<br>dụng.|
|**Tiền điều kiện (Pre-**<br>**conditions)**|Đơn vị vận hành đã đăng nhập thành công và hệ thống có dữ liệu<br>hợp lệ về mức pin, nhu cầu sử dụng, thời gian chờ, trạng thái cổng<br>sạc và sức chứa Hub.|
|**Hậu điều kiện (Post-**<br>**conditions)**|Lịch sạc đề xuất được tạo dựa trên dữ liệu tài nguyên hiện tại, chưa<br>được lưu chính thức vào hệ thống.|
|**Luồng thuật toán**<br>**(Pseudo-code)**|1. Thu thập dữ liệu trạng thái phương tiện và tài nguyên sạc. 2. Kiểm<br>tra tính hợp lệ của dữ liệu. 3. Ưu tiên phương tiện có mức pin thấp<br>hoặc có nhu cầu sử dụng gần. 4. Phân bổ cổng sạc và khung thời<br>gian phù hợp. 5. Kiểm tra xung đột cổng sạc, khung giờ và sức chứa<br>Hub. 6. Tạo lịch sạc đề xuất.|



### **_1.11.6. validateSchedule()_** 

|**Thuộc tính**|**Nội dung chi tiết**|
|---|---|
|**Tênphương thức**|validateSchedule()|
|**Mục đích**|Kiểm tra tính hợp lệ của lịch sạc, bảo đảm không xảy ra xung đột<br>cổngsạc, trùngkhung giờ hoặc vượtquá sức chứa Hub.|
|**Tham số đầu vào**<br>**(@param)**|schedule: ChargingSchedule – Lịch sạc cần kiểm tra.|
|**Giá trị trả về(@return)**|Boolean – Trả về true nếu lịch hợplệ, false nếuphát hiện viphạm.|
|**Ngoại lệ (@exception)**|InvalidScheduleException – Xảy ra khi dữ liệu lịch sạc không đầy<br>đủ hoặc khônghợplệ.|
|**Tiền điều kiện (Pre-**<br>**conditions)**|Lịch sạc đã được tạo hoặc có thay đổi từ thao tác chỉnh sửa của Đơn<br>vị vận hành.|
|**Hậu điều kiện (Post-**<br>**conditions)**|Kết quả kiểm tra tính hợp lệ của lịch sạc được xác định, làm cơ sở<br>cho bướcphê duyệt.|
|**Luồng thuật toán**<br>**(Pseudo-code)**|1. Tiếp nhận lịch sạc cần kiểm tra. 2. Kiểm tra thời gian của từng<br>lượt sạc. 3. Kiểm tra tình trạng khả dụng của cổng sạc. 4. Kiểm tra<br>trùng cổng và khung giờ. 5. Kiểm tra sức chứa Hub. 6. Trả về kết<br>quả kiểm tra.|



### **_1.11.7. editSchedule()_** 

|**Thuộc tính**|**Nội dung chi tiết**|
|---|---|
|**Tênphương thức**|editSchedule()|
|**Mục đích**|Xử lý yêu cầu điều chỉnh lịch sạc của Đơn vị vận hành và kiểm tra<br>tính hợplệ của các thayđổi trước khiphê duyệt.|
|**Tham số đầu vào**<br>**(@param)**|scheduleId: String – Mã lịch sạc cần chỉnh sửa. updatedData:<br>Map<String, Object> – Thông tin Hub hoặc thời gian sạc được điều<br>chỉnh.|
|**Giá trị trả về(@return)**|ChargingSchedule – Lịch sạc sau khi được cậpnhật hợplệ.|
|**Ngoại lệ (@exception)**|InvalidScheduleException – Xảy ra khi thông tin điều chỉnh không<br>hợp lệ. ResourceConflictException – Xảy ra khi cổng sạc hoặc<br>khung giờ được chọn khôngcòn khả dụng.|
|**Tiền điều kiện (Pre-**<br>**conditions)**|Lịch sạc đã được tạo và chưa được phê duyệt chính thức.|
|**Hậu điều kiện (Post-**<br>**conditions)**|Lịch sạc được cập nhật nếu các thay đổi đáp ứng điều kiện hợp lệ;<br>nếu không, lịchgiữ nguyên trạngthái trước đó.|
|**Luồng thuật toán**<br>**(Pseudo-code)**|1. Tiếp nhận yêu cầu chỉnh sửa. 2. Xác định lịch cần cập nhật. 3. Áp<br>dụng thông tin điều chỉnh. 4. Gọi validateSchedule() để kiểm tra tính<br>hợp lệ. 5. Nếu hợp lệ, cập nhật lịch. 6. Nếu không hợp lệ, trả về<br>thôngbáo lỗi vàyêu cầu điều chỉnh lại.|



### **_1.11.8. approveSchedule()_** 

|**Thuộc tính**|**Nội dung chi tiết**|
|---|---|
|**Tênphương thức**|approveSchedule()|
|**Mục đích**|Xác nhận lịch sạc sau khi được Đơn vị vận hành phê duyệt hoặc<br>được hệ thốngtự độngápdụngtheo chế độphê duyệt tự động.|
|**Tham số đầu vào**<br>**(@param)**|scheduleId: String – Mã lịch sạc cần phê duyệt. approvalMode:<br>String– Chế độphê duyệt,gồm MANUAL hoặc AUTO.|
|**Giá trị trả về (@return)**|Boolean – Trả về true nếu lịch được phê duyệt thành công, false nếu<br>khôngthểphê duyệt.|
|**Ngoại lệ (@exception)**|ApprovalException – Xảy ra khi lịch sạc không đáp ứng điều kiện<br>phê duyệt. ResourceConflictException – Xảy ra khi tài nguyên sạc<br>phát sinh xungđột tại thời điểmphê duyệt.|
|**Tiền điều kiện (Pre-**<br>**conditions)**|Lịch sạc đã được tạo và vượt qua bước kiểm tra tính hợp lệ.|
|**Hậu điều kiện (Post-**<br>**conditions)**|Lịch sạc được xác nhận phê duyệt và chuyển sang bước lưu chính<br>thức.|
|**Luồng thuật toán**<br>**(Pseudo-code)**|1. Tiếp nhận yêu cầu phê duyệt và chế độ phê duyệt. 2. Kiểm tra<br>trạng thái lịch sạc. 3. Kiểm tra lại tính hợp lệ và khả dụng của tài<br>nguyên. 4. Xác nhận phê duyệt thủ công hoặc tự động theo cấu hình.<br>5. Chuyển lịch sangbước lưu chính thức.|



### **_1.11.9. saveSchedule()_** 

|**Thuộc tính**|**Nội dung chi tiết**|
|---|---|
|**Tênphương thức**|saveSchedule()|
|**Mục đích**|Lưu lịch sạc đã được phê duyệt, cập nhật trạng thái các cổng sạc<br>thành “đã giữ chỗ” và ghi nhận thao tác vào AuditLog trong cùng<br>mộtgiao dịch nguyên tử.|
|**Tham số đầu vào**<br>**(@param)**|schedule: ChargingSchedule – Lịch sạc đã được phê duyệt cần lưu.|
|**Giá trị trả về (@return)**|Boolean – Trả về true nếu toàn bộ giao dịch thành công, false nếu<br>giao dịch thất bại.|
|**Ngoại lệ (@exception)**|TransactionException – Xảy ra khi giao dịch lưu lịch, giữ cổng sạc<br>hoặcghi logkhôngthể hoàn tất.|
|**Tiền điều kiện (Pre-**<br>**conditions)**|Lịch sạc đã được phê duyệt và các cổng sạc được phân bổ vẫn khả<br>dụng.|
|**Hậu điều kiện (Post-**<br>**conditions)**|Nếu giao dịch thành công, lịch được lưu, cổng sạc được chuyển sang<br>trạng thái “đã giữ chỗ” và AuditLog được ghi nhận. Nếu giao dịch<br>thất bại, toàn bộ thayđổi trong giao dịch được hoàn tác.|
|**Luồng thuật toán**<br>**(Pseudo-code)**|1. Bắt đầu giao dịch. 2. Kiểm tra lại khả năng giữ cổng sạc. 3. Lưu<br>lịch sạc. 4. Cập nhật trạng thái các cổng sạc thành “đã giữ chỗ”. 5.<br>Ghi nhận thao tác vào AuditLog. 6. Commit giao dịch nếu tất cả<br>bước thành công. 7. Rollback toàn bộ thayđổi nếu xảyra lỗi.|



## **1.12. Use Case UC14 - Mô phỏng và phân tích kịch bản** 

### **_1.12.1. displayInterface()_** 

|**Thuộc tính**|**Nội dung chi tiết**|
|---|---|
|**Tênphương thức**|displayInterface()|
|**Mục đích**|Hiển thị giao diện mô phỏng What-if, cho phép Đơn vị vận hành<br>thiết lậpcác tham sốgiả định cho kịch bản môphỏng.|
|**Tham số đầu vào**<br>**(@param)**|Không có.|
|**Giá trị trả về(@return)**|void - Khôngtrả vềgiá trị.|
|**Ngoại lệ (@exception)**|DisplayException - Xảy ra khi hệ thống không thể hiển thị giao diện<br>môphỏng.|
|**Tiền điều kiện (Pre-**<br>**conditions)**|Đơn vị vận hành đã đăng nhập thành công và truy cập chức năng Mô<br>phỏngWhat-if.|
|**Hậu điều kiện (Post-**<br>**conditions)**|Giao diện mô phỏng được hiển thị, sẵn sàng tiếp nhận các tham số<br>giả định.|
|**Luồng thuật toán**<br>**(Pseudo-code)**|1. Tiếp nhận yêu cầu truy cập chức năng mô phỏng.<br>2. Khởi tạo giao diện What-if.<br>3. Hiển thị các trường thiết lập tham số giả định.<br>4. ChophépĐơn vị vận hành nhậpthôngtin kịch bản.|



### **_1.12.2. setupParameters()_** 

|**Thuộc tính**|**Nội dung chi tiết**|
|---|---|
|**Tênphương thức**|setupParameters()|
|**Mục đích**|Tiếp nhận và thiết lập các tham số giả định cho kịch bản mô phỏng,<br>chẳng hạn tăng số lượng xe, giảm số cổng sạc hoặc đóng cửa một<br>Hub.|
|**Tham số đầu vào**<br>**(@param)**|parameters: Map<String, Object> - Tập hợp các tham số giả định do<br>Đơn vị vận hành thiết lập.|
|**Giá trị trả về (@return)**|Map<String, Object> - Tập hợp tham số mô phỏng đã được tiếp<br>nhận.|
|**Ngoại lệ (@exception)**|InvalidParameterException - Xảy ra khi dữ liệu đầu vào không đúng<br>định dạng.|
|**Tiền điều kiện (Pre-**<br>**conditions)**|Giao diện mô phỏng đã được hiển thị và Đơn vị vận hành đang thiết<br>lậpkịch bản.|
|**Hậu điều kiện (Post-**<br>**conditions)**|Các tham số giả định được tiếp nhận và chuyển đến bộ điều khiển để<br>kiểm tra tính hợplệ.|
|**Luồng thuật toán**<br>**(Pseudo-code)**|1. Tiếp nhận các tham số giả định.<br>2. Ghi nhận giá trị của từng tham số.<br>3. Kiểm tra sơ bộ định dạng dữ liệu.<br>4. Chuyển tậptham số đến SimulationController.|



### **_1.12.3. runSimulation()_** 

|**Thuộc tính**|**Nội dung chi tiết**|
|---|---|
|**Tênphương thức**|runSimulation()|
|**Mục đích**|Tiếp nhận yêu cầu chạy mô phỏng và gửi các tham số kịch bản đến<br>bộ điều khiển để thực hiện môphỏngtrên môi trườngảo cách ly.|
|**Tham số đầu vào**<br>**(@param)**|parameters: Map<String, Object> - Tập hợp tham số giả định cần sử<br>dụngđể chạymôphỏng.|
|**Giá trị trả về(@return)**|void - Khôngtrả vềgiá trị.|
|**Ngoại lệ (@exception)**|InvalidParameterException - Tham số mô phỏng không hợp lệ.<br>SimulationInitializationException - Không thể khởi tạo môi trường<br>môphỏngcách ly.|
|**Tiền điều kiện (Pre-**<br>**conditions)**|Các tham số mô phỏng đã được thiết lập và Đơn vị vận hành chọn<br>chức năngChạymôphỏng.|
|**Hậu điều kiện (Post-**<br>**conditions)**|Yêu cầu mô phỏng được chuyển đến bộ điều khiển; kết quả được<br>chuyển đếngiao diện sau khi xử lýhoàn tất.|
|**Luồng thuật toán**<br>**(Pseudo-code)**|1. Tiếp nhận thao tác Chạy mô phỏng.<br>2. Lấy tập tham số đã thiết lập.<br>3. Gửi yêu cầu đến SimulationController.<br>4. Chờ kết quả xử lý.<br>5. Chuyển kếtquả đếnphươngthức hiển thị báo cáo.|



### **_1.12.4. showReport()_** 

|**Thuộc tính**|**Nội dung chi tiết**|
|---|---|
|**Tênphương thức**|showReport()|
|**Mục đích**|Hiển thị báo cáo đánh giá tác động và các đề xuất điều phối được tạo<br>ra sau khi hoàn tất môphỏng.|
|**Tham số đầu vào**<br>**(@param)**|report: String - Nội dung báo cáo đánh giá tác động và đề xuất điều<br>phối.|
|**Giá trị trả về(@return)**|void - Khôngtrả vềgiá trị.|
|**Ngoại lệ (@exception)**|DisplayException - Xảyra khi khôngthể hiển thị báo cáo môphỏng.|
|**Tiền điều kiện (Pre-**<br>**conditions)**|Quá trình mô phỏng đã hoàn tất và hệ thống đã tạo được báo cáo kết<br>quả.|
|**Hậu điều kiện (Post-**<br>**conditions)**|Báo cáo đánh giá tác động và các đề xuất điều phối được hiển thị để<br>Đơn vị vận hành xem xét.|
|**Luồng thuật toán**<br>**(Pseudo-code)**|1. Tiếp nhận nội dung báo cáo.<br>2. Hiển thị kết quả đánh giá tác động.<br>3. Hiển thị các đề xuất điều phối.<br>4. Cho phép Đơn vị vận hành xem xét, kết thúc hoặc chọn áp dụng<br>đề xuất.|



### **_1.12.5. displayParameterError()_** 

|**Thuộc tính**|**Nội dung chi tiết**|
|---|---|
|**Tênphương thức**|displayParameterError()|
|**Mục đích**|Hiển thị cảnh báo và đánh dấu các trường dữ liệu có tham số không<br>hợplệ để Đơn vị vận hành chỉnh sửa.|
|**Tham số đầu vào**<br>**(@param)**|errorMessage: String - Nội dung lỗi cần hiển thị. parameterName:<br>String- Tên trườngtham số khônghợplệ.|
|**Giá trị trả về(@return)**|void - Khôngtrả vềgiá trị.|
|**Ngoại lệ (@exception)**|DisplayException - Xảyra khi khôngthể hiển thị thôngbáo lỗi.|
|**Tiền điều kiện (Pre-**<br>**conditions)**|Hệ thống đã phát hiện tham số mô phỏng không hợp lệ.|
|**Hậu điều kiện (Post-**<br>**conditions)**|Trường tham số không hợp lệ được đánh dấu và thông báo lỗi được<br>hiển thị; Đơn vị vận hành có thể nhậplại dữ liệu.|
|**Luồng thuật toán**<br>**(Pseudo-code)**|1. Tiếp nhận thông tin lỗi từ bộ điều khiển.<br>2. Xác định trường tham số có lỗi.<br>3. Đánh dấu trường dữ liệu tương ứng.<br>4. Hiển thị thông báo cảnh báo.<br>5. Yêu cầu Đơn vị vận hành nhậplại tham số.|



### **_1.12.6. applyRecommendation()_** 

|**Thuộc tính**|**Nội dung chi tiết**|
|---|---|
|**Tênphương thức**|applyRecommendation()|
|**Mục đích**|Tiếp nhận thao tác của Đơn vị vận hành khi lựa chọn áp dụng một đề<br>xuất điềuphối từ báo cáo môphỏngvàoquytrình vận hành thực tế.|



|**Thuộc tính**|**Nội dung chi tiết**|
|---|---|
|**Tham số đầu vào**<br>**(@param)**|targetUseCase: String - Use Case đích được lựa chọn, gồm UC11<br>hoặc UC13. parameters: Map<String, Object> - Các tham số tương<br>ứngvới đề xuất được lựa chọn.|
|**Giá trị trả về(@return)**|void - Khôngtrả vềgiá trị.|
|**Ngoại lệ (@exception)**|InvalidRecommendationException - Đề xuất được chọn không hợp<br>lệ hoặc khôngthuộc UC11, UC13.|
|**Tiền điều kiện (Pre-**<br>**conditions)**|Báo cáo mô phỏng đã được hiển thị và có đề xuất điều phối khả thi.|
|**Hậu điều kiện (Post-**<br>**conditions)**|Yêu cầu áp dụng đề xuất được gửi đến SimulationController để<br>chuyển tiếpsangUse Case tươngứng.|
|**Luồng thuật toán**<br>**(Pseudo-code)**|1. Đơn vị vận hành chọn Áp dụng vào thực tế.<br>2. Xác định Use Case đích UC11 hoặc UC13.<br>3. Lấy các tham số của đề xuất được chọn.<br>4. Gửiyêu cầu chuyển tiếpđến SimulationController.|



### **_1.12.7. initVirtualEnvironment()_** 

|**Thuộc tính**|**Nội dung chi tiết**|
|---|---|
|**Tênphương thức**|initVirtualEnvironment()|
|**Mục đích**|Sao chép hoặc khởi tạo trạng thái hiện tại của toàn mạng lưới vào<br>môi trường mô phỏng ảo cách ly, bảo đảm quá trình mô phỏng<br>khôngảnh hưởngđến hệ thốngvận hành thực tế.|
|**Tham số đầu vào**<br>**(@param)**|Không có.|
|**Giá trị trả về (@return)**|Boolean - Trả về true nếu môi trường mô phỏng được khởi tạo thành<br>công, false nếu thất bại.|
|**Ngoại lệ (@exception)**|SimulationInitializationException - Xảy ra khi hệ thống không thể<br>cấp phát tài nguyên hoặc khởi tạo môi trườngảo cách ly.|
|**Tiền điều kiện (Pre-**<br>**conditions)**|Hệ thống có thể truy xuất trạng thái hiện tại của mạng lưới và có khả<br>năngcấp phát môi trườngmôphỏng.|
|**Hậu điều kiện (Post-**<br>**conditions)**|Trạng thái hiện tại của mạng lưới được khởi tạo trong môi trường<br>môphỏngriêngbiệt; dữ liệu vận hành thực tế khôngbị thayđổi.|
|**Luồng thuật toán**<br>**(Pseudo-code)**|1. Tiếp nhận yêu cầu khởi tạo môi trường mô phỏng.<br>2. Truy xuất trạng thái hiện tại của mạng lưới.<br>3. Sao chép trạng thái vào môi trường mô phỏng riêng biệt.<br>4. Kiểm tra khả năng hoạt động của môi trường.<br>5. Trả về kếtquả khởi tạo.|



### **_1.12.8. validateParameters()_** 

|**Thuộc tính**|**Nội dung chi tiết**|
|---|---|
|**Tênphương thức**|validateParameters()|
|**Mục đích**|Kiểm tra tính hợp lệ và khả năng thực hiện của các tham số giả định<br>trước khi chạymôphỏng.|
|**Tham số đầu vào**|parameters: Map<String, Object> - Tập hợp tham số giả định do<br>|
|**(@param)**|Đơn vị vận hành cungcấp.|



|**Thuộc tính**|**Nội dung chi tiết**|
|---|---|
|**Giá trị trả về (@return)**|Boolean - Trả về true nếu toàn bộ tham số hợp lệ, false nếu phát hiện<br>tham số khônghợplệ hoặc mâu thuẫn.|
|**Ngoại lệ (@exception)**|InvalidParameterException - Xảy ra khi tham số sai định dạng hoặc<br>khôngthể kiểm tra.|
|**Tiền điều kiện (Pre-**<br>**conditions)**|Các tham số mô phỏng đã được tiếp nhận từ giao diện.|
|**Hậu điều kiện (Post-**<br>**conditions)**|Kết quả kiểm tra tính hợp lệ của tham số được xác định; chỉ tham số<br>hợplệ mới được chuyển sangbước môphỏng.|
|**Luồng thuật toán**<br>**(Pseudo-code)**|1. Tiếp nhận tập tham số.<br>2. Kiểm tra định dạng và kiểu dữ liệu.<br>3. Kiểm tra giá trị không hợp lệ, chẳng hạn số lượng xe âm.<br>4. Kiểm tra giới hạn khả thi của môi trường mô phỏng.<br>5. Trả về kếtquả kiểm tra.|



### **_1.12.9. calculateImpact()_** 

|**Thuộc tính**|**Nội dung chi tiết**|
|---|---|
|**Tênphương thức**|calculateImpact()|
|**Mục đích**|Tính toán sự thay đổi trạng thái của mạng lưới dựa trên các tham số<br>giả định trong môi trường mô phỏng ảo cách ly nhằm đánh giá tác<br>độngcủa kịch bản.|
|**Tham số đầu vào**<br>**(@param)**|parameters: Map<String, Object> - Tập hợp tham số giả định được<br>sử dụngtrong quá trình môphỏng.|
|**Giá trị trả về (@return)**|String - Thông tin tổng hợp về kết quả thay đổi trạng thái và tác<br>độngcủa kịch bản môphỏng.|
|**Ngoại lệ (@exception)**|SimulationCalculationException - Xảy ra khi hệ thống không thể<br>thực hiện tính toán môphỏng.|
|**Tiền điều kiện (Pre-**<br>**conditions)**|Môi trường mô phỏng ảo đã được khởi tạo thành công và các tham<br>sốgiả định đã vượtqua bước kiểm tra tính hợplệ.|
|**Hậu điều kiện (Post-**<br>**conditions)**|Kết quả tính toán tác động được tạo ra trong môi trường mô phỏng;<br>trạngthái vận hành thực tế khôngbị thayđổi.|
|**Luồng thuật toán**<br>**(Pseudo-code)**|1. Tiếp nhận các tham số giả định hợp lệ.<br>2. Truy xuất trạng thái mạng lưới trong môi trường mô phỏng.<br>3. Áp dụng các thay đổi giả định lên dữ liệu mô phỏng.<br>4. Tính toán sự thay đổi về phương tiện, cổng sạc và tình trạng Hub.<br>5. Tổng hợp kết quả đánh giá tác động.<br>6. Trả về kếtquả tính toán.|



### **_1.12.10. generateReport()_** 

|**Thuộc tính**|**Nội dung chi tiết**|
|---|---|
|**Tênphương thức**|generateReport()|
|**Mục đích**|Tổng hợp kết quả mô phỏng để tạo báo cáo đánh giá tác động và đề<br>xuấtphươngán điềuphốiphù hợpcho Đơn vị vận hành.|
|**Tham số đầu vào**|impactResult: String - Kết quả tính toán tác động từ phương thức|
|**(@param)**|calculateImpact().|



|**Thuộc tính**|**Nội dung chi tiết**|
|---|---|
|**Giá trị trả về (@return)**|String - Nội dung báo cáo mô phỏng bao gồm kết quả đánh giá tác<br>độngvà các đề xuất điềuphối.|
|**Ngoại lệ (@exception)**|ReportGenerationException - Xảy ra khi hệ thống không thể tổng<br>hợphoặc tạo báo cáo môphỏng.|
|**Tiền điều kiện (Pre-**<br>**conditions)**|Quá trình tính toán mô phỏng đã hoàn tất và có kết quả tác động hợp<br>lệ.|
|**Hậu điều kiện (Post-**<br>**conditions)**|Báo cáo đánh giá tác động và các đề xuất điều phối được tạo thành<br>công, sẵn sànghiển thị cho Đơn vị vận hành.|
|**Luồng thuật toán**<br>**(Pseudo-code)**|1. Tiếp nhận kết quả tính toán tác động.<br>2. Phân tích các thay đổi trạng thái trong kịch bản.<br>3. Xác định vấn đề phát sinh và mức độ ảnh hưởng.<br>4. Xây dựng đề xuất điều phối như điều chuyển phương tiện hoặc<br>thay đổi lịch sạc.<br>5. Tổng hợp nội dung báo cáo.<br>6. Trả về báo cáo môphỏng.|



### **_1.12.11. saveReport()_** 

|**Thuộc tính**|**Nội dung chi tiết**|
|---|---|
|**Tênphương thức**|saveReport()|
|**Mục đích**|Lưu báo cáo mô phỏng sau khi Đơn vị vận hành chọn chức năng Kết<br>thúc, đồngthời liên kết báo cáo với kịch bản môphỏngtươngứng.|
|**Tham số đầu vào**<br>**(@param)**|scenario: SimulationScenario - Kịch bản mô phỏng cần lưu, bao gồm<br>mã kịch bản và nội dungtóm tắt báo cáo.|
|**Giá trị trả về (@return)**|Boolean - Trả về true nếu báo cáo được lưu thành công, false nếu<br>lưu thất bại.|
|**Ngoại lệ (@exception)**|ReportSaveException - Xảy ra khi hệ thống không thể lưu báo cáo<br>môphỏng.|
|**Tiền điều kiện (Pre-**<br>**conditions)**|Quá trình mô phỏng đã hoàn tất, báo cáo đã được tạo và Đơn vị vận<br>hành chọn chức năngKết thúc.|
|**Hậu điều kiện (Post-**<br>**conditions)**|Báo cáo mô phỏng được lưu và gắn với SimulationScenario; trạng<br>thái vận hành thực tế của mạnglưới khôngbị thayđổi.|
|**Luồng thuật toán**<br>**(Pseudo-code)**|1. Tiếp nhận yêu cầu lưu báo cáo.<br>2. Tiếp nhận thông tin kịch bản và nội dung báo cáo.<br>3. Cập nhật nội dung tóm tắt báo cáo vào SimulationScenario.<br>4. Lưu thông tin kịch bản và báo cáo.<br>5. Trả về kếtquả lưu.|



### **_1.12.12. redirectToUseCase()_** 

|**Thuộc tính**|**Nội dung chi tiết**|
|---|---|
|**Tênphương thức**|redirectToUseCase()|
|**Mục đích**|Chuyển Đơn vị vận hành đến màn hình UC11 hoặc UC13 tương ứng<br>với đề xuất được chọn, đồng thời điền sẵn các tham số liên quan để<br>tiếptục xử lýnghiệpvụ.|
|**Tham số đầu vào**<br>**(@param)**|targetUseCase: String - Mã Use Case đích, gồm UC11 hoặc UC13.<br>parameters: Map<String, Object> - Các tham số tương ứng với đề<br>xuất điềuphối được lựa chọn.|



|**Thuộc tính**|**Nội dung chi tiết**|
|---|---|
|**Giá trị trả về (@return)**|Boolean - Trả về true nếu chuyển tiếp thành công, false nếu không<br>thể chuyển tiếp.|
|**Ngoại lệ (@exception)**|InvalidTargetUseCaseException - Use Case đích không được hỗ trợ<br>hoặc tham số chuyển tiếpkhônghợplệ.|
|**Tiền điều kiện (Pre-**<br>**conditions)**|Báo cáo mô phỏng đã được hiển thị và Đơn vị vận hành đã lựa chọn<br>một đề xuất khả thi để ápdụng.|
|**Hậu điều kiện (Post-**<br>**conditions)**|Đơn vị vận hành được chuyển đến UC11 hoặc UC13 tương ứng và<br>các tham số đề xuất được điền sẵn; trạng thái vận hành thực tế chỉ<br>thay đổi khi nghiệp vụ tại Use Case đích được thực hiện và xác<br>nhận.|
|**Luồng thuật toán**<br>**(Pseudo-code)**|1. Tiếp nhận Use Case đích và tham số đề xuất.<br>2. Kiểm tra Use Case đích có phải UC11 hoặc UC13.<br>3. Xác định màn hình tương ứng.<br>4. Truyền các tham số đề xuất sang Use Case đích.<br>5. Chuyển hướng giao diện đến màn hình tương ứng.<br>6. Trả về kếtquả chuyển tiếp.|



## **1.13. Use Case UC15 - Tùy chỉnh giao diện (Customize UI)** 

### **_1.13.1. toggleTheme()_** 

|**Thuộc tính**|**Nội dung chi tiết**|
|---|---|
|**Tênphương thức**|toggleTheme()|
|**Mục đích**|Hiển thị danh sách tùy chọn giao diện để người dùng lựa chọn chế<br>độ sáng, tối hoặc theo hệ thống.|
|**Tham số đầu vào**<br>**(@param)**|Không có.|
|**Giá trị trả về(@return)**|void – Khôngtrả vềgiá trị.|
|**Ngoại lệ (@exception)**|Khôngcó ngoại lệ nghiệpvụ được xác định.|
|**Tiền điều kiện (Pre-**<br>**conditions)**|Người dùng đang truy cập giao diện hệ thống.|
|**Hậu điều kiện (Post-**<br>**conditions)**|Danh sách tùy chọn giao diện được hiển thị. Chế độ giao diện hiện<br>tại chưa thayđổi.|
|**Luồng thuật toán**<br>**(Pseudo-code)**|1. Người dùng nhấn biểu tượng giao diện.<br>2. Hệ thống hiển thị danh sách Light, Dark và System.<br>3. Chờ người dùnglựa chọn chế độ.|



### **_1.13.2. switchLanguage()_** 

|**Thuộc tính**|**Nội dung chi tiết**|
|---|---|
|**Tênphương thức**|switchLanguage()|
|**Mục đích**|Hiển thị danh sách ngôn ngữ để người dùng lựa chọn ngôn ngữ hiển<br>thị của hệ thống.|
|**Tham số đầu vào**<br>**(@param)**|Không có.|
|**Giá trị trả về(@return)**|void – Khôngtrả vềgiá trị.|
|**Ngoại lệ (@exception)**|Khôngcó ngoại lệ nghiệpvụ được xác định.|



|**Thuộc tính**|**Nội dung chi tiết**|
|---|---|
|**Tiền điều kiện (Pre-**<br>**conditions)**|Người dùng đang truy cập giao diện hệ thống.|
|**Hậu điều kiện (Post-**<br>**conditions)**|Danh sách ngôn ngữ được hiển thị, bao gồm Tiếng Việt và Tiếng<br>Anh.|
|**Luồng thuật toán**<br>**(Pseudo-code)**|1. Người dùng nhấn biểu tượng ngôn ngữ.<br>2. Hệ thống hiển thị danh sách ngôn ngữ hỗ trợ.<br>3. Chờ người dùnglựa chọn ngôn ngữ.|



### **_1.13.3. displayError()_** 

|**Thuộc tính**|**Nội dung chi tiết**|
|---|---|
|**Tênphương thức**|displayError()|
|**Mục đích**|Hiển thị thông báo khi hệ thống không thể lưu cấu hình giao diện<br>hoặc ngôn ngữ.|
|**Tham số đầu vào**<br>**(@param)**|errorMessage: String – Nội dung thông báo lỗi.|
|**Giá trị trả về(@return)**|void – Khôngtrả vềgiá trị.|
|**Ngoại lệ (@exception)**|Khôngcó ngoại lệ nghiệpvụ được xác định.|
|**Tiền điều kiện (Pre-**<br>**conditions)**|Hệ thống phát sinh lỗi trong quá trình lưu cấu hình.|
|**Hậu điều kiện (Post-**<br>**conditions)**|Thông báo lỗi được hiển thị cho người dùng; dữ liệu biểu mẫu đang<br>nhậpkhôngbị mất.|
|**Luồng thuật toán**<br>**(Pseudo-code)**|1. Tiếp nhận nội dung lỗi.<br>2. Hiển thị thông báo lỗi trên giao diện.<br>3. Giữ nguyên dữ liệu biểu mẫu đangthực hiện.|



### **_1.13.4. applyTheme()_** 

|**Thuộc tính**|**Nội dung chi tiết**|
|---|---|
|**Tênphương thức**|applyTheme()|
|**Mục đích**|Áp dụng chế độ giao diện được người dùng lựa chọn cho toàn bộ hệ<br>thống.|
|**Tham số đầu vào**<br>**(@param)**|theme: String – Chế độ giao diện được chọn (LIGHT, DARK,<br>SYSTEM).|
|**Giá trị trả về(@return)**|Boolean – Trả về true nếu ápdụngthành công, ngược lại trả về false.|
|**Ngoại lệ (@exception)**|ThemeApplicationException – Xảy ra khi không thể áp dụng chế độ<br>giao diện.|
|**Tiền điều kiện (Pre-**<br>**conditions)**|Người dùng đã lựa chọn chế độ giao diện hợp lệ.|
|**Hậu điều kiện (Post-**<br>**conditions)**|Giao diện được cập nhật theo chế độ đã chọn mà không tải lại trang<br>hoặc làm mất dữ liệu đangnhập.|
|**Luồng thuật toán**<br>**(Pseudo-code)**|1. Tiếp nhận chế độ giao diện.<br>2. Kiểm tra chế độ được lựa chọn.<br>3. Áp dụng màu sắc và kiểu hiển thị tương ứng.<br>4. Trả về kếtquả thực hiện.|



### **_1.13.5. applyLanguage()_** 

|**Thuộc tính**|**Nội dung chi tiết**|
|---|---|
|**Tênphương thức**|applyLanguage()|
|**Mục đích**|Thay đổi ngôn ngữ hiển thị của hệ thống theo lựa chọn của người<br>dùng.|
|**Tham số đầu vào**<br>**(@param)**|language: String – Ngôn ngữ được chọn (VI, EN).|
|**Giá trị trả về (@return)**|Boolean – Trả về true nếu thay đổi thành công, ngược lại trả về<br>false.|
|**Ngoại lệ (@exception)**|LanguageApplicationException – Xảy ra khi không thể áp dụng<br>ngôn ngữ được chọn.|
|**Tiền điều kiện (Pre-**<br>**conditions)**|Người dùng đã lựa chọn ngôn ngữ được hệ thống hỗ trợ.|
|**Hậu điều kiện (Post-**<br>**conditions)**|Nội dung giao diện được chuyển sang ngôn ngữ đã chọn, không tải<br>lại trangvà khônglàm mất dữ liệu biểu mẫu.|
|**Luồng thuật toán**<br>**(Pseudo-code)**|1. Tiếp nhận ngôn ngữ được chọn.<br>2. Kiểm tra ngôn ngữ có được hỗ trợ hay không.<br>3. Tải nội dung tương ứng với ngôn ngữ đã chọn.<br>4. Cập nhật nội dung giao diện.<br>5. Trả về kếtquả thực hiện.|



### **_1.13.6. preserveFormState()_** 

|**Thuộc tính**|**Nội dung chi tiết**|
|---|---|
|**Tênphương thức**|preserveFormState()|
|**Mục đích**|Bảo toàn dữ liệu người dùng đang nhập trên biểu mẫu khi thay đổi<br>giao diện hoặc ngôn ngữ.|
|**Tham số đầu vào**<br>**(@param)**|formState: Map<String, Object> – Dữ liệu hiện tại của biểu mẫu.|
|**Giá trị trả về(@return)**|Map<String, Object> – Trả về dữ liệu biểu mẫu đã được bảo toàn.|
|**Ngoại lệ (@exception)**|FormStateException – Xảy ra khi không thể bảo toàn dữ liệu biểu<br>mẫu.|
|**Tiền điều kiện (Pre-**<br>**conditions)**|Người dùng đang thực hiện một biểu mẫu có dữ liệu chưa được gửi<br>đi.|
|**Hậu điều kiện (Post-**<br>**conditions)**|Dữ liệu biểu mẫu, bao gồm Hub đã chọn, được giữ nguyên sau khi<br>thayđổigiao diện hoặc ngôn ngữ.|
|**Luồng thuật toán**<br>**(Pseudo-code)**|1. Tiếp nhận dữ liệu biểu mẫu hiện tại.<br>2. Ghi nhận các giá trị người dùng đã nhập và lựa chọn.<br>3. Bảo toàn dữ liệu trong quá trình cập nhật giao diện.<br>4. Trả về trạngthái biểu mẫu đã được bảo toàn.|



### **_1.13.7. savePreference()_** 

|**Thuộc tính**|**Nội dung chi tiết**|
|---|---|
|**Tênphương thức**|savePreference()|
|**Mục đích**|Lưu tùy chọn giao diện và ngôn ngữ của người dùng để duy trì thiết<br>lậpđã lựa chọn.|



|**Thuộc tính**|**Nội dung chi tiết**|
|---|---|
|**Tham số đầu vào**<br>**(@param)**|theme: String – Chế độ giao diện; language: String – Ngôn ngữ được<br>lựa chọn.|
|**Giá trị trả về(@return)**|Boolean – Trả về true nếu lưu thành công, ngược lại trả về false.|
|**Ngoại lệ (@exception)**|PreferenceSaveException – Xảyra khi khôngthể lưu cấu hình.|
|**Tiền điều kiện (Pre-**<br>**conditions)**|Chế độ giao diện và ngôn ngữ đã được lựa chọn hợp lệ.|
|**Hậu điều kiện (Post-**<br>**conditions)**|Tùy chọn giao diện và ngôn ngữ được lưu thành công vào bộ nhớ<br>cấu hình cục bộ.|
|**Luồng thuật toán**<br>**(Pseudo-code)**|1. Tiếp nhận chế độ giao diện và ngôn ngữ.<br>2. Kiểm tra tính hợp lệ của các tùy chọn.<br>3. Lưu cấu hình vào bộ nhớ cục bộ.<br>4. Trả về kếtquả lưu cấu hình.|



### **_1.13.8. handleSaveError()_** 

|**Thuộc tính**|**Nội dung chi tiết**|
|---|---|
|**Tênphương thức**|handleSaveError()|
|**Mục đích**|Xử lý lỗi phát sinh khi hệ thống không thể lưu tùy chọn giao diện<br>hoặc ngôn ngữ.|
|**Tham số đầu vào**<br>**(@param)**|error: Exception – Thông tin ngoại lệ phát sinh trong quá trình lưu<br>cấu hình.|
|**Giá trị trả về(@return)**|String– Nội dungthôngbáo lỗi cần hiển thị.|
|**Ngoại lệ (@exception)**|Khôngcó ngoại lệ nghiệpvụ bổ sungđược xác định.|
|**Tiền điều kiện (Pre-**<br>**conditions)**|Phương thức savePreference() thực hiện không thành công.|
|**Hậu điều kiện (Post-**<br>**conditions)**|Lỗi được xử lý và thông tin lỗi được chuyển đến giao diện; hệ thống<br>duytrì cấu hình hiện tại và khônglàm mất dữ liệu biểu mẫu.|
|**Luồng thuật toán**<br>**(Pseudo-code)**|1. Tiếp nhận thông tin ngoại lệ.<br>2. Xác định lỗi phát sinh trong quá trình lưu.<br>3. Tạo nội dung thông báo lỗi.<br>4. Trả về thôngbáo đểgiao diện hiển thị.|



## **1.14. Use Case UC16 – Cập nhật trạng thái tài nguyên (Update Resource Status)** 

### **_1.14.1. receiveTelemetryPacket(packet)_** 

|**Thuộc tính**|**Nội dung chi tiết**|
|---|---|
|**Tênphương thức**|receiveTelemetryPacket(packet)|
|**Mục đích**|Tiếp nhận gói tin trạng thái thời gian thực từ Bộ giả lập dữ liệu (hoặc<br>cảm biến IoT), điều phối qua ResourceSyncController và trả mã<br>phản hồi HTTP chuẩn(200 OK hoặc 400 Bad Request).|
|**Tham số đầu vào**<br>**(@param)**|packet: ResourcePacket – Gói dữ liệu trạng thái gồm ID tài nguyên,<br>trạngthái, mứcpin, tọa độ, timestampvà cờ môphỏng.|
|**Giá trị trả về (@return)**|HttpResponse – Mã 200 OK nếu cập nhật thành công hoặc loại bỏ<br>gói trễ đúng quy định; mã 400 Bad Request nếu sai định dạng hoặc<br>khôngtìm thấyID(EX2).|



|**Thuộc tính**|**Nội dung chi tiết**|
|---|---|
|**Ngoại lệ (@exception)**|Không ném ngoại lệ ra ngoài giao thức HTTP; các ngoại lệ nghiệp<br>vụ được ánh xạ thành mã trạngthái HTTP tươngứng.|
|**Tiền điều kiện (Pre-**<br>**conditions)**|Hệ thống đang hoạt động và lắng nghe kết nối từ Bộ giả lập dữ liệu.|
|**Hậu điều kiện (Post-**<br>**conditions)**|Gói tin được xử lý; nếu hợp lệ và mới nhất, giao diện người dùng<br>nhận cập nhật trong <= REALTIME_SLA_SECONDS (15 giây –<br>NFR02).|
|**Luồng thuật toán**<br>**(Pseudo-code)**|1. Try:<br>a. Gọi result =<br>ResourceSyncController.ingestResourceStatus(packet).<br>b. Trả về HttpResponse(200, "OK", result).<br>2. Catch (InvalidPacketException | ResourceNotFoundException<br>ex):<br>a. Trả về HttpResponse(400, "Bad Request", ex.message).|



### **_1.14.2. ingestResourceStatus(packet)_** 

|**Thuộc tính**|**Nội dung chi tiết**|
|---|---|
|**Tênphương thức**|ingestResourceStatus(packet)|
|**Mục đích**|Xử lý toàn bộ luồng đồng bộ trạng thái tài nguyên: kiểm tra hợp lệ<br>cấu trúc và ID (EX2), lọc/loại bỏ gói tin trễ theo Timestamp (EX1 –<br>NFR08), tách luồng What-If Sandbox (AF1 – NFR07) và phát tín<br>hiệu WebSocket/SSE(NFR02).|
|**Tham số đầu vào**<br>**(@param)**|packet: ResourcePacket – Gói tin telemetry nhận được từ Endpoint.|
|**Giá trị trả về (@return)**|SyncResult – Kết quả xử lý gồm trạng thái<br>{UPDATED_OPERATIONAL, UPDATED_SANDBOX,<br>DROPPED_OUTDATED}.|
|**Ngoại lệ (@exception)**|InvalidPacketException (EX2) – Gói tin thiếu trường bắt buộc hoặc<br>giá trị không hợp lệ.<br>ResourceNotFoundException (EX2) – Không tìm thấy tài nguyên<br>tươngứngvớipacket.resourceId.|
|**Tiền điều kiện (Pre-**<br>**conditions)**|Gói tin đã được tiếp nhận tại ResourceIngestionEndpoint.|
|**Hậu điều kiện (Post-**<br>**conditions)**|Nếu gói mới hợp lệ (vận hành thực tế): Operational DB được cập<br>nhật và RealtimeGateway phát tín hiệu. Nếu isSimulation=true: chỉ<br>ghi vào SandboxStateStore. Nếu gói trễ: hủy gói, ghi log loại bỏ,<br>không ghi đè CSDL.|



|**Thuộc tính**|**Nội dung chi tiết**|
|---|---|
|**Luồng thuật toán**<br>**(Pseudo-code)**|1. Gọi validatePacket(packet); nếu lỗi -> ghi AuditLog("SYSTEM",<br>"INTEGRATION_ERROR", packet.resourceId, err) và ném ngoại<br>lệ.<br>2. Nếu packet.isSimulation == true (AF1 – NFR07):<br>a. Gọi SandboxStateStore.upsertSimulatedState(packet).<br>b. Trả về SyncResult(UPDATED_SANDBOX) // Tuyệt đối không<br>ghi đè Operational DB.<br>3. Tìm Resource resource =<br>resourceRepo.findById(packet.resourceId); nếu null -> ghi AuditLog<br>lỗi tích hợp và ném ResourceNotFoundException.<br>4. Nếu isOutdatedPacket(packet.packetTimestamp,<br>resource.lastUpdatedAt) == true (EX1 – NFR08):<br>a. Gọi AuditLog.record("SIMULATOR",<br>"DROP_OUTDATED_PACKET", packet.resourceId, "Dropped<br>stale packet").<br>b. Trả về SyncResult(DROPPED_OUTDATED) // Không ghi đè<br>dữ liệu mới hơn.<br>5. Cập nhật Operational DB:<br>- Nếu resource là SharedVehicle -> gọi<br>resource.updateTelemetry(packet.status, packet.batteryLevel,<br>packet.packetTimestamp).<br>- Ngược lại -> gọi resource.updateStatus(packet.status,<br>packet.packetTimestamp).<br>6. Gọi RealtimeGateway.broadcastResourceUpdate(resource.id,<br>resource.status, packet.packetTimestamp) (NFR02 <= 15s).<br>7. Trả về SyncResult(UPDATED_OPERATIONAL).|



### **_1.14.3. validatePacket(packet)_** 

|**Thuộc tính**|**Nội dung chi tiết**|
|---|---|
|**Tênphương thức**|validatePacket(packet)|
|**Mục đích**|Kiểm tra tính đầy đủ và hợp lệ về cấu trúc dữ liệu của gói tin<br>telemetry trước khi truy xuất hoặc ghi CSDL (UC16 – Bước 2 &<br>EX2).|
|**Tham số đầu vào**<br>**(@param)**|packet: ResourcePacket – Gói tin cần kiểm tra.|
|**Giá trị trả về(@return)**|void – Kết thúc bình thườngnếugói tin hợplệ.|
|**Ngoại lệ (@exception)**|InvalidPacketException – Xảy ra khi packet null, thiếu<br>resourceId/status/packetTimestamp, hoặc batteryLevel nằm ngoài [0,<br>100].|
|**Tiền điều kiện (Pre-**<br>**conditions)**|Gói tin đã được deserialize thành đối tượng ResourcePacket.|
|**Hậu điều kiện (Post-**<br>**conditions)**|Đảm bảo gói tin đạt chuẩn cấu trúc trước khi so sánh timestamp<br>hoặc cậpnhật trạngthái.|



|**Thuộc tính**|**Nội dung chi tiết**|
|---|---|
|**Luồng thuật toán**|1. Nếu packet == null -> ném InvalidPacketException("Packet is<br>null").<br>2. Nếu packet.resourceId rỗng hoặc packet.status == null hoặc<br>packet.packetTimestamp == null -> ném|
|**(Pseudo-code)**|InvalidPacketException("Missing required fields").<br>3. Nếu packet.batteryLevel != null và (packet.batteryLevel < 0 ||<br>packet.batteryLevel > 100) -> ném InvalidPacketException("Invalid<br>batterylevel").|



### **_1.14.4. isOutdatedPacket(packetTimestamp, currentTimestamp)_** 

|**Thuộc tính**|**Nội dung chi tiết**|
|---|---|
|**Tênphương thức**|isOutdatedPacket(packetTimestamp, currentTimestamp)|
|**Mục đích**|So sánh dấu thời gian của gói tin đến với thời điểm cập nhật hiện tại<br>trongCSDL đểphát hiệngói tin bị trễ hoặc trùnglặp (NFR08).|
|**Tham số đầu vào**<br>**(@param)**|packetTimestamp: LocalDateTime – Thời điểm ghi nhận trên gói tin<br>đến.<br>currentTimestamp: LocalDateTime (nullable) – Thời điểm cập nhật<br>hiện tại của tài nguyên trongCSDL.|
|**Giá trị trả về (@return)**|boolean – Trả về true nếu gói tin bị lỗi thời (packetTimestamp <=<br>currentTimestamp), false nếu gói tin mới hơn (packetTimestamp ><br>currentTimestamp).|
|**Ngoại lệ (@exception)**|Khôngcó.|
|**Tiền điều kiện (Pre-**<br>**conditions)**|packetTimestamp đã được kiểm tra khác null trong validatePacket().|
|**Hậu điều kiện (Post-**<br>**conditions)**|Không thay đổi dữ liệu; kết quả quyết định cho phép cập nhật hay<br>hủybỏgói tin.|
|**Luồng thuật toán**<br>**(Pseudo-code)**|1. Nếu currentTimestamp == null -> trả về false (chấp nhận bản ghi<br>đầu tiên).<br>2. Trả vềpacketTimestamp<= currentTimestamp.|



### **_1.14.5. upsertSimulatedState(packet)_** 

|**Thuộc tính**|**Nội dung chi tiết**|
|---|---|
|**Tênphương thức**|upsertSimulatedState(packet)|
|**Mục đích**|Cập nhật trạng thái tài nguyên giả lập vào kho lưu trữ ảo cách ly<br>(What-If Sandbox) mà hoàn toàn không tác động tới Operational DB<br>(UC16 – AF1, NFR07).|
|**Tham số đầu vào**<br>**(@param)**|packet: ResourcePacket – Gói tin mô phỏng có cờ isSimulation =<br>true.|
|**Giá trị trả về(@return)**|void – Khôngtrả vềgiá trị.|
|**Ngoại lệ (@exception)**|InvalidStateException – Xảyra khipacket.isSimulation == false.|
|**Tiền điều kiện (Pre-**<br>**conditions)**|Môi trường What-If Sandbox đã được khởi tạo theo scenarioId.|
|**Hậu điều kiện (Post-**<br>**conditions)**|Bản đồ simulatedResources trong Sandbox được cập nhật trạng thái<br>mới nhất (với kiểm tra timestamp nội bộ Sandbox); Operational DB<br>khôngthayđổi.|



|**Thuộc tính**|**Nội dung chi tiết**|
|---|---|
|**Luồng thuật toán**<br>**(Pseudo-code)**|1. Nếu !packet.isSimulation -> ném<br>InvalidStateException("Operational packet cannot enter sandbox").<br>2. Lấy simulated = this.simulatedResources.get(packet.resourceId).<br>3. Nếu simulated == null hoặc packet.packetTimestamp ><br>simulated.lastUpdatedAt:<br>a. Cập nhật trạng thái và lastUpdatedAt của bản sao trong<br>simulatedResources.<br>b. Cậpnhật this.lastSyncAt = now().|



## **1.15. Các lớp Thực thể Lõi & Giao diện Dùng chung (Core Domain & Interfaces)** 

### **_1.15.1. MobilityHub.hasAvailableCapacity(requiredCount)_** 

|**Thuộc tính**|**Nội dung chi tiết**|
|---|---|
|**Tênphương thức**|MobilityHub.hasAvailableCapacity(requiredCount)|
|**Mục đích**|Kiểm tra xem Hub có đủ số chỗ đỗ trống để tiếp nhận thêm phương<br>tiện điềuphối haykhông (UC11 – EX2).|
|**Tham số đầu vào**<br>**(@param)**|requiredCount: int – Số lượng phương tiện dự kiến điều phối đến<br>Hub.|
|**Giá trị trả về (@return)**|boolean – Trả về true nếu Hub đang ACTIVE và availableSpots >=<br>requiredCount, ngược lại false.|
|**Ngoại lệ (@exception)**|IllegalArgumentException – Khi requiredCount <= 0.|
|**Tiền điều kiện (Pre-**<br>**conditions)**|Hub đã được cấu hình capacity và availableSpots hợp lệ.|
|**Hậu điều kiện (Post-**<br>**conditions)**|Không làm thay đổi trạng thái Hub.|
|**Luồng thuật toán**<br>**(Pseudo-code)**|1. Nếu requiredCount <= 0 -> ném IllegalArgumentException.<br>2. Trả về (this.status == HubStatus.ACTIVE) &&<br>(this.availableSpots >= requiredCount).|



### **_1.15.2. MobilityHub.adjustExpectedCapacity(delta)_** 

|**Thuộc tính**|**Nội dung chi tiết**|
|---|---|
|**Tênphương thức**|MobilityHub.adjustExpectedCapacity(delta)|
|**Mục đích**|Cập nhật số chỗ đỗ trống dự kiến tại Hub nguồn (+count) và Hub<br>đích(-count)khi tạo hoặc hủylệnh điềuphối.|
|**Tham số đầu vào**<br>**(@param)**|delta: int – Độ biến thiên số chỗ trống (dương khi xe rời đi, âm khi<br>xe được điềuphối đến).|
|**Giá trị trả về(@return)**|void – Khôngtrả vềgiá trị.|
|**Ngoại lệ (@exception)**|HubCapacityExceededException – Khi availableSpots + delta < 0<br>hoặc > capacity.|
|**Tiền điều kiện (Pre-**<br>**conditions)**|Hub đang ở trạng thái ACTIVE.|
|**Hậu điều kiện (Post-**<br>**conditions)**|Thuộc tính availableSpots của Hub được cập nhật nằm trong đoạn<br>[0, capacity].|



|**Thuộc tính**|**Nội dung chi tiết**|
|---|---|
||1. Tính nextSpots = this.availableSpots + delta.<br>|
|**Luồng thuật toán**|2. Nếu nextSpots < 0 hoặc nextSpots > this.capacity -> ném|
|**(Pseudo-code)**|HubCapacityExceededException.<br>3. Gán this.availableSpots = nextSpots.|



### **_1.15.3. MobilityHub.isolateHub()_** 

|**Thuộc tính**|**Nội dung chi tiết**|
|---|---|
|**Tênphương thức**|MobilityHub.isolateHub()|
|**Mục đích**|Chuyển trạng thái Hub sang ISOLATED để cô lập giao dịch khi Hub<br>mất kết nối hoàn toàn, bảo vệ toàn mạnglưới(NFR05).|
|**Tham số đầu vào**<br>**(@param)**|Không có.|
|**Giá trị trả về(@return)**|void – Khôngtrả vềgiá trị.|
|**Ngoại lệ (@exception)**|Khôngcó.|
|**Tiền điều kiện (Pre-**<br>**conditions)**|Hệ thống xác nhận Hub bị mất kết nối hoàn toàn (UC12 – EX1).|
|**Hậu điều kiện (Post-**<br>**conditions)**|this.status = HubStatus.ISOLATED; mọi giao dịch mới tại Hub này<br>bị tạm ngưng.|
|**Luồng thuật toán**<br>**(Pseudo-code)**|1. Gán this.status = HubStatus.ISOLATED.|



### **_1.15.4. Resource.updateStatus(newStatus, timestamp)_** 

|**Thuộc tính**|**Nội dung chi tiết**|
|---|---|
|**Tênphương thức**|Resource.updateStatus(newStatus, timestamp)|
|**Mục đích**|Cập nhật trạng thái hiện hành và dấu thời gian cập nhật gần nhất cho<br>bất kỳtài nguyên nào(SharedVehicle, ChargingPort, ParkingSpot).|
|**Tham số đầu vào**<br>**(@param)**|newStatus: ResourceStatus – Trạng thái mới cần áp dụng.<br>timestamp: LocalDateTime – Mốc thờigian hiệu lực của cậpnhật.|
|**Giá trị trả về(@return)**|void – Khôngtrả vềgiá trị.|
|**Ngoại lệ (@exception)**|InvalidArgumentException – Khi newStatus hoặc timestampnull.|
|**Tiền điều kiện (Pre-**<br>**conditions)**|Đối tượng Resource tồn tại trong hệ thống.|
|**Hậu điều kiện (Post-**<br>**conditions)**|status = newStatus; lastUpdatedAt = timestamp.|
|**Luồng thuật toán**<br>**(Pseudo-code)**|1. Kiểm tra newStatus != null và timestamp != null.<br>2. Gán this.status = newStatus; this.lastUpdatedAt = timestamp.|



### **_1.15.5. Resource.isAvailable()_** 

|**Thuộc tính**|**Nội dung chi tiết**|
|---|---|
|**Tênphương thức**|Resource.isAvailable()|
|**Mục đích**|Kiểm tra nhanh tài nguyên hiện có đang sẵn sàng để phục vụ đặt chỗ<br>hoặc điềuphối haykhông.|
|**Tham số đầu vào**<br>**(@param)**|Không có.|



|**Thuộc tính**|**Nội dung chi tiết**|
|---|---|
|**Giá trị trả về(@return)**|boolean – Trả về true nếu status == ResourceStatus.AVAILABLE.|
|**Ngoại lệ (@exception)**|Khôngcó.|
|**Tiền điều kiện (Pre-**<br>**conditions)**|Đối tượng Resource đã được khởi tạo.|
|**Hậu điều kiện (Post-**<br>**conditions)**|Không thay đổi trạng thái tài nguyên.|
|**Luồng thuật toán**<br>**(Pseudo-code)**|1. Trả về (this.status == ResourceStatus.AVAILABLE).|



### **_1.15.6. SharedVehicle.updateTelemetry(status, batteryLevel, timestamp)_** 

|**Thuộc tính**|**Nội dung chi tiết**|
|---|---|
|**Tênphương thức**|SharedVehicle.updateTelemetry(status, batteryLevel, timestamp)|
|**Mục đích**|Cập nhật đồng bộ trạng thái vận hành, mức pin (%) và dấu thời gian<br>mới nhất chophươngtiện điện dùngchungtừgói tin UC16.|
|**Tham số đầu vào**<br>**(@param)**|status: ResourceStatus – Trạng thái mới của xe.<br>batteryLevel: double – Mức pin hiện tại (0..100).<br>timestamp: LocalDateTime – Thời điểmghi nhận telemetry.|
|**Giá trị trả về(@return)**|void – Khôngtrả vềgiá trị.|
|**Ngoại lệ (@exception)**|IllegalArgumentException – Khi batteryLevel < 0 hoặc > 100.|
|**Tiền điều kiện (Pre-**<br>**conditions)**|Gói tin đã vượt qua bước kiểm tra cấu trúc và chống gói trễ<br>(NFR08).|
|**Hậu điều kiện (Post-**<br>**conditions)**|status, batteryLevel và lastUpdatedAt của SharedVehicle được cập<br>nhật đồngbộ.|
|**Luồng thuật toán**<br>**(Pseudo-code)**|1. Nếu batteryLevel < 0 || batteryLevel > 100 -> ném<br>IllegalArgumentException.<br>2. Gọi super.updateStatus(status, timestamp).<br>3. Gán this.batteryLevel = batteryLevel.|



### **_1.15.7. AuditLog.record(actorId, action, targetId, details)_** 

|**Thuộc tính**|**Nội dung chi tiết**|
|---|---|
|**Tênphương thức**|AuditLog.record(actorId, action, targetId, details)|
|**Mục đích**|Tạo và lưu trữ bản ghi nhật ký kiểm toán phục vụ truy vết các thao<br>tác quan trọng (điều phối, tạm ngưng/khôi phục sự cố, lọc gói trễ) tối<br>thiểu 90 ngày (NFR11).|
|**Tham số đầu vào**<br>**(@param)**|actorId: String – Mã tác nhân thực hiện (Operator ID hoặc<br>SYSTEM/SIMULATOR).<br>action: String – Tên hành động nghiệp vụ.<br>targetId: String – Mã đối tượng bị tác động.<br>details: String– Thôngtin chi tiết thao tác.|
|**Giá trị trả về(@return)**|AuditLog– Đối tượngbảnghi AuditLogđã được lưu bền vững.|
|**Ngoại lệ (@exception)**|PersistenceException – Xảy ra khi không thể ghi log vào cơ sở dữ<br>liệu.|
|**Tiền điều kiện (Pre-**<br>**conditions)**|Thông tin tác nhân và hành động hợp lệ.|



|**Thuộc tính**|**Nội dung chi tiết**|
|---|---|
|**Hậu điều kiện (Post-**<br>**conditions)**|Một bản ghi AuditLog mới với timestamp = now() được lưu trữ tối<br>thiểu 90 ngày.|
|**Luồng thuật toán**|1. Tạo đối tượng log = new AuditLog(UUID, actorId, action,<br>targetId, details, now()).|
|**(Pseudo-code)**|2. Lưu log vào kho lưu trữ AuditLog (retention >= 90 days).<br>3. Trả về log.|



### **_1.15.8. NotificationService.sendNotification(recipientId, content)_** 

|**Thuộc tính**|**Nội dung chi tiết**|
|---|---|
|**Tênphương thức**|NotificationService.sendNotification(recipientId, content)|
|**Mục đích**|Gửi thông báo nghiệp vụ ra ngoài hệ thống tới đội ngũ vận chuyển<br>thực địa(UC11)hoặc Sinh viên bị hủyđơn do sự cố bảo trì(UC12).|
|**Tham số đầu vào**<br>**(@param)**|recipientId: String – Mã người nhận hoặc nhóm nhận thông báo.<br>content: String– Nội dungthôngbáo.|
|**Giá trị trả về (@return)**|boolean – Trả về true nếu dịch vụ thông báo tiếp nhận gửi thành<br>công, false nếugửi thất bại.|
|**Ngoại lệ (@exception)**|Không ném ngoại lệ chặn luồng nghiệp vụ chính; lỗi gửi được ghi<br>nhận để thử lại.|
|**Tiền điều kiện (Pre-**<br>**conditions)**|Giao dịch nghiệp vụ chính (tạo lệnh điều phối hoặc tạm ngưng tài<br>nguyên)đã commit thành công.|
|**Hậu điều kiện (Post-**<br>**conditions)**|Thông báo được chuyển qua kênh tương ứng tới người nhận; nếu lỗi,<br>hệ thống ghi logđể xử lýbù.|
|**Luồng thuật toán**<br>**(Pseudo-code)**|1. Đóng gói payload thông báo gồm recipientId, content và<br>timestamp.<br>2. Gọi API của hệ thống Notification Service bên ngoài thông qua<br>Notify Adapter.<br>3. Nếu phản hồi HTTP 2xx -> trả về true; ngược lại ghi log lỗi tích<br>hợpvà trả về false.|



### **_1.15.9. RealtimeGateway.broadcastResourceUpdate(resourceId, status, updatedAt)_** 

|**Thuộc tính**|**Nội dung chi tiết**|
|---|---|
|**Tên phương thức**|RealtimeGateway.broadcastResourceUpdate(resourceId, status,<br>updatedAt)|
|**Mục đích**|Đẩy tín hiệu cập nhật trạng thái tài nguyên theo thời gian thực qua<br>WebSocket/SSE tới các giao diện Mobile App và Web Dashboard<br>đangkết nối(NFR02 <= 15giây).|
|**Tham số đầu vào**<br>**(@param)**|resourceId: String – Mã tài nguyên vừa thay đổi trạng thái.<br>status: ResourceStatus – Trạng thái mới nhất.<br>updatedAt: LocalDateTime – Thời điểm cậpnhật hiệu lực.|
|**Giá trị trả về(@return)**|void – Khôngtrả vềgiá trị.|
|**Ngoại lệ (@exception)**|Không ném ngoại lệ ra luồng ingestion; lỗi kết nối client đơn lẻ bị bỏ<br>qua và tự độngdọn session.|
|**Tiền điều kiện (Pre-**<br>**conditions)**|Dữ liệu trạng thái mới đã được cập nhật thành công vào Operational<br>DB.|



|**Thuộc tính**|**Nội dung chi tiết**|
|---|---|
|**Hậu điều kiện (Post-**<br>**conditions)**|Tất cả client đang đăng ký kênh cập nhật nhận được sự kiện trạng<br>thái mới trongvòng<= 15giây.|
||1. Tạo thông điệp sự kiện JSON {resourceId, status, updatedAt}.|
|**Luồng thuật toán**|<br>2. Phát sự kiện tới các kênh/topic WebSocket và SSE đang hoạt|
|**(Pseudo-code)**|động.<br>3. Ghi nhận thời điểmphát để theo dõi SLA <= 15giây (NFR02).|



# **II. Kịch bản kiểm thử (Test Case)** 

## **2.1. Test case cho UC1 – Tìm phương tiện và Hub phù hợp** 

### **_2.1.1. TC_UC01_01 – Ngoại lệ (AF3) - Không có kết quả phù hợp với tiêu chí tìm kiếm._** 

|**Trường thông tin**|**Đặc tả kịch bản**|
|---|---|
|Test Case ID|TC_UC01_01|
|Use Case liênquan|UC1 - Tìmphươngtiện và Hubphù hợp|
|Mô tả kịch bản|Ngoại lệ(AF3)- Khôngcó kếtquảphù hợpvới tiêu chí tìm kiếm.|
|Tiền điều kiện<br>(Preconditions)|Vị trí xác định được; không có phương tiện khả dụng nào trong bán<br>kính tìm kiếm.|
|Dữ liệu đầu vào (Input<br>Data)|location=(10.762622, 106.660172); radiusKm=0.1;<br>searchType=VEHICLE; vehicleType="E-bike";<br>minBatteryLevel=20|
|Kết quả mong đợi<br>(Expected Result)|Hệ thống trả về danh sách rỗng và thông báo không có kết quả phù<br>hợp; tiêu chí tìm kiếm được giữ nguyên trên giao diện để Sinh viên<br>điều chỉnh; khôngthayđổi dữ liệu.|
|Kết quả thực tế (Actual /<br>Status)|Pending|



### **_2.1.2. TC_UC01_02 – Ngoại lệ (EX1) - Không xác định được vị trí tìm kiếm._** 

|**Trường thông tin**|**Đặc tả kịch bản**|
|---|---|
|Test Case ID|TC_UC01_02|
|Use Case liênquan|UC1 - Tìmphươngtiện và Hubphù hợp|
|Mô tả kịch bản|Ngoại lệ(EX1)- Khôngxác định được vị trí tìm kiếm.|
|Tiền điều kiện<br>(Preconditions)|Sinh viên từ chối cấp quyền định vị và không chọn vị trí thủ công<br>trên bản đồ.|
|Dữ liệu đầu vào (Input<br>Data)|location=null; radiusKm=2; searchType=VEHICLE|
|Kết quả mong đợi<br>(Expected Result)|Hệ thống ném InvalidLocationException, hiển thị thông báo lỗi và<br>cho phép thử lại hoặc chuyển sang chọn vị trí thủ công (nhánh 3a);<br>khôngthực hiện truyvấn dữ liệu.|
|Kết quả thực tế (Actual /<br>Status)|Pending|



### **_2.1.3. TC_UC01_03 – Ngoại lệ (EX2) - Tiêu chí tìm kiếm không hợp lệ._** 

|**Trường thông tin**|**Đặc tả kịch bản**|
|---|---|
|Test Case ID|TC_UC01_03|
|Use Case liênquan|UC1 - Tìmphươngtiện và Hubphù hợp|
|Mô tả kịch bản|Ngoại lệ(EX2)- Tiêu chí tìm kiếm khônghợplệ.|
|Tiền điều kiện<br>(Preconditions)|Vị trí xác định được; giao diện tìm kiếm đang hiển thị.|
|Dữ liệu đầu vào (Input|location=(10.762622, 106.660172); radiusKm=-5;|
|Data)|minBatteryLevel=150|



|**Trường thông tin**|**Đặc tả kịch bản**|
|---|---|
|Kết quả mong đợi<br>(Expected Result)|Hệ thống ném InvalidSearchCriteriaException, chỉ rõ các trường cần<br>chỉnh sửa (bán kính phải lớn hơn 0, mức pin trong khoảng 0-100) và<br>yêu cầu nhậplại; khôngtruyvấn xuốngtầngdữ liệu.|
|Kết quả thực tế (Actual /<br>Status)|Pending|



### **_2.1.4. TC_UC01_04 – Ngoại lệ (EX3) - Map API không khả dụng._** 

|**Trường thông tin**|**Đặc tả kịch bản**|
|---|---|
|Test Case ID|TC_UC01_04|
|Use Case liênquan|UC1 - Tìmphươngtiện và Hubphù hợp|
|Mô tả kịch bản|Ngoại lệ(EX3)- MapAPI khôngkhả dụng.|
|Tiền điều kiện<br>(Preconditions)|Dịch vụ Map API bị timeout hoặc trả về lỗi kết nối; dữ liệu Hub vẫn<br>truyxuất được.|
|Dữ liệu đầu vào (Input<br>Data)|location=(10.762622, 106.660172); radiusKm=2; searchType=HUB|
|Kết quả mong đợi<br>(Expected Result)|Hệ thống thông báo lỗi bản đồ và chuyển sang hiển thị danh sách<br>Hub theo khu vực hoặc toạ độ đã lưu; chức năng tìm kiếm vẫn trả<br>kếtquả dạngdanh sách.|
|Kết quả thực tế (Actual /<br>Status)|Pending|



### **_2.1.5. TC_UC01_05 – Ngoại lệ (EX4) - Không truy xuất được dữ liệu phương tiện/Hub._** 

|**Trường thông tin**|**Đặc tả kịch bản**|
|---|---|
|Test Case ID|TC_UC01_05|
|Use Case liênquan|UC1 - Tìmphươngtiện và Hubphù hợp|
|Mô tả kịch bản|Ngoại lệ(EX4)- Khôngtruyxuất được dữ liệuphươngtiện/Hub.|
|Tiền điều kiện<br>(Preconditions)|Kết nối tới cơ sở dữ liệu bị gián đoạn trong lúc tìm kiếm.|
|Dữ liệu đầu vào (Input<br>Data)|location=(10.762622, 106.660172); radiusKm=2;<br>searchType=VEHICLE; vehicleType="E-bike";<br>minBatteryLevel=20|
|Kết quả mong đợi<br>(Expected Result)|Hệ thống ném DataSourceUnavailableException, thông báo lỗi, giữ<br>lại tiêu chí đã nhập và cho phép Sinh viên thử lại; không hiển thị kết<br>quả sai lệch.|
|Kết quả thực tế (Actual /<br>Status)|Pending|



## **2.2. Test case cho UC2 – Xem trạng thái phương tiện và Hub** 

### **_2.2.1. TC_UC02_01 – Ngoại lệ (EX2) - Tài nguyên không tồn tại hoặc đã ngừng hoạt động._** 

|**Trường thông tin**|**Đặc tả kịch bản**|
|---|---|
|Test Case ID|TC_UC02_01|
|Use Case liênquan|UC2 - Xem trạngtháiphươngtiện và Hub|
|Mô tả kịch bản|Ngoại lệ(EX2)- Tài nguyên khôngtồn tại hoặc đã ngừnghoạt động.|



|**Trường thông tin**|**Đặc tả kịch bản**|
|---|---|
|Tiền điều kiện<br>(Preconditions)|resourceId không tồn tại trong hệ thống.|
|Dữ liệu đầu vào (Input<br>Data)|resourceType=VEHICLE; resourceId="V-9999-INVALID"|
|Kết quả mong đợi<br>(Expected Result)|Hệ thống ném ResourceNotFoundException, thông báo và đưa Sinh<br>viên về danh sách tìm kiếm; khôngtrả dữ liệu trạngthái nào.|
|Kết quả thực tế (Actual /<br>Status)|Pending|



### **_2.2.2. TC_UC02_02 – Ngoại lệ (EX1) - Chưa chọn tài nguyên hợp lệ._** 

|**Trường thông tin**|**Đặc tả kịch bản**|
|---|---|
|Test Case ID|TC_UC02_02|
|Use Case liênquan|UC2 - Xem trạngtháiphươngtiện và Hub|
|Mô tả kịch bản|Ngoại lệ(EX1)- Chưa chọn tài nguyên hợplệ.|
|Tiền điều kiện<br>(Preconditions)|Sinh viên mở chức năng xem trạng thái nhưng chưa chọn phương<br>tiện hoặc Hub.|
|Dữ liệu đầu vào (Input<br>Data)|resourceType=VEHICLE; resourceId=""|
|Kết quả mong đợi<br>(Expected Result)|Hệ thống ném InvalidArgumentException và yêu cầu Sinh viên chọn<br>phươngtiện hoặc Hub trước khi tiếptục; khôngtruyvấn dữ liệu.|
|Kết quả thực tế (Actual /<br>Status)|Pending|



### **_2.2.3. TC_UC02_03 – Ngoại lệ (EX3) - Không truy xuất được dữ liệu trạng thái._** 

|**Trường thông tin**|**Đặc tả kịch bản**|
|---|---|
|Test Case ID|TC_UC02_03|
|Use Case liênquan|UC2 - Xem trạngtháiphươngtiện và Hub|
|Mô tả kịch bản|Ngoại lệ(EX3)- Khôngtruyxuất được dữ liệu trạngthái.|
|Tiền điều kiện<br>(Preconditions)|resourceId hợp lệ; kết nối tới cơ sở dữ liệu bị gián đoạn.|
|Dữ liệu đầu vào (Input<br>Data)|resourceType=HUB; resourceId="HUB-001"|
|Kết quả mong đợi<br>(Expected Result)|Hệ thống ném DataSourceUnavailableException, thông báo lỗi, giữ<br>lại tài nguyên đangchọn và chophépSinh viên thử lại.|
|Kết quả thực tế (Actual /<br>Status)|Pending|



**_2.2.4. TC_UC02_04 – Biên (EX4) - Dữ liệu trạng thái quá cũ._** 

|**Trường thông tin**|**Đặc tả kịch bản**|
|---|---|
|Test Case ID|TC_UC02_04|
|Use Case liênquan|UC2 - Xem trạngtháiphươngtiện và Hub|
|Mô tả kịch bản|Biên(EX4)- Dữ liệu trạngtháiquá cũ.|



|**Trường thông tin**|**Đặc tả kịch bản**|
|---|---|
|Tiền điều kiện<br>(Preconditions)|Tài nguyên tồn tại; thời điểm cập nhật gần nhất (lastUpdatedAt) cũ<br>hơn ngưỡngSTALE_THRESHOLD.|
|Dữ liệu đầu vào (Input<br>Data)|resourceType=VEHICLE; resourceId="V-0012"; lastUpdatedAt =<br>thời điểm hiện tại - 30phút|
|Kết quả mong đợi<br>(Expected Result)|Hệ thống vẫn hiển thị thời điểm cập nhật gần nhất nhưng đánh dấu<br>dữ liệu chưa đáng tin cậy (stale) và không khẳng định phương tiện<br>còn khả dụng.|
|Kết quả thực tế (Actual /<br>Status)|Pending|



### **_2.2.5. TC_UC02_05 – Biên (AF4) - Tài nguyên đang không khả dụng._** 

|**Trường thông tin**|**Đặc tả kịch bản**|
|---|---|
|Test Case ID|TC_UC02_05|
|Use Case liênquan|UC2 - Xem trạngtháiphươngtiện và Hub|
|Mô tả kịch bản|Biên(AF4)- Tài nguyên đangkhôngkhả dụng.|
|Tiền điều kiện<br>(Preconditions)|Phương tiện tồn tại và đang ở trạng thái "Đã đặt" bởi Sinh viên khác.|
|Dữ liệu đầu vào (Input<br>Data)|resourceType=VEHICLE; resourceId="V-0020"|
|Kết quả mong đợi<br>(Expected Result)|Hệ thống vẫn hiển thị trạng thái hiện tại ("Đã đặt") kèm thời điểm<br>cập nhật, không báo lỗi, và cho phép Sinh viên chọn tài nguyên<br>khác; khôngthayđổi dữ liệu đặt xe.|
|Kết quả thực tế (Actual /<br>Status)|Pending<br>2.4. Test case cho UC4 - Đặt chỗ đỗ xe|



## **2.3. Test case cho UC3 – Đặt xe** 

### **_2.3.1. TC_UC03_01 – Đặt xe thành công_** 

|**Trường thông tin**|**Đặc tả kịch bản**|
|---|---|
|Test Case ID|TC_UC03_01|
|Use Case liênquan|UC3 – Đặt xe|
|Mô tả kịch bản|Đặt xe thành công|
|Tiền điều kiện<br>(Preconditions)|Sinh viên đã đăng nhập; xe được chọn đang khả dụng tại Hub hoạt<br>động.|
|Dữ liệu đầu vào (Input<br>Data)|Người dùng: sinh viên An.<br>Phương tiện: xe điện số 1 tại Hub A.<br>Thao tác: chọn xe và xác nhận đặt.|
|Kết quả mong đợi<br>(Expected Result)|1. Tạo một đơn thuộc sinh viên An.<br>2. Xe chuyển sang trạng thái đã giữ.<br>3. Lưu lịch sử và hiển thị xác nhận đặt xe.|
|Kếtquả thực tế / Status|Pending– Chưa thực hiện kiểm thử.|



### **_2.3.2. TC_UC03_02 – Hủy trước khi xác nhận_** 

|**Trường thông tin**|**Đặc tả kịch bản**|
|---|---|
|Test Case ID|TC_UC03_02|
|Use Case liênquan|UC3 – Đặt xe|
|Mô tả kịch bản|Hủytrước khi xác nhận|
|Tiền điều kiện<br>(Preconditions)|Sinh viên đang xem hộp thoại đặt xe; chưa gửi yêu cầu lưu.|
|Dữ liệu đầu vào (Input<br>Data)|Xe điện số 1 tại Hub A.<br>Thao tác: chọn Hủy.|
|Kết quả mong đợi<br>(Expected Result)|1. Đóng hộp thoại và xóa lựa chọn tạm.<br>2. Khôngtạo đơn; trạngthái xe khôngđổi.|
|Kếtquả thực tế / Status|Pending– Chưa thực hiện kiểm thử.|



### **_2.3.3. TC_UC03_03 – Nhiều người cùng đặt một xe_** 

|**Trường thông tin**|**Đặc tả kịch bản**|
|---|---|
|Test Case ID|TC_UC03_03|
|Use Case liênquan|UC3 – Đặt xe|
|Mô tả kịch bản|Nhiều người cùngđặt một xe|
|Tiền điều kiện<br>(Preconditions)|Hai sinh viên An và Bình đã đăng nhập; chỉ có xe điện số 1 đang khả<br>dụng.|
|Dữ liệu đầu vào (Input<br>Data)|Tài nguyên: cùng xe điện số 1.<br>Thao tác: gửi hai xác nhận đồng thời; lặp lại 10 lần, khôi phục xe<br>trước mỗi lần.|
|Kết quả mong đợi<br>(Expected Result)|1. Mỗi lần chỉ có một đơn đặt xe thành công.<br>2. Người còn lại nhận thông báo xe không khả dụng.<br>3. Không có hai đơn cùng giữ xe; lịch sử phản ánh đúng đơn thành<br>công.|
|Kếtquả thực tế / Status|Pending– Chưa thực hiện kiểm thử.|



### **_2.3.4. TC_UC03_04 – Lỗi khi lưu đơn_** 

|**Trường thông tin**|**Đặc tả kịch bản**|
|---|---|
|Test Case ID|TC_UC03_04|
|Use Case liênquan|UC3 – Đặt xe|
|Mô tả kịch bản|Lỗi khi lưu đơn|
|Tiền điều kiện<br>(Preconditions)|Xe điện số 1 khả dụng; mô phỏng lỗi lưu trước khi giao dịch hoàn<br>tất.|
|Dữ liệu đầu vào (Input<br>Data)|Sinh viên An chọn xe điện số 1 và xác nhận đặt.|
|Kết quả mong đợi<br>(Expected Result)|1. Thông báo chưa đặt xe thành công.<br>2. Không lưu đơn dở dang; xe vẫn khả dụng.<br>3. Chỉ cho thử lại sau khi xác địnhyêu cầu trước chưa được lưu.|
|Kếtquả thực tế / Status|Pending– Chưa thực hiện kiểm thử.|



## **2.4. Test case cho UC4 – Đặt chỗ đỗ xe** 

### **_2.4.1. TC_UC04_01 – Đặt chỗ đỗ thành công_** 

|**Trường thông tin**|**Đặc tả kịch bản**|
|---|---|
|Test Case ID|TC_UC04_01|
|Use Case liênquan|UC4 – Đặt chỗ đỗ xe|
|Mô tả kịch bản|Đặt chỗ đỗ thành công|
|Tiền điều kiện<br>(Preconditions)|Sinh viên An đã đăng nhập; chỗ đỗ số 1 tại Hub A trống và chưa<br>đượcgiữ trongkhung giờ chọn.|
|Dữ liệu đầu vào (Input<br>Data)|Chỗ đỗ: số 1 tại Hub A.<br>Thời gian: 09:00–10:00 ngày 01/12/2026.<br>Thao tác: chọn chỗ và xác nhận.|
|Kết quả mong đợi<br>(Expected Result)|1. Lưu đơn thuộc sinh viên An và giữ đúng khung giờ.<br>2. Hiển thị thôngtin đặt chỗ;ghi lịch sử.|
|Kếtquả thực tế / Status|Pending– Chưa thực hiện kiểm thử.|



### **_2.4.2. TC_UC04_02 – Khoảng thời gian không hợp lệ_** 

|**Trường thông tin**|**Đặc tả kịch bản**|
|---|---|
|Test Case ID|TC_UC04_02|
|Use Case liênquan|UC4 – Đặt chỗ đỗ xe|
|Mô tả kịch bản|Khoảngthờigian khônghợplệ|
|Tiền điều kiện<br>(Preconditions)|Sinh viên đã đăng nhập và chọn chỗ đỗ.|
|Dữ liệu đầu vào (Input<br>Data)|Lần 1: bắt đầu 10:00, kết thúc 09:00.<br>Lần 2: bắt đầu và kết thúc đều 10:00.<br>Thao tác: xác nhận từnglần độc lập.|
|Kết quả mong đợi<br>(Expected Result)|1. Từ chối cả hai khoảng thời gian.<br>2. Yêu cầu sửa thờigian; khôngtạo đơn hoặcgiữ chỗ.|
|Kếtquả thực tế / Status|Pending– Chưa thực hiện kiểm thử.|



### **_2.4.3. TC_UC04_03 – Đặt chỗ đỗ đồng thời bị trùng giờ_** 

|**Trường thông tin**|**Đặc tả kịch bản**|
|---|---|
|Test Case ID|TC_UC04_03|
|Use Case liênquan|UC4 – Đặt chỗ đỗ xe|
|Mô tả kịch bản|Đặt chỗ đỗ đồngthời bị trùng giờ|
|Tiền điều kiện<br>(Preconditions)|Hai sinh viên đã đăng nhập; chỗ đỗ số 1 tại Hub A chưa có đơn.|
|Dữ liệu đầu vào (Input<br>Data)|An đặt 09:00–10:00; Bình đặt 09:30–10:30 cùng ngày, cùng chỗ.<br>Thao tác:gửi đồngthời; lặplại 10 lần với dữ liệu được khôiphục.|
|Kết quả mong đợi<br>(Expected Result)|1. Mỗi lần chỉ một yêu cầu thành công.<br>2. Yêu cầu còn lại nhận thông báo trùng khung giờ.<br>3. Khônglưu hai đơn có khoảng giữ chỗgiao nhau.|
|Kếtquả thực tế / Status|Pending– Chưa thực hiện kiểm thử.|



### **_2.4.4. TC_UC04_04 – Chưa đăng nhập hoặc không có quyền_** 

|**Trường thông tin**|**Đặc tả kịch bản**|
|---|---|
|Test Case ID|TC_UC04_04|
|Use Case liênquan|UC4 – Đặt chỗ đỗ xe|
|Mô tả kịch bản|Chưa đăngnhậphoặc khôngcóquyền|
|Tiền điều kiện<br>(Preconditions)|Người dùng chưa có phiên; kiểm tra thêm một tài khoản vận hành<br>khôngcóquyền sinh viên.|
|Dữ liệu đầu vào (Input<br>Data)|Chỗ đỗ số 1; thời gian 09:00–10:00.<br>Thao tác:gửiyêu cầu đặt bằngtừngtài khoản.|
|Kết quả mong đợi<br>(Expected Result)|1. Người chưa đăng nhập được yêu cầu xác thực.<br>2. Tài khoản thiếu quyền bị từ chối.<br>3. Khônglưu đơn trongcả hai trườnghợp.|
|Kếtquả thực tế / Status|Pending– Chưa thực hiện kiểm thử.|



## **2.5. Test case cho UC5 – Nhận phương tiện** 

### **_2.5.1. TC_UC05_01 – Nhận xe thành công_** 

|**Trường thông tin**|**Đặc tả kịch bản**|
|---|---|
|Test Case ID|TC_UC05_01|
|Use Case liênquan|UC5 – Nhậnphươngtiện|
|Mô tả kịch bản|Nhận xe thành công|
|Tiền điều kiện<br>(Preconditions)|An có đơn đặt xe còn hiệu lực tại Hub A; xe đang được giữ và không<br>có sự cố.|
|Dữ liệu đầu vào (Input<br>Data)|Đơn: đơn đặt xe điện số 1 của An.<br>Hub nhận: Hub A.<br>Thao tác: xác nhận nhận xe môphỏng.|
|Kết quả mong đợi<br>(Expected Result)|1. Xe chuyển sang đang sử dụng; đơn chuyển sang đã nhận.<br>2. Lưu người nhận, thời gian nhận và lịch sử.<br>3. Hiển thị thành công; khôngđiều khiển khóa vật lý.|
|Kếtquả thực tế / Status|Pending– Chưa thực hiện kiểm thử.|



### **_2.5.2. TC_UC05_02 – Đơn không hợp lệ hoặc thuộc người khác_** 

|**Trường thông tin**|**Đặc tả kịch bản**|
|---|---|
|Test Case ID|TC_UC05_02|
|Use Case liênquan|UC5 – Nhậnphươngtiện|
|Mô tả kịch bản|Đơn khônghợplệ hoặc thuộc người khác|
|Tiền điều kiện<br>(Preconditions)|An đã đăng nhập; có một đơn thuộc sinh viên Bình.|
|Dữ liệu đầu vào (Input<br>Data)|Lần 1: nhập mã đơn không tồn tại.<br>Lần 2: dùng mã đơn của Bình.<br>Thao tác: xác nhận nhận xe.|
|Kết quả mong đợi<br>(Expected Result)|1. Từ chối cả hai yêu cầu.<br>2. Không tiết lộ chi tiết đơn của Bình.<br>3. Khôngđổi trạngthái xe hoặc đơn.|
|Kếtquả thực tế / Status|Pending– Chưa thực hiện kiểm thử.|



### **_2.5.3. TC_UC05_03 – Kiểm tra thời hạn nhận xe_** 

|**Trường thông tin**|**Đặc tả kịch bản**|
|---|---|
|Test Case ID|TC_UC05_03|
|Use Case liênquan|UC5 – Nhậnphươngtiện|
|Mô tả kịch bản|Kiểm tra thời hạn nhận xe|
|Tiền điều kiện<br>(Preconditions)|Đơn của An có hiệu lực từ 08:00 đến 08:15; xe không có sự cố.|
|Dữ liệu đầu vào (Input<br>Data)|Thử độc lập tại 08:14:59, 08:15:00 và 08:15:01.<br>Thao tác: xác nhận nhận xe tại mỗi thời điểm.|
|Kết quả mong đợi<br>(Expected Result)|1. Trước 08:15 được nhận xe.<br>2. Từ đúng 08:15 trở đi, thông báo đơn hết hiệu lực và không ghi<br>nhận nhận xe.Quyước biên thờigian cần thốngnhất trongnhóm.|
|Kếtquả thực tế / Status|Pending– Chưa thực hiện kiểm thử.|



### **_2.5.4. TC_UC05_04 – Lỗi cập nhật sau thao tác nhận_** 

|**Trường thông tin**|**Đặc tả kịch bản**|
|---|---|
|Test Case ID|TC_UC05_04|
|Use Case liênquan|UC5 – Nhậnphươngtiện|
|Mô tả kịch bản|Lỗi cậpnhật sau thao tác nhận|
|Tiền điều kiện<br>(Preconditions)|Đã lưu thông tin nhận xe mô phỏng; gây lỗi ở bước cập nhật cuối.|
|Dữ liệu đầu vào (Input<br>Data)|An xác nhận nhận xe điện số 1.<br>Sau lỗi, Bình thử đặt lại chính xe đó.|
|Kết quả mong đợi<br>(Expected Result)|1. Không báo nhận xe hoàn tất.<br>2. Giữ thông tin nhận và chặn Bình đặt lại xe.<br>3. Chuyển vận hành kiểm tra, khôngtựgiảiphóngxe.|
|Kếtquả thực tế / Status|Pending– Chưa thực hiện kiểm thử.|



## **2.6. Test case cho UC6 – Trả phương tiện** 

### **_2.6.1. TC_UC06_01 – Thành công: trả xe pin thấp, xe chuyển sang "Chờ sạc"._** 

|**Trường thông tin**|**Đặc tả kịch bản**|
|---|---|
|Test Case ID|TC_UC06_01|
|Use Case liênquan|UC6: Trảphươngtiện|
|Mô tả kịch bản|Thành công: trả xepin thấp, xe chuyển sang"Chờ sạc".|
|Tiền điều kiện<br>(Preconditions)|SV01 đã đăng nhập. Xe V001 có lượt mượn IN_USE của SV01, pin<br>15%, khônglỗi kỹthuật. Hub A còn chỗ tiếpnhận.|
|Dữ liệu đầu vào (Input<br>Data)|studentId = SV01, vehicleId = V001, hubId = HubA|
|Kết quả mong đợi<br>(Expected Result)|ReturnRecord.resultingStatus = WAITING_CHARGE.<br>RentalRecord = ENDED. AuditLog ghi thời điểm, người trả, xe và<br>Hub nhận. Hiển thị xác nhận trả xe thành công.|
|Kết quả thực tế (Actual /|Pending|
|Status)|2.6. Test case cho UC6 - Trảphươngtiện|



### **_2.6.2. TC_UC06_02 – Ngoại lệ: xe không có lượt mượn hợp lệ._** 

|**Trường thông tin**|**Đặc tả kịch bản**|
|---|---|
|Test Case ID|TC_UC06_02|
|Use Case liênquan|UC6: Trảphươngtiện|
|Mô tả kịch bản|Ngoại lệ: xe khôngcó lượt mượn hợplệ.|
|Tiền điều kiện<br>(Preconditions)|SV01 đã đăng nhập. Xe V002 ở trạng thái AVAILABLE, không có<br>RentalRecord IN_USE.|
|Dữ liệu đầu vào (Input<br>Data)|studentId = SV01, vehicleId = V002, hubId = HubA|
|Kết quả mong đợi<br>(Expected Result)|Ném InvalidReturnException. Không có ReturnRecord, AuditLog<br>hay thay đổi trạng thái xe. Hiển thị thông báo xe/lượt mượn không<br>hợplệ và hướngdẫn liên hệ đơn vị vận hành.|
|Kết quả thực tế (Actual /<br>Status)|Pending|



### **_2.6.3. TC_UC06_03 – Ngoại lệ: gửi thông báo thất bại nhưng việc trả xe vẫn thành công._** 

|**Trường thông tin**|**Đặc tả kịch bản**|
|---|---|
|Test Case ID|TC_UC06_03|
|Use Case liênquan|UC6: Trảphươngtiện|
|Mô tả kịch bản|Ngoại lệ:gửi thôngbáo thất bại nhưngviệc trả xe vẫn thành công.|
|Tiền điều kiện<br>(Preconditions)|Như TC_UC06_01. NotificationService được giả lập trả lỗi.|
|Dữ liệu đầu vào (Input<br>Data)|studentId = SV01, vehicleId = V001, hubId = HubA|
|Kết quả mong đợi<br>(Expected Result)|returnVehicle không ném ngoại lệ. RentalRecord = ENDED, trạng<br>thái xe đã cập nhật, ReturnRecord đã lưu. Lỗi thông báo được ghi<br>log để xử lý lại. Sinh viên vẫn thấy xác nhận trả xe thành công.<br>2.7. Test case cho UC7 - Đăngkýsạc|



## **2.7. Test case cho UC7 – Đăng ký sạc** 

### **_2.7.1. TC_UC07_01 – Ngoại lệ: khung giờ đã được người khác đặt._** 

|**Trường thông tin**|**Đặc tả kịch bản**|
|---|---|
|Test Case ID|TC_UC07_01|
|Use Case liênquan|UC7: Đăngkýsạc|
|Mô tả kịch bản|Ngoại lệ: khung giờ đã được người khác đặt.|
|Tiền điều kiện<br>(Preconditions)|Cổng P1 AVAILABLE. SV02 đã có đăng ký CONFIRMED cho P1,<br>14:00 đến 15:00.|
|Dữ liệu đầu vào (Input<br>Data)|studentId = SV01, vehicleId = V001, portId = P1, start = 14:00, end<br>= 15:00|
|Kết quả mong đợi<br>(Expected Result)|Ném SlotConflictException. Không tạo ChargingRegistration mới,<br>không ghi AuditLog thành công. Hiển thị xung đột và gợi ý cổng<br>hoặc khung giờ khác. P1 chỉ có đúng1 đăngkýtrongkhung giờ này.|
|Kết quả thực tế (Actual /<br>Status)|Pending|



### **_2.7.2. TC_UC07_02 – Race condition: hai sinh viên đăng ký cùng cổng, cùng khung giờ đồng thời._** 

|**Trường thông tin**|**Đặc tả kịch bản**|
|---|---|
|Test Case ID|TC_UC07_02|
|Use Case liênquan|UC7: Đăngkýsạc|
|Mô tả kịch bản|Race condition: hai sinh viên đăng ký cùng cổng, cùng khung giờ<br>đồngthời.|
|Tiền điều kiện<br>(Preconditions)|P1 AVAILABLE, chưa có đăng ký nào. Hai luồng (thread) bắt đầu<br>cùnglúc, mỗi luồngđãqua bước kiểm tra khả dụng.|
|Dữ liệu đầu vào (Input<br>Data)|Luồng A: SV01, V001, P1, 14:00, 15:00. Luồng B: SV02, V002, P1,<br>14:00, 15:00.|
|Kết quả mong đợi<br>(Expected Result)|Đúng một luồng nhận ChargingRegistration CONFIRMED, luồng<br>còn lại nhận SlotConflictException. CSDL chỉ có 1 đăng ký cho P1<br>trong khung giờ này, P1 chỉ bị giữ một lần. Lặp lại 100 lần vẫn<br>khôngcó lần nào tạo 2 đăngký.|
|Kết quả thực tế (Actual /<br>Status)|Pending|



### **_2.7.3. TC_UC07_03 – Thành công: đăng ký cổng còn trống._** 

|**Trường thông tin**|**Đặc tả kịch bản**|
|---|---|
|Test Case ID|TC_UC07_03|
|Use Case liênquan|UC7: Đăngkýsạc|
|Mô tả kịch bản|Thành công: đăngkýcổngcòn trống.|
|Tiền điều kiện<br>(Preconditions)|P1 AVAILABLE, không có đăng ký chồng lấn. V001 thuộc lượt<br>dùnghợplệ của SV01.|
|Dữ liệu đầu vào (Input<br>Data)|studentId = SV01, vehicleId = V001, portId = P1, start = 16:00, end<br>= 17:00|
|Kết quả mong đợi<br>(Expected Result)|Trả về ChargingRegistration (CONFIRMED). P1 được giữ cho<br>16:00 đến 17:00. AuditLog được ghi. Yêu cầu thông báo được<br>chuyển đến Hệ thống thông báo. Hiển thị xác nhận đăng ký.<br>2.8. Test case cho UC8 - Giám sát mạnglưới MobilityHub|
|Kết quả thực tế (Actual /<br>Status)|Pending|



## **2.8. Test case cho UC8 – Giám sát mạng lưới Mobility Hub** 

### **_2.8.1. TC_UC08_01 – Biên (EX4) - Một Hub có dữ liệu cấu hình không hợp lệ._** 

|**Trường thông tin**|**Đặc tả kịch bản**|
|---|---|
|Test Case ID|TC_UC08_01|
|Use Case liênquan|UC8 - Giám sát mạnglưới MobilityHub|
|Mô tả kịch bản|Biên(EX4)- Một Hub có dữ liệu cấu hình khônghợplệ.|
|Tiền điều kiện<br>(Preconditions)|Đã đăng nhập với vai trò Đơn vị vận hành; tồn tại 1 Hub thiếu thuộc<br>tính capacitytrongcấu hình.|
|Dữ liệu đầu vào (Input<br>Data)|filter=null (lấy toàn bộ mạng lưới)|



|**Trường thông tin**|**Đặc tả kịch bản**|
|---|---|
|Kết quả mong đợi|Dashboard vẫn hiển thị đúng các Hub hợp lệ; Hub lỗi cấu hình bị<br>|
|(Expected Result)|đánh dấu "cần kiểm tra" và bị loại khỏiphéptính mức độ sử dụng.|
|Kết quả thực tế (Actual /|Pending|
|Status)|2.9. Test case cho UC9 - Theo dõi tài nguyên|



### **_2.8.2. TC_UC08_02 – Ngoại lệ (AF5) - Không có Hub phù hợp với bộ lọc._** 

|**Trường thông tin**|**Đặc tả kịch bản**|
|---|---|
|Test Case ID|TC_UC08_02|
|Use Case liênquan|UC8 - Giám sát mạnglưới MobilityHub|
|Mô tả kịch bản|Ngoại lệ(AF5)- Khôngcó Hubphù hợpvới bộ lọc.|
|Tiền điều kiện<br>(Preconditions)|Đã đăng nhập với vai trò Đơn vị vận hành; không có Hub nào thuộc<br>khu vực được lọc.|
|Dữ liệu đầu vào (Input<br>Data)|filter = { khuVuc: "Khu vực không tồn tại" }|
|Kết quả mong đợi<br>(Expected Result)|Hệ thống thông báo không có Hub đáp ứng tiêu chí, giữ nguyên bộ<br>lọc để Đơn vị vận hành điều chỉnh hoặc xoá bộ lọc.|
|Kết quả thực tế (Actual /<br>Status)|Pending|



### **_2.8.3. TC_UC08_03 – Ngoại lệ (EX1) - Người dùng không đủ quyền truy cập._** 

|**Trường thông tin**|**Đặc tả kịch bản**|
|---|---|
|Test Case ID|TC_UC08_03|
|Use Case liênquan|UC8 - Giám sát mạnglưới MobilityHub|
|Mô tả kịch bản|Ngoại lệ(EX1)- Người dùngkhôngđủquyền truycập.|
|Tiền điều kiện<br>(Preconditions)|Người dùng đăng nhập bằng tài khoản có vai trò Sinh viên.|
|Dữ liệu đầu vào (Input<br>Data)|session.role=STUDENT; filter=null|
|Kết quả mong đợi<br>(Expected Result)|Hệ thống ném UnauthorizedException, từ chối truy cập dashboard<br>vàyêu cầu xác thực lại bằngtài khoản cóquyền vận hành(NFR10).|
|Kết quả thực tế (Actual /<br>Status)|Pending|



### **_2.8.4. TC_UC08_04 – Ngoại lệ (EX2) - Không truy xuất được dữ liệu giám sát._** 

|**Trường thông tin**|**Đặc tả kịch bản**|
|---|---|
|Test Case ID|TC_UC08_04|
|Use Case liênquan|UC8 - Giám sát mạnglưới MobilityHub|
|Mô tả kịch bản|Ngoại lệ(EX2)- Khôngtruyxuất được dữ liệugiám sát.|
|Tiền điều kiện<br>(Preconditions)|Đã đăng nhập với vai trò Đơn vị vận hành; kết nối tới cơ sở dữ liệu<br>bịgián đoạn.|
|Dữ liệu đầu vào (Input<br>Data)|filter=null|



|**Trường thông tin**|**Đặc tả kịch bản**|
|---|---|
|Kết quả mong đợi|Hệ thống ném DataSourceUnavailableException, thông báo không<br>|
|(Expected Result)|thể tải dashboard và chophépĐơn vị vận hành thử lại.|
|Kết quả thực tế (Actual /<br>Status)|Pending|



### **_2.8.5. TC_UC08_05 – Ngoại lệ (EX3, NFR05) - Một Hub mất kết nối, các Hub khác vẫn hoạt động._** 

|**Trường thông tin**|**Đặc tả kịch bản**|
|---|---|
|Test Case ID|TC_UC08_05|
|Use Case liênquan|UC8 - Giám sát mạnglưới MobilityHub|
|Mô tả kịch bản|Ngoại lệ (EX3, NFR05) - Một Hub mất kết nối, các Hub khác vẫn<br>hoạt động.|
|Tiền điều kiện<br>(Preconditions)|Đã đăng nhập với vai trò Đơn vị vận hành; 1 Hub mất kết nối hoàn<br>toàn, các Hub còn lại bình thường.|
|Dữ liệu đầu vào (Input<br>Data)|filter=null; Hub "HUB-003" không gửi dữ liệu trong 10 phút|
|Kết quả mong đợi<br>(Expected Result)|Hub mất kết nối được hiển thị với dữ liệu gần nhất và đánh dấu chưa<br>xác định, không khẳng định tài nguyên còn khả dụng; dashboard của<br>các Hub còn lại vẫn hiển thị bình thường, khôngbịgián đoạn.|
|Kết quả thực tế (Actual /<br>Status)|Pending<br>2.5. Test case cho UC5 - Nhậnphươngtiện|



## **2.9. Test case cho UC9 – Theo dõi tài nguyên** 

### **_2.9.1. TC_UC09_01 – Biên: một dòng tài nguyên có timestamp quá cũ._** 

|**Trường thông tin**|**Đặc tả kịch bản**|
|---|---|
|Test Case ID|TC_UC09_01|
|Use Case liênquan|UC9: Theo dõi tài nguyên|
|Mô tả kịch bản|Biên: một dòngtài nguyên có timestamp quá cũ.|
|Tiền điều kiện<br>(Preconditions)|Vận hành đã đăng nhập từ UC8. Hub A: 20 xe, 24 chỗ đỗ, 5 cổng<br>sạc khả dụng. Port 2 FAULTY, cậpnhật 07:47; Hub cậpnhật 10:39.|
|Dữ liệu đầu vào (Input<br>Data)|hubId = HubA, giờ hiện tại 10:39|
|Kết quả mong đợi<br>(Expected Result)|HubResource với 20 / 24 / 5 và lastUpdated = 10:39. Dòng Port 2 có<br>isStale = true và được đánh dấu trên giao diện. Không dữ liệu vận<br>hành nào bị thayđổi.|
|Kết quả thực tế (Actual /<br>Status)|Pending|



### **_2.9.2. TC_UC09_02 – Ngoại lệ: không truy xuất được dữ liệu (EX1)._** 

|**Trường thông tin**|**Đặc tả kịch bản**|
|---|---|
|Test Case ID|TC_UC09_02|
|Use Case liênquan|UC9: Theo dõi tài nguyên|
|Mô tả kịch bản|Ngoại lệ: khôngtruyxuất được dữ liệu(EX1).|



|**Trường thông tin**|**Đặc tả kịch bản**|
|---|---|
|Tiền điều kiện<br>(Preconditions)|Vận hành đã đăng nhập. Kho dữ liệu tài nguyên được giả lập lỗi kết<br>nối.|
|Dữ liệu đầu vào (Input<br>Data)|hubId = HubA|
|Kết quả mong đợi<br>(Expected Result)|Ném DataUnavailableException. Giao diện hiển thị thông báo lỗi<br>truy cập dữ liệu và cho phép thử lại ("Refresh information"). Không<br>hiển thị số liệu cũ như thể còn hiệu lực.|
|Kết quả thực tế (Actual /|Pending|
|Status)|2.10. Test case cho UC10 - Xem cảnh báoquá tải|



## **2.10. Test case cho UC10 – Xem cảnh báo quá tải** 

### **_2.10.1. TC_UC10_01 – Thành công: chỗ đỗ 95% vượt ngưỡng 75%, gọi hai lần không tạo cảnh báo trùng._** 

|**Trường thông tin**|**Đặc tả kịch bản**|
|---|---|
|Test Case ID|TC_UC10_01|
|Use Case liênquan|UC10: Xem cảnh báoquá tải|
|Mô tả kịch bản|Thành công: chỗ đỗ 95% vượt ngưỡng 75%, gọi hai lần không tạo<br>cảnh báo trùng.|
|Tiền điều kiện<br>(Preconditions)|Hub A có DataState = FRESH. Ngưỡng PARKING_SPOT = 75%.<br>Chưa có cảnh báo ACTIVE cho Hub A, loại PARKING_SPOT.|
|Dữ liệu đầu vào (Input<br>Data)|hubId = HubA, mức sử dụng chỗ đỗ 95%. Gọi evaluateHubLoad hai<br>lần liên tiếp.|
|Kết quả mong đợi<br>(Expected Result)|Lần 1: tạo 1 OverloadAlert (utilization = 0.95, threshold = 0.75,<br>severity = HIGH, ACTIVE). Lần 2: vẫn 1 cảnh báo ACTIVE, được<br>cập nhật chứ không tạo mới. Chi tiết hiển thị Hub, loại, mức sử<br>dụng, ngưỡng, vị trí, nguyên nhân dự kiến.|
|Kết quả thực tế (Actual /<br>Status)|Pending|



### **_2.10.2. TC_UC10_02 – Biên: mức sử dụng thấp hơn ngưỡng, không có cảnh báo._** 

|**Trường thông tin**|**Đặc tả kịch bản**|
|---|---|
|Test Case ID|TC_UC10_02|
|Use Case liênquan|UC10: Xem cảnh báoquá tải|
|Mô tả kịch bản|Biên: mức sử dụngthấphơn ngưỡng, khôngcó cảnh báo.|
|Tiền điều kiện<br>(Preconditions)|Hub C có DataState = FRESH. Ngưỡng 75% cho chỗ đỗ và cổng<br>sạc. Chưa có cảnh báo ACTIVE.|
|Dữ liệu đầu vào (Input<br>Data)|hubId = HubC, chỗ đỗ 70%, cổng sạc 60%|
|Kết quả mong đợi<br>(Expected Result)|Trả về danh sách rỗng, không tạo OverloadAlert nào. Giao diện gọi<br>showNormalStatus() (trạngthái mạnglưới bình thường).|
|Kết quả thực tế (Actual /<br>Status)|Pending|



### **_2.10.3. TC_UC10_03 – Ngoại lệ: dữ liệu quá cũ, không tạo cảnh báo._** 

|**Trường thông tin**|**Đặc tả kịch bản**|
|---|---|
|Test Case ID|TC_UC10_03|
|Use Case liênquan|UC10: Xem cảnh báoquá tải|
|Mô tả kịch bản|Ngoại lệ: dữ liệuquá cũ, khôngtạo cảnh báo.|
|Tiền điều kiện<br>(Preconditions)|Hub A có DataState = STALE (dữ liệu cũ hơn 15 giây). Ngưỡng đã<br>cấu hình.|
|Dữ liệu đầu vào (Input<br>Data)|hubId = HubA|
|Kết quả mong đợi<br>(Expected Result)|Ném DataUnavailableException. Không tạo hay cập nhật cảnh báo<br>nào, tránh cảnh báo sai do dữ liệu lỗi thời. Giao diện hiển thị thông<br>báo lỗi vàgiữ nguyên dashboard để thử lại.|
|Kết quả thực tế (Actual /<br>Status)|Pending<br>2.11. Test case cho UC11 - Điềuphốiphươngtiện|



## **2.11. Test case cho UC11 – Điều phối phương tiện** 

### **_2.11.1. TC_UC11_01 – Thành công (Normal Flow): Điều phối 2 xe từ Hub KTX B sang Hub Ga Metro còn đủ chỗ đỗ trống._** 

|**Trường thông tin**|**Đặc tả kịch bản**|
|---|---|
|Test Case ID|TC_UC11_01|
|Use Case liênquan|UC11 – Điềuphốiphươngtiện|
|Mô tả kịch bản|Thành công (Normal Flow): Điều phối 2 xe từ Hub KTX B sang<br>Hub Ga Metro còn đủ chỗ đỗ trống.|
|Tiền điều kiện<br>(Preconditions)|1. Operator OP01 đã đăng nhập hợp lệ qua SSO (NFR10).<br>2. Hub KTX B (HUB_KTXB) có xe EB_01 (AVAILABLE, pin<br>90%) và EB_02 (AVAILABLE, pin 85%).<br>3. Hub Ga Metro (HUB_METRO) đang ACTIVE và còn<br>availableSpots = 10.|
|Dữ liệu đầu vào (Input<br>Data)|operatorId = "OP01", sourceHubId = "HUB_KTXB", destHubId =<br>"HUB_METRO", vehicleIds =["EB_01", "EB_02"]|
|Kết quả mong đợi<br>(Expected Result)|1. Tạo thành công DispatchOrder (status = PENDING) với 2 xe<br>EB_01, EB_02.<br>2. EB_01 và EB_02 chuyển sang trạng thái DISPATCHING (Sinh<br>viên không thể đặt – NFR09).<br>3. availableSpots tại HUB_METRO giảm từ 10 xuống 8; tại<br>HUB_KTXB tăng tương ứng.<br>4. Ghi 1 bản ghi AuditLog (NFR11) và gửi thông báo công việc tới<br>đội vận chuyểnqua NotificationService.|
|Kết quả thực tế (Actual /<br>Status)|Pending|



### **_2.11.2. TC_UC11_02 – Ngoại lệ (EX1 – Race Condition / NFR09): Xe được chọn vừa bị Sinh viên đặt trước ngay trước khi Operator xác nhận lệnh._** 

|**Trường thông tin**|**Đặc tả kịch bản**|
|---|---|
|Test Case ID|TC_UC11_02|
|Use Case liênquan|UC11 – Điềuphốiphươngtiện|



|**Trường thông tin**|**Đặc tả kịch bản**|
|---|---|
|Mô tả kịch bản|Ngoại lệ (EX1 – Race Condition / NFR09): Xe được chọn vừa bị<br>Sinh viên đặt trước ngaytrước khi Operator xác nhận lệnh.|
|Tiền điều kiện<br>(Preconditions)|1. Operator OP01 mở màn hình điều phối và thấy xe EB_01 khả<br>dụng.<br>2. Ngay trước thời điểm Operator bấm xác nhận, Sinh viên SV05 đặt<br>thành côngEB_01(status chuyển sangRESERVED).|
|Dữ liệu đầu vào (Input<br>Data)|operatorId = "OP01", sourceHubId = "HUB_KTXB", destHubId =<br>"HUB_METRO", vehicleIds =["EB_01", "EB_02"]|
|Kết quả mong đợi<br>(Expected Result)|1. Cơ chế khóa giao dịch phát hiện EB_01 không còn ở trạng thái<br>AVAILABLE và ném VehicleConflictException.<br>2. Toàn bộ giao dịch bị rollback: không tạo DispatchOrder nào,<br>EB_02 vẫn giữ nguyên AVAILABLE, sức chứa các Hub không đổi.<br>3. Giao diện thông báo xung đột ở EB_01 và gợi ý Operator loại bỏ<br>xe xungđột hoặc chọn xe khác.|
|Kết quả thực tế (Actual /<br>Status)|Pending|



### **_2.11.3. TC_UC11_03 – Ngoại lệ (EX2): Hub đích không đủ chỗ đỗ trống cho số lượng phương tiện điều phối._** 

|**Trường thông tin**|**Đặc tả kịch bản**|
|---|---|
|Test Case ID|TC_UC11_03|
|Use Case liênquan|UC11 – Điềuphốiphươngtiện|
|Mô tả kịch bản|Ngoại lệ (EX2): Hub đích không đủ chỗ đỗ trống cho số lượng<br>phươngtiện điềuphối.|
|Tiền điều kiện<br>(Preconditions)|1. Operator OP01 đã đăng nhập.<br>2. Hub nguồn HUB_KTXB có 3 xe AVAILABLE.<br>3. Hub đích HUB_THUVIEN đang ACTIVE nhưng chỉ còn<br>availableSpots = 1.|
|Dữ liệu đầu vào (Input<br>Data)|operatorId = "OP01", sourceHubId = "HUB_KTXB", destHubId =<br>"HUB_THUVIEN", vehicleIds =["EB_01", "EB_02", "EB_03"]|
|Kết quả mong đợi<br>(Expected Result)|1. hasAvailableCapacity(3) trả về false -> ném<br>HubCapacityExceededException.<br>2. Không tạo DispatchOrder, trạng thái cả 3 xe vẫn là AVAILABLE.<br>3. Giao diện hiển thị cảnh báo quá tải sức chứa Hub đích và yêu cầu<br>giảm số xe(<= 1)hoặc chọn Hub đích khác.|
|Kết quả thực tế (Actual /<br>Status)|Pending|



### **_2.11.4. TC_UC11_04 – Luồng thay thế (AF2): Hủy lệnh điều phối đang chờ xử lý trước khi vận chuyển._** 

|**Trường thông tin**|**Đặc tả kịch bản**|
|---|---|
|Test Case ID|TC_UC11_04|
|Use Case liênquan|UC11 – Điềuphốiphươngtiện|
|Mô tả kịch bản|Luồng thay thế (AF2): Hủy lệnh điều phối đang chờ xử lý trước khi<br>vận chuyển.|



|**Trường thông tin**|**Đặc tả kịch bản**|
|---|---|
|Tiền điều kiện<br>(Preconditions)|1. Lệnh điều phối ORD_101 đang ở trạng thái PENDING gồm 2 xe<br>EB_01, EB_02 (status = DISPATCHING).<br>2. Đội vận chuyển chưa bắt đầu di chuyển xe.|
|Dữ liệu đầu vào (Input<br>Data)|operatorId = "OP01", orderId = "ORD_101"|
|Kết quả mong đợi<br>(Expected Result)|1. cancelDispatchOrder() trả về true.<br>2. ORD_101 chuyển sang status = CANCELLED.<br>3. EB_01 và EB_02 được mở khóa và khôi phục về AVAILABLE<br>tại HUB_KTXB.<br>4. Sức chứa dự kiến của HUB_KTXB và HUB_METRO được hoàn<br>tác vàghi nhận vào AuditLog.|
|Kết quả thực tế (Actual /<br>Status)|Pending|



## **2.12. Test case cho UC12 – Xử lý các sự cố** 

### **_2.12.1. TC_UC12_01 – Thành công (Normal Flow): Tạm ngưng cổng sạc bị lỗi đang có lịch đặt trước của Sinh viên, hủy lịch, thông báo và ghi AuditLog._** 

|**Trường thông tin**|**Đặc tả kịch bản**|
|---|---|
|Test Case ID|TC_UC12_01|
|Use Case liênquan|UC12 – Xử lýcác sự cố|
|Mô tả kịch bản|Thành công (Normal Flow): Tạm ngưng cổng sạc bị lỗi đang có lịch<br>đặt trước của Sinh viên, hủylịch, thôngbáo vàghi AuditLog.|
|Tiền điều kiện<br>(Preconditions)|1. Operator OP01 đã đăng nhập hợp lệ.<br>2. Sự cố INC_201 (CRITICAL/HIGH) được ghi nhận cho cổng sạc<br>CP_03 (status = AVAILABLE).<br>3. Sinh viên SV12 đang có lịch ChargingRegistration CR_55<br>(CONFIRMED)cho CP_03.|
|Dữ liệu đầu vào (Input<br>Data)|operatorId = "OP01", incidentId = "INC_201", reason = "Cổng sạc<br>mất kết nối bo mạch nguồn", fixingMethod = "Cử kỹ thuật viên thay<br>rơ-le bảo vệ"|
|Kết quả mong đợi<br>(Expected Result)|1. Incident INC_201 chuyển sang IN_PROGRESS với đầy đủ<br>nguyên nhân và hướng khắc phục.<br>2. Cổng CP_03 chuyển sang MAINTENANCE (bị loại khỏi danh<br>sách tìm kiếm/đặt chỗ).<br>3. ChargingRegistration CR_55 tự động chuyển sang<br>CANCELLED_BY_INCIDENT.<br>4. NotificationService gửi thông báo xin lỗi tới SV12 và ghi<br>AuditLog (lưu >= 90 ngày– NFR11).|
|Kết quả thực tế (Actual /<br>Status)|Pending|



### **_2.12.2. TC_UC12_02 – Luồng thay thế (AF1): Hoàn tất sửa chữa và khôi phục tài nguyên về trạng thái Khả dụng._** 

|**Trường thông tin**|**Đặc tả kịch bản**|
|---|---|
|Test Case ID|TC_UC12_02|
|Use Case liênquan|UC12 – Xử lýcác sự cố|



|**Trường thông tin**|**Đặc tả kịch bản**|
|---|---|
|Mô tả kịch bản|Luồng thay thế (AF1): Hoàn tất sửa chữa và khôi phục tài nguyên về<br>trạngthái Khả dụng.|
|Tiền điều kiện<br>(Preconditions)|1. Sự cố INC_201 đang ở trạng thái IN_PROGRESS; cổng sạc<br>CP_03 đangở trạngthái MAINTENANCE.|
|Dữ liệu đầu vào (Input<br>Data)|operatorId = "OP01", incidentId = "INC_201"|
|Kết quả mong đợi<br>(Expected Result)|1. Incident INC_201 chuyển sang RESOLVED và ghi nhận<br>resolvedAt = thời điểm hiện tại.<br>2. Cổng sạc CP_03 khôi phục từ MAINTENANCE về<br>AVAILABLE.<br>3. Ghi nhận AuditLog thao tác hoàn tất xử lý và cập nhật trạng thái<br>mạnglưới.|
|Kết quả thực tế (Actual /<br>Status)|Pending|



### **_2.12.3. TC_UC12_03 – Ngoại lệ (EX1 – NFR05 Fault Tolerance): Mất kết nối hoàn toàn tại một Hub đơn lẻ kích hoạt cô lập lỗi mà không làm gián đoạn các Hub khác._** 

|**Trường thông tin**|**Đặc tả kịch bản**|
|---|---|
|Test Case ID|TC_UC12_03|
|Use Case liênquan|UC12 – Xử lýcác sự cố|
|Mô tả kịch bản|Ngoại lệ (EX1 – NFR05 Fault Tolerance): Mất kết nối hoàn toàn tại<br>một Hub đơn lẻ kích hoạt cô lập lỗi mà không làm gián đoạn các<br>Hub khác.|
|Tiền điều kiện<br>(Preconditions)|1. Mạng lưới có HUB_A, HUB_B, HUB_C đang hoạt động bình<br>thường (ACTIVE).<br>2. HUB_B mất kết nối hoàn toàn khỏi hệ thống giám sát.|
|Dữ liệu đầu vào (Input<br>Data)|hubId = "HUB_B"|
|Kết quả mong đợi<br>(Expected Result)|1. HUB_B chuyển sang trạng thái ISOLATED; mọi giao dịch mới<br>tại HUB_B bị tạm ngưng.<br>2. Tự động tạo sự cố loại HUB_DISCONNECTED mức CRITICAL<br>và gửi cảnh báo cho Operator.<br>3. HUB_A và HUB_C vẫn ở trạng thái ACTIVE, phục vụ tìm<br>kiếm/đặt xe bình thườngkhôngbị treo hay gián đoạn(NFR05).|
|Kết quả thực tế (Actual /<br>Status)|Pending|



**_2.12.4. TC_UC12_04 – Ngoại lệ (Bảo mật RBAC – NFR10): Tài khoản Sinh viên cố gắng gọi chức năng xử lý sự cố bị từ chối truy cập._** 

|**Trường thông tin**|**Đặc tả kịch bản**|
|---|---|
|Test Case ID|TC_UC12_04|
|Use Case liênquan|UC12 – Xử lýcác sự cố|
|Mô tả kịch bản|Ngoại lệ (Bảo mật RBAC – NFR10): Tài khoản Sinh viên cố gắng<br>gọi chức năngxử lýsự cố bị từ chối truycập.|
|Tiền điều kiện|1. Người dùng đang đăng nhập với tài khoản vai trò STUDENT<br>|
|(Preconditions)|(khôngcóquyền OPERATOR).|



|**Trường thông tin**|**Đặc tả kịch bản**|
|---|---|
|Dữ liệu đầu vào (Input<br>Data)|actorId = "SV01" (role = STUDENT), incidentId = "INC_201"|
|Kết quả mong đợi<br>(Expected Result)|1. Hệ thống ném UnauthorizedException ngay bước kiểm tra quyền.<br>2. Không có bất kỳ thay đổi nào lên Incident, Resource hay<br>AuditLognghiệpvụ.|
|Kết quả thực tế (Actual /|Pending|
|Status)|2.13. Test case cho UC13 - Lậplịch sạc thôngminh|



## **2.13. Test case cho UC13 – Lập lịch sạc thông minh** 

### **_2.13.1. TC_UC13_01 – Lập lịch sạc và phê duyệt thủ công thành công_** 

|**Trường thông tin**|**Đặc tả kịch bản**|
|---|---|
|Test Case ID|TC_UC13_01|
|Use Case liênquan|UC13 – Smart ChargingSchedule|
|Mô tả kịch bản|Kiểm tra hệ thống tạo lịch sạc phù hợp và cho phép Operator phê<br>duyệt, lưu lịch thành côngkhi các tài nguyên sạc khả dụng.|
|Tiền điều kiện<br>(Preconditions)|1. Operator đã đăng nhập và có quyền lập lịch sạc.<br>2. Dữ liệu phương tiện, mức pin, nhu cầu sử dụng, thời gian chờ và<br>trạng thái trụ sạc đã được cập nhật.<br>3. Hub còn khả năng tiếp nhận lịch sạc.<br>4. Trụ sạc được chọn khôngcó lịch trùngthờigian.|
|Dữ liệu đầu vào (Input<br>Data)|Operator: OP001; Hub: HUB001;Vehicle: VEH001; Battery Level:<br>15%; Charging Port: CP001; Charging Time: 14:00–15:00;<br>Approval Mode: MANUAL.|
|Kết quả mong đợi<br>(Expected Result)|1. Hệ thống tạo lịch sạc phù hợp với dữ liệu đầu vào.<br>2. Lịch sạc hiển thị đầy đủ phương tiện, trụ sạc, thời gian và mức độ<br>ưu tiên.<br>3. Operator phê duyệt lịch thành công.<br>4. Lịch được lưu vào hệ thống.<br>5. Trụ sạc được chuyển sang trạng thái đã giữ chỗ.<br>6. Thao tác đượcghi nhận trongAuditLog.|
|Kếtquả thực tế / Status|Pending– Chưa thực hiện kiểm thử.|



### **_2.13.2. TC_UC13_02 – Operator chỉnh sửa lịch sạc trước khi phê duyệt_** 

|**Trường thông tin**|**Đặc tả kịch bản**|
|---|---|
|Test Case ID|TC_UC13_02|
|Use Case liênquan|UC13 – Smart ChargingSchedule|
|Mô tả kịch bản|Kiểm tra khả năng Operator chỉnh sửa lịch sạc do hệ thống đề xuất<br>trước khiphê duyệt.|
|Tiền điều kiện<br>(Preconditions)|1. Operator đã đăng nhập và có quyền lập lịch sạc.<br>2. Hệ thống đã tạo lịch sạc ở trạng thái chờ phê duyệt.<br>3. Hub và trụ sạc có đủ tài nguyên để đápứnglịch sau khi chỉnh sửa.|



|**Trường thông tin**|**Đặc tả kịch bản**|
|---|---|
|Dữ liệu đầu vào (Input<br>Data)|Operator: OP001<br>Schedule ID: SCH001<br>Vehicle: VEH001<br>Charging Port: CP001<br>Thời gian ban đầu: 14:00–15:00<br>Thờigian sau chỉnh sửa: 15:00–16:00|
|Kết quả mong đợi<br>(Expected Result)|1. Hệ thống hiển thị lịch sạc hiện tại để Operator chỉnh sửa.<br>2. Operator cập nhật thời gian sạc thành công.<br>3. Hệ thống kiểm tra và xác nhận khung giờ mới không bị xung đột<br>tài nguyên.<br>4. Lịch sạc được cập nhật theo thông tin mới nhưng vẫn ở trạng thái<br>chờ phê duyệt.<br>5. Operator có thể tiếptụcphê duyệt lịch sau khi chỉnh sửa.|
|Kếtquả thực tế / Status|Pending– Chưa thực hiện kiểm thử.|



### **_2.13.3. TC_UC13_03 – Hệ thống tự động phê duyệt lịch sạc_** 

|**Trường thông tin**|**Đặc tả kịch bản**|
|---|---|
|Test Case ID|TC_UC13_03|
|Use Case liênquan|UC13 – Smart ChargingSchedule|
|Mô tả kịch bản|Kiểm tra khả năng hệ thống tự động phê duyệt lịch sạc khi chế độ<br>phê duyệt tự động được kích hoạt và lịch đáp ứng các điều kiện hợp<br>lệ.|
|Tiền điều kiện<br>(Preconditions)|1. Operator đã đăng nhập và có quyền lập lịch sạc.<br>2. Chế độ tự động phê duyệt đã được kích hoạt.<br>3. Dữ liệu phương tiện, mức pin, nhu cầu sử dụng và tài nguyên sạc<br>hợp lệ.<br>4. Trụ sạc khôngcó lịch trùngthờigian và Hub khôngbịquá tải.|
|Dữ liệu đầu vào (Input<br>Data)|Operator: OP001<br>Hub: HUB001<br>Vehicle: VEH002<br>Battery Level: 18%<br>Charging Port: CP002<br>Charging Time: 16:00–17:00<br>Approval Mode: AUTO|
|Kết quả mong đợi<br>(Expected Result)|1. Hệ thống tiếp nhận dữ liệu và tạo lịch sạc hợp lệ.<br>2. Hệ thống tự động phê duyệt lịch mà không yêu cầu Operator xác<br>nhận thủ công.<br>3. Lịch sạc được lưu thành công với trạng thái đã phê duyệt.<br>4. Trụ sạc tương ứng được chuyển sang trạng thái đã giữ chỗ.<br>5. Thao tácphê duyệt đượcghi nhận trongAuditLog.|
|Kếtquả thực tế / Status|Pending– Chưa thực hiện kiểm thử.|



### **_2.13.4. TC_UC13_04 – Xử lý xung đột tài nguyên và Hub quá tải_** 

|**Trường thông tin**|**Đặc tả kịch bản**|
|---|---|
|Test Case ID|TC_UC13_04|
|Use Case liênquan|UC13 – Smart ChargingSchedule|



|**Trường thông tin**|**Đặc tả kịch bản**|
|---|---|
|Mô tả kịch bản|Kiểm tra khả năng hệ thống phát hiện xung đột trụ sạc, khung giờ<br>hoặc tình trạngHubquá tải trong quá trình lậplịch sạc.|
|Tiền điều kiện<br>(Preconditions)|1. Operator đã đăng nhập và có quyền lập lịch sạc.<br>2. Hub HUB001 đang hoạt động.<br>3. Trụ sạc CP001 đã được giữ chỗ trong khoảng thời gian 14:00–<br>15:00.<br>4. Dữ liệu tải của Hub được cập nhật và có thể xác định tình trạng<br>quá tải.|
|Dữ liệu đầu vào (Input<br>Data)|Operator: OP001<br>Hub: HUB001<br>Vehicle: VEH003<br>Battery Level: 12%<br>Charging Port: CP001<br>Charging Time: 14:30–15:30<br>Tình trạngHub:Quá tải trongtrườnghợpkiểm thử bổ sung.|
|Kết quả mong đợi<br>(Expected Result)|1. Hệ thống phát hiện trụ sạc CP001 bị trùng lịch trong khoảng<br>14:30–15:00.<br>2. Hệ thống không cho phép lưu lịch sạc bị xung đột.<br>3. Hệ thống hiển thị cảnh báo và đề xuất khung giờ hoặc tài nguyên<br>thay thế phù hợp.<br>4. Khi Hub quá tải, hệ thống thông báo tình trạng quá tải và đề xuất<br>chuyển yêu cầu đến chức năng điều phối tại UC11.<br>5. Không phát sinh lịch sạc mới hoặc giữ chỗ tài nguyên không hợp<br>lệ.|
|Kếtquả thực tế / Status|Pending– Chưa thực hiện kiểm thử.|



### **_2.13.5. TC_UC13_05 – Xử lý lỗi truy xuất dữ liệu và bảo đảm tính toàn vẹn khi lưu lịch_** 

|**Trường thông tin**|**Đặc tả kịch bản**|
|---|---|
|Test Case ID|TC_UC13_05|
|Use Case liênquan|UC13 – Smart ChargingSchedule|
|Mô tả kịch bản|Kiểm tra khả năng hệ thống xử lý lỗi khi không truy xuất được dữ<br>liệu từ hệ thống mô phỏng hoặc cảm biến, đồng thời bảo đảm các dữ<br>liệu liên quan được lưu đồng bộ khi phát sinh lỗi trong quá trình lưu<br>lịch.|
|Tiền điều kiện<br>(Preconditions)|1. Operator đã đăng nhập và có quyền lập lịch sạc.<br>2. Hệ thống đang sử dụng dữ liệu từ hệ thống mô phỏng hoặc cảm<br>biến.<br>3. Có thể mô phỏng tình huống lỗi truy xuất dữ liệu và lỗi trong quá<br>trình lưu lịch.<br>4. Có sẵn lịch sạc và trụ sạc để kiểm tra trạng thái trước và sau giao<br>dịch.|



|**Trường thông tin**|**Đặc tả kịch bản**|
|---|---|
|Dữ liệu đầu vào (Input<br>Data)|Operator: OP001<br>Hub: HUB001<br>Vehicle: VEH004<br>Charging Port: CP003<br>Charging Time: 17:00–18:00<br>Tình huống 1: Hệ thống mô phỏng/cảm biến không phản hồi dữ liệu.<br>Tình huống 2: Phát sinh lỗi khi lưu ChargingSchedule, giữ chỗ<br>ChargingPort hoặcghi AuditLog.|
|Kết quả mong đợi<br>(Expected Result)|1. Khi không truy xuất được dữ liệu, hệ thống thông báo lỗi và<br>không tạo lịch dựa trên dữ liệu không đầy đủ.<br>2. Khi phát sinh lỗi trong quá trình lưu, giao dịch phải được rollback.<br>3. Không tồn tại lịch sạc mới được lưu một phần.<br>4. Trạng thái giữ chỗ của trụ sạc được khôi phục về trạng thái trước<br>giao dịch nếu giao dịch thất bại.<br>5. Hệ thống thông báo cho Operator biết thao tác lưu lịch không<br>thành công.|
|Kết quả thực tế / Status<br>**.14. Test case cho UC14**|Pending – Chưa thực hiện kiểm thử.<br>**– Mô phỏng và phân tích kịch bản**|
|**_.14.1. TC_UC14_01 – Chạ_**<br>**Trường thông tin**|**_y mô phỏng thành công và lưu báo cáo_**<br>**Nội dung**|
|1. Test Case ID|TC_UC14_01|
|2. Use Case liênquan|UC14 – Môphỏngvàphân tích kịch bản|
|3. Mô tả kịch bản|Đơn vị vận hành thiết lập kịch bản giả định về tình trạng quá tải tại<br>một MobilityHub, chạymôphỏngvà lưu báo cáo đánhgiá.|
|4. Tiền điều kiện<br>(Preconditions)|1. Đơn vị vận hành đã đăng nhập thành công và có quyền truy cập<br>UC14.<br>2. Trạng thái hiện tại của toàn mạng lưới đã được sao chép vào môi<br>trường mô phỏng ảo cách ly.<br>3. Dữ liệu Hub và tài nguyên hợplệ.|
|5. Dữ liệu đầu vào (Input<br>Data)|- Operator ID: OP001<br>- Scenario ID: SCN001<br>- Hub ID: HUB001<br>- Kịch bản: Lượng sinh viên tăng 30%.<br>- Trạngthái ban đầu: 20 xe, 10 chỗ đỗ, 5 cổngsạc khả dụng.|
|6. Kết quả mong đợi<br>(Expected Result)|1. Hệ thống tiếp nhận tham số và thực hiện mô phỏng thành công<br>trên môi trường ảo cách ly.<br>2. Báo cáo hiển thị tác động của kịch bản và đề xuất điều phối phù<br>hợp.<br>3. Báo cáo được lưu khi Operator chọn “Kết thúc”.<br>4. Dữ liệu vận hành thực tế không bị thay đổi sau quá trình mô<br>phỏng.|
|7. Kếtquả thực tế / Status|Pending|



## **2.14. Test case cho UC14 – Mô phỏng và phân tích kịch bản** 

### **_2.14.1. TC_UC14_01 – Chạy mô phỏng thành công và lưu báo cáo_** 

### **_2.14.2. TC_UC14_02 – Chuyển tiếp áp dụng đề xuất mô phỏng (AF1)_** 

|**Trường thông tin**|**Nội dung**|
|---|---|
|1. Test Case ID|TC_UC14_02|
|2. Use Case liênquan|UC14 – Môphỏngvàphân tích kịch bản|
|3. Mô tả kịch bản|Sau khi mô phỏng, Đơn vị vận hành đánh giá đề xuất điều phối là<br>khả thi và chọn “Ápdụngvào thực tế”.|
|4. Tiền điều kiện<br>(Preconditions)|1. Đơn vị vận hành đã đăng nhập thành công và có quyền truy cập<br>UC14.<br>2. Mô phỏng đã hoàn tất và báo cáo đề xuất đã được tạo.<br>3. Đề xuất điềuphối có thể chuyển tiếpsangUC11 hoặc UC13.|
|5. Dữ liệu đầu vào (Input<br>Data)|- Operator ID: OP001<br>- Scenario ID: SCN002<br>- Recommendation: Điều chuyển 5 phương tiện từ HUB001 sang<br>HUB002.<br>- Use Case đích: UC11.|
|6. Kết quả mong đợi<br>(Expected Result)|1. Hệ thống ghi nhận lựa chọn áp dụng đề xuất của Operator.<br>2. Hệ thống chuyển hướng đến giao diện UC11 với các tham số điều<br>phối tương ứng được điền sẵn.<br>3. Operator có thể kiểm tra và tiếp tục thực hiện quy trình UC11.<br>4. Việc chuyển tiếp không tự động thay đổi trạng thái vận hành thực<br>tế khi chưa thực hiệnquytrình của UC11.|
|7. Kếtquả thực tế / Status|Pending|



### **_2.14.3. TC_UC14_03 – Nhập tham số mô phỏng không hợp lệ (EX1)_** 

|**Trường thông tin**|**Nội dung**|
|---|---|
|1. Test Case ID|TC_UC14_03|
|2. Use Case liênquan|UC14 – Môphỏngvàphân tích kịch bản|
|3. Mô tả kịch bản|Đơn vị vận hành nhập tham số mô phỏng không hợp lệ, chẳng hạn<br>số lượng phươngtiệngiả định cógiá trị âm.|
|4. Tiền điều kiện<br>(Preconditions)|1. Đơn vị vận hành đã đăng nhập thành công và có quyền truy cập<br>UC14.<br>2. Giao diện thiết lậptham số môphỏngđangđược hiển thị.|
|5. Dữ liệu đầu vào (Input<br>Data)|- Operator ID: OP001<br>- Scenario ID: SCN003<br>- Hub ID: HUB001<br>- Số lượng phươngtiệngiả định: -5.|
|6. Kết quả mong đợi<br>(Expected Result)|1. Hệ thống phát hiện tham số không hợp lệ.<br>2. Hệ thống đánh dấu trường dữ liệu lỗi và hiển thị thông báo yêu<br>cầu nhập lại.<br>3. Mô phỏng không được thực hiện khi tham số chưa hợp lệ.<br>4. Operator có thể chỉnh sửa và nhậplại tham số.|
|7. Kếtquả thực tế / Status|Pending|



### **_2.14.4. TC_UC14_04 – Không thể khởi tạo môi trường mô phỏng (EX2)_** 

|**Trường thông tin**|**Nội dung**|
|---|---|
|1. Test Case ID|TC_UC14_04|
|2. Use Case liênquan|UC14 – Môphỏngvàphân tích kịch bản|
|3. Mô tả kịch bản|Hệ thống không thể cấp phát tài nguyên để khởi tạo môi trường mô<br>phỏngcách lyvới cơ sở dữ liệu vận hành thực tế.|
|4. Tiền điều kiện<br>(Preconditions)|1. Đơn vị vận hành đã đăng nhập thành công và có quyền truy cập<br>UC14.<br>2. Operator đã thiết lập tham số kịch bản hợp lệ.<br>3. Hệ thống gặp lỗi cấp phát tài nguyên khi khởi tạo môi trường mô<br>phỏng.|
|5. Dữ liệu đầu vào (Input<br>Data)|- Operator ID: OP001<br>- Scenario ID: SCN004<br>- Hub ID: HUB001<br>- Kịch bản: Đóng cửa HUB001 để đánh giá khả năng điều phối<br>phương tiện.<br>- Trạngthái môi trườngmôphỏng: Khôngthể khởi tạo.|
|6. Kết quả mong đợi<br>(Expected Result)|1. Hệ thống phát hiện không thể khởi tạo môi trường mô phỏng cách<br>ly.<br>2. Hệ thống hiển thị thông báo: “Không thể chạy mô phỏng do lỗi<br>cấp phát môi trường”.<br>3. Quá trình mô phỏng kết thúc sớm và không tạo báo cáo kết quả.<br>4. Trạngthái dữ liệu vận hành thực tế đượcgiữ nguyên.|
|7. Kết quả thực tế / Status|Pending|



## **2.15. Test case cho UC15 – Tùy chỉnh giao diện (Customize UI)** 

### **_2.15.1. TC_UC15_01 – Thay đổi giao diện thành công_** 

|**Trường thông tin**|**Nội dung**|
|---|---|
|Test Case ID|TC_UC15_01|
|Use Case liênquan|UC15 – Customize UI|
|Mô tả kịch bản|Người dùngchuyển đổigiao diện từ sángsangtối hoặc ngược lại.|
|Tiền điều kiện|Người dùng đang truy cập hệ thống; giao diện hiện tại đã được khởi<br>tạo.|
|Dữ liệu đầu vào|Theme hiện tại: Light; Theme được chọn: Dark.|
|Kết quả mong đợi|Hệ thống áp dụng giao diện tối thành công; các thành phần giao diện<br>được cập nhật đồng bộ; tùy chọn giao diện được lưu để sử dụng cho<br>lần truycậptiếptheo.|
|Kếtquả thực tế / Status|Pending|



### **_2.15.2. TC_UC15_02 – Thay đổi ngôn ngữ và giữ nguyên trạng thái biểu mẫu_** 

|**Trường thông tin**|**Nội dung**|
|---|---|
|Test Case ID|TC_UC15_02|
|Use Case liênquan|UC15 – Customize UI|



|**Trường thông tin**|**Nội dung**|
|---|---|
|Mô tả kịch bản|Người dùng chuyển đổi ngôn ngữ hệ thống khi đang thao tác trên<br>một biểu mẫu.|
|Tiền điều kiện|Người dùng đang truy cập hệ thống; biểu mẫu đang có dữ liệu được<br>nhậpnhưngchưagửi.|
|Dữ liệu đầu vào|Ngôn ngữ hiện tại: Tiếng Việt (VN); ngôn ngữ được chọn: Tiếng<br>Anh(EN); dữ liệu biểu mẫu: đã nhậpmột số trườngthôngtin.|
|Kết quả mong đợi|Hệ thống chuyển đổi ngôn ngữ thành công; nội dung giao diện được<br>cập nhật theo ngôn ngữ mới; dữ liệu đã nhập trong biểu mẫu được<br>giữ nguyên, khôngbị mất hoặc đặt lại.|
|Kếtquả thực tế / Status|Pending|



### **_2.15.3. TC_UC15_03 – Lỗi khi lưu tùy chọn giao diện_** 

|**Trường thông tin**|**Nội dung**|
|---|---|
|Test Case ID|TC_UC15_03|
|Use Case liênquan|UC15 – Customize UI|
|Mô tả kịch bản|Người dùng thay đổi giao diện hoặc ngôn ngữ nhưng hệ thống gặp<br>lỗi khi lưu tùychọn.|
|Tiền điều kiện|Người dùng đang truy cập hệ thống; chức năng thay đổi giao diện và<br>ngôn ngữ hoạt động bình thường; phát sinh lỗi tại quá trình lưu tùy<br>chọn.|
|Dữ liệu đầu vào|Theme mới: Dark; Language mới: EN; trạngthái lưu: thất bại.|
|Kết quả mong đợi|Hệ thống hiển thị thông báo lỗi lưu tùy chọn; không ghi nhận tùy<br>chọn mới là đã lưu thành công; giữ trạng thái biểu mẫu và cho phép<br>người dùngthử lưu lại.|
|Kết quả thực tế / Status|Pending<br>2.16. Test case cho UC16 - Cậpnhật trạngthái tài nguyên|



## **2.16. Test case cho UC16 – Cập nhật trạng thái tài nguyên** 

**_2.16.1. TC_UC16_01 – Thành công (Normal Flow – NFR02): Tiếp nhận gói dữ liệu mới hợp lệ, cập nhật Operational DB và đẩy cập nhật thời gian thực <= 15 giây._** 

|**Trường thông tin**|**Đặc tả kịch bản**|
|---|---|
|Test Case ID|TC_UC16_01|
|Use Case liênquan|UC16 – Cậpnhật trạngthái tài nguyên|
|Mô tả kịch bản|Thành công (Normal Flow – NFR02): Tiếp nhận gói dữ liệu mới<br>hợp lệ, cập nhật Operational DB và đẩy cập nhật thời gian thực <=<br>15giây.|
|Tiền điều kiện<br>(Preconditions)|1. Xe EB_01 tồn tại trong Operational DB với status =<br>AVAILABLE, batteryLevel = 80%, lastUpdatedAt = 2026-11-<br>13T10:00:00.<br>2. Giao diện Sinh viên và Operator đang kết nối RealtimeGateway<br>(WebSocket/SSE).|
|Dữ liệu đầu vào (Input<br>Data)|packet = { packetId: "PKT_901", resourceId: "EB_01",<br>resourceType: "SharedVehicle", status: IN_USE, batteryLevel: 78.5,<br>latitude: 10.8701, longitude: 106.8031, packetTimestamp: 2026-11-<br>13T10:00:10, isSimulation: false}|



|**Trường thông tin**|**Đặc tả kịch bản**|
|---|---|
|Kết quả mong đợi|1. packetTimestamp (10:00:10) > lastUpdatedAt (10:00:00) -> hợp<br>lệ.<br>2. Operational DB cập nhật EB_01: status = IN_USE, batteryLevel =<br>78.5, lastUpdatedAt = 10:00:10.|
|(Expected Result)|3. RealtimeGateway phát sự kiện cập nhật tới giao diện người dùng<br>trong <= 15 giây (NFR02).<br>4. Endpoint trả về HTTP 200 OK (SyncResult =<br>UPDATED_OPERATIONAL).|
|Kết quả thực tế (Actual /<br>Status)|Pending|



### **_2.16.2. TC_UC16_02 – Ngoại lệ BẮT BUỘC (EX1 – NFR08): Lọc/loại bỏ gói dữ liệu trễ (Out-ofdate Timestamp) để không ghi đè dữ liệu mới hơn._** 

|**Trường thông tin**|**Đặc tả kịch bản**|
|---|---|
|Test Case ID|TC_UC16_02|
|Use Case liênquan|UC16 – Cậpnhật trạngthái tài nguyên|
|Mô tả kịch bản|Ngoại lệ BẮT BUỘC (EX1 – NFR08): Lọc/loại bỏ gói dữ liệu trễ<br>(Out-of-date Timestamp)để không ghi đè dữ liệu mới hơn.|
|Tiền điều kiện<br>(Preconditions)|1. Xe EB_01 trong Operational DB đang có trạng thái mới nhất:<br>status = IN_USE, batteryLevel = 75.0%, lastUpdatedAt = 2026-11-<br>13T10:05:00.<br>2. Một gói tin cũ bị trễ mạng (packetTimestamp = 10:04:30) hoặc<br>trùngmốc thờigian(10:05:00)mới đến nơi.|
|Dữ liệu đầu vào (Input<br>Data)|packet = { packetId: "PKT_899", resourceId: "EB_01",<br>resourceType: "SharedVehicle", status: AVAILABLE, batteryLevel:<br>82.0,packetTimestamp: 2026-11-13T10:04:30, isSimulation: false}|
|Kết quả mong đợi<br>(Expected Result)|1. isOutdatedPacket(10:04:30, 10:05:00) trả về true.<br>2. Hệ thống tự động hủy gói tin PKT_899, ghi AuditLog với action<br>= DROP_OUTDATED_PACKET.<br>3. Dữ liệu Operational DB của EB_01 giữ nguyên tuyệt đối (status =<br>IN_USE, batteryLevel = 75.0%, lastUpdatedAt = 10:05:00), không<br>bị ghi đè.<br>4. Không phát tín hiệu đẩy trạng thái cũ lên RealtimeGateway;<br>Endpoint trả về 200 OK kèm SyncResult =<br>DROPPED_OUTDATED.|
|Kết quả thực tế (Actual /<br>Status)|Pending|



### **_2.16.3. TC_UC16_03 – Ngoại lệ (EX2): Gói tin sai định dạng (mức pin âm) hoặc resourceId không tồn tại trong danh mục._** 

|**Trường thông tin**|**Đặc tả kịch bản**|
|---|---|
|Test Case ID|TC_UC16_03|
|Use Case liênquan|UC16 – Cậpnhật trạngthái tài nguyên|
|Mô tả kịch bản|Ngoại lệ (EX2): Gói tin sai định dạng (mức pin âm) hoặc resourceId<br>khôngtồn tại trongdanh mục.|
|Tiền điều kiện|1. Hệ thống đang sẵn sàng nhận gói tin từ Bộ giả lập dữ liệu.<br>|
|(Preconditions)|2. Mã tài nguyên "EB_NOT_FOUND" khôngtồn tại tronghệ thống.|



|**Trường thông tin**|**Đặc tả kịch bản**|
|---|---|
|Dữ liệu đầu vào (Input<br>Data)|Trường hợp A: packetId = "PKT_ERR1", resourceId = "EB_01",<br>batteryLevel = -10, packetTimestamp = 10:06:00.<br>Trường hợp B: packetId = "PKT_ERR2", resourceId =<br>"EB_NOT_FOUND", status = AVAILABLE, batteryLevel = 90,<br>packetTimestamp= 10:06:00.|
|Kết quả mong đợi<br>(Expected Result)|1. Trường hợp A ném InvalidPacketException; Trường hợp B ném<br>ResourceNotFoundException.<br>2. Hệ thống ghi nhận lỗi tích hợp (INTEGRATION_ERROR) vào<br>AuditLog và bỏ qua gói tin.<br>3. Endpoint trả về HTTP 400 Bad Request cho Bộgiả lậpdữ liệu.|
|Kết quả thực tế (Actual /|Pending|
|Status)|2.17. Test case cho UC17 - Xác thựcqua SSO|



### **_2.16.4. TC_UC16_04 – Luồng thay thế (AF1 – NFR07): Gói tin gắn cờ mô phỏng What-If chỉ ghi vào môi trường ảo cách ly, không ảnh hưởng Operational DB._** 

|**Trường thông tin**|**Đặc tả kịch bản**|
|---|---|
|Test Case ID|TC_UC16_04|
|Use Case liênquan|UC16 – Cậpnhật trạngthái tài nguyên|
|Mô tả kịch bản|Luồng thay thế (AF1 – NFR07): Gói tin gắn cờ mô phỏng What-If<br>chỉ ghi vào môi trường ảo cách ly, không ảnh hưởng Operational<br>DB.|
|Tiền điều kiện<br>(Preconditions)|1. Xe EB_01 trong Operational DB có status = AVAILABLE,<br>batteryLevel = 90.0%, lastUpdatedAt = 10:00:00.<br>2. SandboxStateStore cho kịch bản SCN_01 đã được khởi tạo.|
|Dữ liệu đầu vào (Input<br>Data)|packet = { packetId: "PKT_SIM_01", resourceId: "EB_01", status:<br>MAINTENANCE, batteryLevel: 12.0, packetTimestamp: 2026-11-<br>13T10:10:00, isSimulation: true}|
|Kết quả mong đợi<br>(Expected Result)|1. Hệ thống điều hướng gói tin tới<br>SandboxStateStore.upsertSimulatedState(packet).<br>2. Bản sao EB_01 trong SandboxStateStore cập nhật status =<br>MAINTENANCE, batteryLevel = 12.0%.<br>3. Operational DB của EB_01 vẫn giữ nguyên hoàn toàn (status =<br>AVAILABLE, batteryLevel = 90.0%, lastUpdatedAt = 10:00:00)<br>(NFR07).<br>4. Trả về HTTP 200 OK(SyncResult = UPDATED_SANDBOX).|
|Kết quả thực tế (Actual /<br>Status)|Pending|



## **2.17. Test case cho UC17 – Xác thực qua SSO** 

### **_2.17.1. TC_UC17_01 – Đăng nhập SSO thành công_** 

|**Trường thông tin**|**Đặc tả kịch bản**|
|---|---|
|Test Case ID|TC_UC17_01|
|Use Case liênquan|UC17 – Xác thựcqua SSO|
|Mô tả kịch bản|ĐăngnhậpSSO thành công|
|Tiền điều kiện<br>(Preconditions)|Tài khoản SSO hợp lệ và được ánh xạ quyền trong Hub.|



|**Trường thông tin**|**Đặc tả kịch bản**|
|---|---|
|Dữ liệu đầu vào (Input<br>Data)|Lần 1: tài khoản sinh viên An.<br>Lần 2: tài khoản nhân viên vận hành.<br>Thao tác: đăngnhậpSSO bằngtừngtài khoản.|
|Kết quả mong đợi<br>(Expected Result)|1. Tạo phiên với đúng vai trò.<br>2. Hiển thị giao diện tương ứng; ghi lịch sử đăng nhập.<br>3. Không yêu cầu nhậplại thôngtin nếu SSO đã cóphiên hợplệ.|
|Kếtquả thực tế / Status|Pending– Chưa thực hiện kiểm thử.|



### **_2.17.2. TC_UC17_02 – Hủy đăng nhập_** 

|**Trường thông tin**|**Đặc tả kịch bản**|
|---|---|
|Test Case ID|TC_UC17_02|
|Use Case liênquan|UC17 – Xác thựcqua SSO|
|Mô tả kịch bản|Hủyđăngnhập|
|Tiền điều kiện<br>(Preconditions)|Đang ở bước đăng nhập SSO; có thể có lựa chọn xe tạm.|
|Dữ liệu đầu vào (Input<br>Data)|Thao tác: chọn Hủy hoặc Từ chối tại SSO.|
|Kết quả mong đợi<br>(Expected Result)|1. Không tạo phiên mới.<br>2. Trở về trangchủ; xóa lựa chọn đặt xe tạm nếu có.|
|Kếtquả thực tế / Status|Pending– Chưa thực hiện kiểm thử.|



### **_2.17.3. TC_UC17_03 – Thông tin sai hoặc tài khoản bị khóa_** 

|**Trường thông tin**|**Đặc tả kịch bản**|
|---|---|
|Test Case ID|TC_UC17_03|
|Use Case liênquan|UC17 – Xác thựcqua SSO|
|Mô tả kịch bản|Thôngtin sai hoặc tài khoản bị khóa|
|Tiền điều kiện<br>(Preconditions)|SSO được cấu hình trả kết quả từ chối.|
|Dữ liệu đầu vào (Input<br>Data)|Lần 1: nhập sai thông tin đăng nhập.<br>Lần 2: dùngtài khoản bị khóa.|
|Kết quả mong đợi|1. Hiển thị lỗi phù hợp.<br>|
|(Expected Result)|2. Khôngtạophiên Hub; khôngcấp quyền truycập.|
|Kếtquả thực tế / Status|Pending– Chưa thực hiện kiểm thử.|



### **_2.17.4. TC_UC17_04 – SSO không phản hồi_** 

|**Trường thông tin**|**Đặc tả kịch bản**|
|---|---|
|Test Case ID|TC_UC17_04|
|Use Case liênquan|UC17 – Xác thựcqua SSO|
|Mô tả kịch bản|SSO không phản hồi|
|Tiền điều kiện<br>(Preconditions)|Mô phỏng SSO mất kết nối hoặc không trả lời trong thời gian chờ đã<br>cấu hình.|
|Dữ liệu đầu vào (Input<br>Data)|Thao tác: bắt đầu đăng nhập hoặc gửi kết quả để xác minh.|
|Kết quả mong đợi<br>(Expected Result)|1. Thông báo tạm thời không thể đăng nhập và cho phép thử lại.<br>2. Khôngtạophiên mới khi chưa xác minh thành công.|
|Kếtquả thực tế / Status|Pending– Chưa thực hiện kiểm thử.|



