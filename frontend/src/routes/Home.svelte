<script>
  import fastapi from "../lib/api"
  import {link} from 'svelte-spa-router'
  import {page} from '../lib/store'
  // 한국의 날짜 형식으로 표시하기위해 "ko"라는 값으로 로케일 설정을 해야한다.
  import moment from 'moment/min/moment-with-locales'
  moment.locale('ko')

  // question_list에 최초 빈 리스트를 초깃값으로 설정했다 만약 이렇게 하지 않을 경우 fetch 함수는 비동기 방식으로 실행되기 때문에
  // 요청하는 중에 HTML 영역의 each 문이 실행되고 값이 없어 오류가 발생한다. 따라서 반복문을 사용할 경우 해당 값을 빈 리스트로 초기화하는 것이 좋다.
  let question_list = []
  let size = 10
  // let page = 0 // 스토어 변수 추가로 인해 주석 처리
  let total = 0
  /*
  Math.ceil 함수는 소숫값이 존재할 때 값을 올리는 역할을 하는 함수로
  예시로 전체가 12개 게시물이 있고 한페이지에 표시할 갯수가 10개라면 total/size의 계산값은 1.2가 됨으로
  Math.ceil 함수로 인해 전체 페이지 개수는 2가 된다.

  변수 앞에 $: 기호가 붙으면 스벨트에서는 반응형 변수가 된다. 
  즉 total변수의 값이 API 호출로 인해 값이 변하면 total_page 변수의 값도 실시간으로 재계산된다.
  */
  $: total_page = Math.ceil(total/size)

  // function get_question_list(_page) {
  //   // fetch("http://127.0.0.1:8000/api/question/list").then((response) =>{
  //   //   response.json().then((json) => {
  //   //     question_list = json
  //   //   })
  //   // })
    
  //   // fastapi 함수를 만들어서 사용
  //   fastapi('get', '/api/question/list', {}, (json) =>{
  //       // question_list = json

  //       // API 결과 내용이 배열에서 딕셔너리 형태로 변경되었고 question_list라는 이름으로 데이터가 전달 되기에
  //       // json.question_list로 변경한다.
  //       question_list = json.question_list
  //   })
  // }

  function get_question_list(_page){
    // _page 매개변수를 추가하여 페이지 번호 입력으로 API를 호출한다.

    let params = {
      page: _page,
      size: size,
    }

    fastapi('get', '/api/question/list', params, (json) => {
      question_list = json.question_list
      $page = _page
      total = json.total
    })
  }

  // $: get_question_list($page)가 해당하는 의미는 
  // page값이 변경될 경우 해당 함수도 다시 호출하라는 의미 
  $: get_question_list($page)
</script>

<div class="container my-3">
  <table class="table">
    <thead>
      <tr class="table-dark">
        <th>번호</th>
        <th>제목</th>
        <th>작성일시</th>
      </tr>
    </thead>
    <tbody>
      {#each question_list as question, i}
      <tr>
        <td>{total - ($page - size) - i}</td>
        <td>
          <!--
          // a 태그에 use:link를 사용하는 이유 (해시 라우팅)
          use:link 속성을 사용시 항상 /# 문자가 선행되며 브라우저는 이 경로를 하나의 페이지로 인식하여
          새로 고침을 하더라도 서버로 요청이 발생하지 않는다.
          -->
          <a use:link href="/detail/{question.id}">{question.subject}</a>
        </td>
        <td>{moment(question.create_date).format("YYYY년 MM월 DD일 a hh:mm")}</td>
      </tr>
      {/each}
    </tbody>
  </table>
  <!-- 페이징 처리 시작 -->
  <ul class="pagination justify-content-center">
    <!-- 이전 페이지 -->
    <li class="page-item {$page <= 0 && 'disabled'}">
      <button class="page-link" on:click={() => get_question_list($page-1)}>이전</button>
    </li>
    <!-- 페이지 번호 -->
    {#each Array(total_page) as _, loop_page}
    {#if loop_page >= $page-5 && loop_page <= $page+5}
    <li class="page-item {loop_page === $page && 'active'}">
      <button on:click={() => get_question_list(loop_page)} class="page-link">{loop_page+1}</button>
    </li>
    {/if}
    {/each}
    <!-- 다음 페이지 -->
    <li class="page-item {$page >= total_page-1 && 'disabled'}">
      <button class="page-link" on:click={() => get_question_list($page+1)}>다음</button>
    </li>
  </ul>
  <!-- 페이징 처리 끝-->
  <a use:link href="/question-create" class="btn btn-primary">질문 등록하기</a>
</div>