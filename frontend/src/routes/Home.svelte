<script>
  import fastapi from "../lib/api"
  import {link} from 'svelte-spa-router'

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
    <!--
    // a 태그에 use:link를 사용하는 이유 (해시 라우팅)
    use:link 속성을 사용시 항상 /# 문자가 선행되며 브라우저는 이 경로를 하나의 페이지로 인식하여
    새로 고침을 하더라도 서버로 요청이 발생하지 않는다.
    -->
    <li><a use:link href="/detail/{question.id}">{question.subject}</a></li>
  {/each}
</ul>