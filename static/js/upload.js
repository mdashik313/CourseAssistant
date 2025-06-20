function setfilename(val) {
  var fileName = val.substr(val.lastIndexOf("\\") + 1, val.length);
  document.getElementById("uploadFile").textContent = fileName;
}

function clearUpload() {
  document.getElementById("file-upload").value = "";
  document.getElementById("uploadFile").textContent = "";
}
