import { writable } from "svelte/store"

// 쓰기 가능한 스토어 변수 page, writable(0) 에서 0은 초깃값을 0으로 설정한다는 의미
// export const page = writable(0)

// 스토어 변수가 지속성을 가질 수 있게 변경
/*
이름(key)과 초기값(initValue)을 입력받아 writable 스토어를 생성하여 리턴
localStorage에 해당 이름 값이 이미 존재하면 초기값 대신 기존 값을 스토어로 생성하여 리턴
localStorage에 저장하는 값은 항상 문자열로 유지하기 위해 저장은 JSON.stringify를 사용
읽을 떄는 JSON.parse를 사용한다.
*/
const persis_storage = (key, initValue) => {
    const storedValueStr = localStorage.getItem(key)
    const store = writable(storedValueStr != null ? JSON.parse(storedValueStr) : initValue)
    // store.subscribe() 함수는 스토어에 저장된 값이 변경될 때 실행되는 콜백 함수 이다.
    store.subscribe((val) => {
        localStorage.setItem(key, JSON.stringify(val))
    })
    return store

}

export const page = persis_storage("page", 0)