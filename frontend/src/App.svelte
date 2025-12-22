<script>
  let message;

  fetch("http://127.0.0.1:8000/hello").then((respone) => {
    respone.json().then((json) => {
      message = json.message;
    });
  });
</script>

<h1>{message}</h1>