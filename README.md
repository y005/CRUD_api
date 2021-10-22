# [[위코드 x 원티드] 백엔드 프리온보딩 선발 과제](https://wecode.notion.site/x-2f1edca34653419d8e109df1816197c2)

### 1. 구현한 방법과 이유


### 2. 자세한 실행 방법(endpoint 호출방법)

```bash
   
   import requests

   url = "https://yh-finance.p.rapidapi.com/market/v2/get-quotes"

   querystring = {"region":"US","symbols":"AMD,IBM,AAPL"}

   headers = {
      'x-rapidapi-host': "yh-finance.p.rapidapi.com",
      'x-rapidapi-key': "f977847401mshd7a2fe4cba6191fp1ae565jsnf4676589249d"
   }

   response = requests.request("GET", url, headers=headers, params=querystring)

   print(response.text)
```

### 3. api 명세(request/response 서술 필요)
