<script>
    import fastapi from "../lib/api"
    // svelte에서 export let 변수는 '이 컴포넌트는 params라는 외부 입력을 받는다'라는 선언이다.
    export let params = {}
    let question_id = params.question_id
    // console.log('question_id:' + question_id)
    let question = {}

    function get_question() {
        fastapi("get", "/api/question/detail/" + question_id, {}, (json) =>{
            question = json
        })
    }

    get_question()
</script>

<h1>{question.subject}</h1>
<div>
    {question.content}
</div>