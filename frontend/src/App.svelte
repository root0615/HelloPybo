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

<script>
  // svelte-spa-router : 스벨트에서 라우터 기능을 담당하는 라이브러리
  import Router from 'svelte-spa-router'
  import Home from "./routes/Home.svelte"
  import Detail from "./routes/Detail.svelte"
  import QuestionCreate from "./routes/QuestionCreate.svelte"

  const routes = {
    '/': Home,
    '/detail/:question_id': Detail,
    '/question-create': QuestionCreate,
  }
</script>

<Router {routes}/>


