function myFunc() {
  let numInput = document.getElementById("numInput");
  while (numInput.nextSibling) {
    numInput.nextSibling.remove();
  }

  let numInputval = document.getElementById("numInput").value;
  for (var i = numInputval; i > 0; i--) {
    var newDiv = document.createElement("div");
    newDiv.setAttribute("id", "demo" + i);
    newDiv.innerHTML = "*** TEST ***";
    numInput.parentNode.insertBefore(newDiv, numInput.nextSibling);
  }
}
