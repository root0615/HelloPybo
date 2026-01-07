<script>
    import {link} from 'svelte-spa-router'
    import {page} from '../lib/store'
</script>

<!-- 네비게이션 바 -->
<nav class="navbar navbar-expand-lg navbar-light bg-light border-bottom">
    <div class="container-fluid">
        <!-- 
        스토어에 page번호가 저장되는 경우 첫번째 페이지로 이동하지 않아 
        항상 첫페이지로 이동할 수 있도록 수정
         -->
        <a use:link class="navbar-brand" href="/" on:click={() => {$page = 0}}>Pybo</a>
        <!-- 아래 버튼 태그의 속성들은 햄버거 기능을 하는 부트스트랩 전용 코드이다. -->
        <button
            class="navbar-toggler"
            type="button"
            data-bs-toggle="collapse"
            data-bs-target="#navbarSupportedContent"
            aria-controls="navbarSupportedContent"
            aria-expanded="false"
            aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarSupportedContent">
            <ul class="navbar-nav me-auto mb-2 mb-lg-0">
                <li class="nav-item">
                    <a use:link class="nav-link" href="/user-create">회원가입</a>
                </li>
                <li class="nav-item">
                    <a use:link class="nav-link" href="/user-login">로그인</a>
                </li>
            </ul>
        </div>
    </div>
</nav>