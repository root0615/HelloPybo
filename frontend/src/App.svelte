<script>
  // question_list에 최초 빈 리스트를 초깃값으로 설정했다 만약 이렇게 하지 않을 경우 fetch 함수는 비동기 방식으로 실행되기 때문에
  // 요청하는 중에 HTML 영역의 each 문이 실행되고 값이 없어 오류가 발생한다. 따라서 반복문을 사용할 경우 해당 값을 빈 리스트로 초기화하는 것이 좋다.
  let question_list = []

  
  function get_question_list() {
    fetch("http://127.0.0.1:8000/api/question/list").then((response) =>{
      response.json().then((json) => {
        question_list = json
      })
    })
  }

  get_question_list()
</script>


<!-- 
// 반환 값의 JSON 형태를 그대로 출력하고 싶을 때 사용
<pre>
{JSON.stringify(question_list, null, 2)}
</pre> 

// 스벨트 문법 (조건문)
{#if 조건문1}
    <p>조건문1에 해당하면 실행</p>
{:else if 조건문2}
    <p>조건문2에 해당하면 실행</p>
{:else}
    <p>조건문1, 2 모두 해당하지 않으면 실행</p>
{/if}

// 스벨트 문법 (반복문)
{#each list as item, index}
    <p>순서: {index} </p>
    <p>{item}</p>
{/each}

// 스벨트 문법 (객체 표시)
{객체}
// 스벨트 문법 (객체 속성 표시)
{객체.속성}
-->

<ul>
  {#each question_list as question}
    <li>{question.subject}</li>
  {/each}
</ul>