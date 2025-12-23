<script>
  import fastapi from "../lib/api";
  // question_list에 최초 빈 리스트를 초깃값으로 설정했다 만약 이렇게 하지 않을 경우 fetch 함수는 비동기 방식으로 실행되기 때문에
  // 요청하는 중에 HTML 영역의 each 문이 실행되고 값이 없어 오류가 발생한다. 따라서 반복문을 사용할 경우 해당 값을 빈 리스트로 초기화하는 것이 좋다.
  let question_list = []


  
  function get_question_list() {
    // fetch("http://127.0.0.1:8000/api/question/list").then((response) =>{
    //   response.json().then((json) => {
    //     question_list = json
    //   })
    // })
    
    // fastapi 함수를 만들어서 사용
    fastapi('get', '/api/question/list', {}, (json) =>{
        question_list = json
    })
  }

  get_question_list()
</script>

<ul>
  {#each question_list as question}
    <li>{question.subject}</li>
  {/each}
</ul>