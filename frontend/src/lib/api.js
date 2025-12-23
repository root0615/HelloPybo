const fastapi = (operation, url, params, success_callback, failure_callback) => {
    /*
    operation: 데이터를 처리하는 방법(소문자) ex) get, post, put, delete
    url: 요청 URL, 백엔드 서버의 호스트명 이후 URL만 전달.
    params: 요청 데이터
    success_callback: API 호출 성공시 수행할 함수, 전달된 함수에는 API 호출시 반환되는 json이 입력으로 주어짐.
    failure_callback: API 호출 실패시 수행할 함수, 전달된 함수에는 오류값이 입력으로 주어짐.
    */
    let method = operation
    let content_type = 'application/json'
    let body = JSON.stringify(params)   // get이 아닌 경우 이와 같이 params를 JSON 문자열로 변경

    let _url = import.meta.env.VITE_SERVER_URL+url
    if(method === 'get'){
        // URLSearchParams({a:1, b:2}): ?a=1&b=2 와 같은 형태의 쿼리스트링을 생성, 파싱, 수정, 인코딩하기 위한 web 표준 API
        // GET 방식으로 요청시에만 사용
        _url += "?" + new URLSearchParams(params)
    } 

    let options = {
        method: method,
        headers: {
            "Content-Type": content_type
        }
    }

    if(method !== 'get'){
        options['body'] = body
    }

    fetch(_url, options)
        .then(response =>{
            response.json()
                .then(json => {
                    if(response.status >= 200 && response.status < 300) {
                        if(success_callback){
                            success_callback(json)
                        }
                    }else {
                        if(failure_callback) {
                            failure_callback(json)
                        }else {
                            alert(JSON.stringify(json))
                        }
                    }
                })
                .catch(error =>{
                    alert(JSON.stringify(error))
                })
        })
}

// api.js 파일에서 기본으로 내보낼 것은 fastapi이다.
// 즉 다른 파일에서 가져가서 사용할 수 있게 해준다.
export default fastapi