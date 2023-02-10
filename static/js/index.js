function myFunc() {
  let numInput = document.getElementById("tableData");
  while (numInput.nextSibling) {
    numInput.nextSibling.remove();
  }

  let numInputval = document.getElementById("numInput").value;
  for (var i = 1; i <= numInputval; i++) {
    var newDiv = document.createElement("div");
    newDiv.setAttribute("class", "d-flex align-items-center ");
    newDiv.innerHTML = ` <div>
                                    <input class="number form-control" type="number" value="${i}" readonly>
                                </div>
                                <div>
                                    <input class="time form-control" name="starttime${i}" type="time">
                                </div>
                                <div>
                                    <input class="number form-control" name="finaldate" type="number" id="duration${i}"
                                        placeholder="1">
                                </div>
                                <div>
                                    
                                </div>`;
    numInput.insertBefore(newDiv, numInput.nextSibling);
  }
}
