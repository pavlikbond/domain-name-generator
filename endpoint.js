async function query(data) {
  const response = await fetch("https://d0ltfp2kv5l7u1h9.us-east-1.aws.endpoints.huggingface.cloud", {
    headers: {
      Accept: "application/json",
      Authorization: "Bearer YOUR_HUGGING_FACE_TOKEN_HERE",
      "Content-Type": "application/json",
    },
    method: "POST",
    body: JSON.stringify(data),
  });
  const result = await response.json();
  return result;
}

query({
  business_description: "A coffee shop with organic beans and pasteries",
  inputs: "",
}).then((response) => {
  console.log(JSON.stringify(response));
});
