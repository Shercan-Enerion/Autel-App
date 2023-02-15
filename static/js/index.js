var dataGetServer = {};
//function control show the elements cars numbers
function addedCars() {
  let cars = document.getElementsByClassName("carSim");
  while (cars.length > 0) {
    cars[cars.length - 1].remove();
  }
  let numInput = document.getElementById("tableData");
  while (numInput.nextSibling) {
    numInput.nextSibling.remove();
  }

  let numInputval = document.getElementById("numInput").value;
  for (var i = 1; i <= numInputval; i++) {
    var newDiv = document.createElement("div");
    newDiv.setAttribute("class", "container row carSim");
    newDiv.innerHTML = `        <div class="col">
                                    <input class="number form-control" type="number" value="${i}" readonly>
                                </div>
                                <div class="col">
                                    <input class="time form-control" name="starttime${i}" type="time">
                                </div>
                                <div class="col">
                                    <input class="number form-control" name="finaldate" type="number" id="duration${i}"
                                        placeholder="1">
                                </div>`;
    numInput.insertBefore(newDiv, numInput.nextSibling);
  }
}
// function for control adedd periods when the input new rates is true
function addedPeriod() {
  var newDiv = document.createElement("div");
  let periods = document.getElementsByClassName("periods");
  let divPeriod = document.getElementById("divPeriod");
  console.log(periods.length);
  newDiv.setAttribute(
    "class",
    "d-flex flex-wrap justify-content-between periods"
  );
  newDiv.innerHTML = `<div class="d-flex flex-column align-items-start">
                                    <div class="pt-1">Period</div>
                                    <div class="pb-1">
                                        <input type="number" id="period" class="number form-control" placeholder="1">
                                    </div>
                                </div>
                                <div class="d-flex flex-column align-items-start">
                                    <div class="pt-1">Start time</div>
                                    <div class="pb-1">
                                        <input type="time" class="time form-control" placeholder="07:00">
                                    </div>
                                </div>
                                <div class="d-flex flex-column align-items-start">
                                    <div class="pt-1">Rate period</div>
                                    <div class="pb-1">
                                        <input type="number" class="number form-control" placeholder="5">
                                    </div>
                                </div>`;
  divPeriod.insertBefore(newDiv, divPeriod.children[-1]);
}

//control for elements new rates and rates
const newRates = document.getElementById("newRates");
newRates.style.display = "none";
$("#newRates")[0].attributes.style.value = "display: none;";
$(document).ready(function () {
  $("#checkSimu").on("change", function () {
    if (this.checked) {
      $("#newRates")[0].attributes.style.value = "display: block;";
      $("#electricCo").autocomplete("disable");
      $("#sector").autocomplete("disable");
      $("#rateName").autocomplete("disable");
      $("#sector").prop("disabled", false);
      $("#rateName").prop("disabled", false);
    } else {
      $("#newRates")[0].attributes.style.value = "display: none;";
      $("#electricCo").autocomplete("enable");
      $("#sector").autocomplete("enable");
      $("#rateName").autocomplete("enable");
      $("#sector").prop("disabled", true);
      $("#rateName").prop("disabled", true);
    }
  });
});

// Type of the service
$(function () {
  let data = ["Residential", "Commercial", "Industrial", "Lighting"];
  $("#sector").autocomplete({
    source: data,
  });
  $("#rateName").autocomplete({
    source: [""],
  });
});
// companys and rates contract
$(function () {
  $("#electricCo").autocomplete({
    source: function (req, add) {
      let url =
        window.location.protocol +
        "//" +
        window.location.host +
        "/companyrate/?value=companies&substr=" +
        req.term;
      $.getJSON(url, function (data) {
        var suggestions = [];
        var maxResults = 20;
        var endResult = Math.min(maxResults, data.length);
        for (i = 0; i < endResult; i++) {
          suggestions.push(data[i]);
        }
        add(suggestions);
      });
    },
    delay: 75,
    minLength: 2,
  });
});
//get data to database
$(document).ready(function () {
  $("#electricCo").change(function () {
    $("#sector").prop("disabled", false);
  });
});
$(document).ready(function () {
  $("#sector").change(function () {
    company = document.getElementById("electricCo").value.replace(/&/g, "%26");
    sector = document.getElementById("sector").value.replace(/&/g, "%26");
    let url =
      window.location.protocol +
      "//" +
      window.location.host +
      "/companyrate/?value=rates&sector=" +
      sector +
      "&company=" +
      company;
    console.log(url);
    $("#rateName").prop("disabled", false);
    $.getJSON(url, function (data) {
      $("#rateName").autocomplete({
        source: data,
      });
    });
  });
});
$(document).ready(function () {
  $("#rateName").change(function () {
    let url2 =
      window.location.protocol +
      "//" +
      window.location.host +
      "/rates?sector=" +
      $("#sector").val() +
      "&company=" +
      $("#electricCo").val().replace(/&/g, "%26") +
      "&rate=" +
      $("#rateName").val();
    console.log(url2);
    $.getJSON(url2, function (data) {
      dataGetServer = data;
      console.log(dataGetServer);
      selectUpdate();
    });
  });
});
// update data with elements to perior company
function selectUpdate() {
  let i = 1;
  dataGetServer.energyratestructure.forEach((element) => {
    $("#periodCompany").append(`<option value="${i}">${i}</option>`);
    i++;
  });
  $("#periodCompany").selectpicker("refresh");
}
$(document).ready(function () {
  $("#periodCompany").change(function () {
    let i = $("#periodCompany").val() - 1;
    $("#rateVal").val(dataGetServer.energyratestructure[i][0].rate);
    // $("#period").val(dataGetServer.energyratestructure[i].period);
    // $("#time").val(dataGetServer.energyratestructure[i].time);
    // $("#periodRate").val(dataGetServer.energyratestructure[i].periodRate);
  });
});

//send form
document.addEventListener("DOMContentLoaded", function () {
  document
    .getElementById("formSim")
    .addEventListener("submit", validarFormulario);
});
//control the send database and block query
function validarFormulario(evento) {
  evento.preventDefault();
  var electricCo = document.getElementById("electricCo").value;
  var sector = document.getElementById("sector").value;
  var ratename = document.getElementById("rateName").value;
  if (electricCo.length > 4 && sector.length > 4 && ratename.length > 4) {
    alert("Data sent");
    this.submit();
  } else {
    alert("Missing data");
    return;
  }
}
