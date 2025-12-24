<script>
    import fastapi from "../lib/api"
    import Error from "../components/Error.svelte"

    // svelte에서 export let 변수는 '이 컴포넌트는 params라는 외부 입력을 받는다'라는 선언이다.
    export let params = {}
    let question_id = params.question_id
    // console.log('question_id:' + question_id)
    // 질문 한 건에 대한 상세 정보이므로 {} 로 초기화 해야한다
    // {answers:[]} 를 넣는 이유는 밑에 each 문에서 question.answers를 참조하고 있기 때문에 아직 조회가 안되면 오류 발생함으로 미리 넣어준다.
    let question = {answers:[]}
    let content = ""
    let error = {detail:[]}

    function get_question() {
        fastapi("get", "/api/question/detail/" + question_id, {}, (json) => {
            question = json
        })
    }

    get_question()

    function post_answer(event) {
        event.preventDefault()
        let url = "/api/answer/create/" + question_id
        // POST 방식으로 보내기위해 파라미터를 정의해준다.
        let params = {
            content: content
        }
        fastapi('post', url, params,
            (json) => {
                // 답변 등록이 성공했을 때 textarea 내용을 지우기위해 content를 빈 문자열로 대입했다.
                content = ''
                // 오류가 발생한 이후 재시도 시 성공하면 오류 메시지를 없애기 위해 초기화
                error = {detail:[]}
                // 상세 화면에 새로운 결과값을 반영하기 위해 get_question()으로 다시 불러들임
                get_question()
            },
            // failure_callback 함수 자리로 실패할 경우에 실행된다.
            (err_json) => {
                error = err_json
            }
        )
    }
</script>

<h1>{question.subject}</h1>
<div>
    {question.content}
</div>
<ul>
    {#each question.answers as answer}
        <li>{answer.content}</li>
    {/each}
</ul>
<!--
위에서 import로 Error 컴포넌트를 가져왔기에 <Error> 태그를 사용하고
Error(자식) 컴포넌트 안에 export let error로 props 이름으로 지정했기에
왼쪽 error는 해당 이름을 그대로 써준다. 오른쪽 error는 현재 Detail(부모)의 변수 이름을 넣어준 내용이다.
-->
<Error error={error} />
<form method="post">
    <textarea rows="15" bind:value={content}></textarea>
    <!--답변 등록 버튼을 누르면 post_answer() 함수가 실행된다.-->
    <input type="submit" value="답변등록" on:click={post_answer}>
</form>