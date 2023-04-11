document.getElementById("upload-button").addEventListener("click", function () {
  document.getElementById("input-image").click();
});

document.getElementById("input-image").addEventListener("change", function () {
  let formData = new FormData();
  formData.append("file", this.files[0]);
  axios
    .post("/upload", formData, {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    })
    .then(function (response) {
      document.getElementById("output").src = response.data.image;
      document.getElementById("download").href = response.data.download_url;
    })
    .catch(function (error) {
      console.log(error);
    });
});