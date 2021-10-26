# CRUD API 구현하기

### 1. Description
   
   - 사용한 프레임워크: flask
   - 사용한 데이터베이스: sqlite3의 인메모리데이터베이스
   - 사용자 등록: 데이터베이스에 해당하는 id가 없는 경우 데이터베이스에 id와 단방향 해쉬로 decrypt된 pwd를 저장합니다. 
   - 사용자 로그인: 데이터베이스에 해당하는 id와 pwd가 있는지 확인한 후 일치하는 경우 JWT를 사용해 발급한 access_token과 refresh_token을 넘겨줍니다.
   - 토큰 refresh: access_token이 만료된 경우 새로운 access_token을 발급해줍니다.  
   - 게시글 읽기: 데이터베이스 쿼리 내 limit와 offset를 활용하여 url 매개변수로 들어온 page와 per_page를 입력받아 pagination을 구현했습니다.
   - 게시글 쓰기: access_token을 헤더파일에 추가하여 로그인이 확인된 사용자일 경우에만 data로 들어온 title과 content로 게시글을 작성합니다.
   - 게시글 수정: access_token을 헤더파일에 추가하여 수정할 글을 작성할 사용자일 경우에만 data로 들어온 title과 content로 게시글을 수정합니다.
   - 게시글 삭제: access_token을 헤더파일에 추가하여 삭제를 원하는 게시글의 작성자일 경우에만 게시글을 삭제합니다.
   
### 2. API Usage Example(request/response)
1) app.py 실행
```bash
nohup python app.py &
```
2-1) 사용자 등록 
- request
```bash
curl -d '{"id":"id", "pwd":"pwd"}' -H "Content-Type: application/json" -X POST http://127.0.0.1:5000/user/register
```
2-2) 사용자 로그인 
- request
```bash
curl -d '{"id":"id", "pwd":"pwd"}' -H "Content-Type: application/json" -X POST http://127.0.0.1:5000/user/login
```
2-3) 토큰 refresh 
- request
```bash
curl -H "Content-Type: application/json" -H "Authorization: Bearer access_token" -X POST http://127.0.0.1:5000/token/refresh
```
2-4) 게시글 등록 
- request
```bash
curl -d '{"title":"hi","content":"hello"}' -H "Content-Type: application/json" -H "Authorization: Bearer access_token" -X POST http://127.0.0.1:5000/post/create
```
2-5) 특정 게시글 조회 
- request
```bash
curl -H "Content-Type: application/json" -X  GET http://127.0.0.1:5000/post/view?num=0
```
2-6) 전체 게시글 조회 
- request
```bash
curl -H "Content-Type: application/json" -X  GET http://127.0.0.1:5000/post/viewList?page=1&per_page=5
```
2-7) 게시글 수정
- request
```bash
curl -d '{"title":"hi","content":"not hello"}' -H "Content-Type: application/json" -H "Authorization: Bearer access_token" -X  PATCH http://127.0.0.1:5000/post/update/1
```
2-8) 게시글 삭제
- request
```bash
curl -H "Content-Type: application/json" -H "Authorization: Bearer access_token" -X DELETE
http://127.0.0.1:5000/post/delete/1
```
