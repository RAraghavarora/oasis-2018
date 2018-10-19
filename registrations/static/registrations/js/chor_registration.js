document.getElementById("closeIconDialog").addEventListener('click', function () {
  document.getElementById("overlay").style.opacity = 0;
  setTimeout(function () { document.getElementById("overlay").style.display = 'none'; document.getElementById("errorSpan").innerHTML = "" }, 350);
});

function showError(errorMsg) {
  document.getElementById("errorSpan").innerHTML = errorMsg;
  document.getElementById("overlay").style.display = "flex";
  document.getElementById("overlay").style.opacity = 1;
}

$(document).ready(function () {
  $("#back-btn").css('display', "none");
})

function checkEmail(email) {

  // var email = document.getElementById('txtEmail');
  var filter = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;

  if (!filter.test(email)) {
    // 'txtEmail'.textContent = 'Please provide a valid email address';
    // alert('Please provide a valid email address');
    // email.focus;
    return false;
  }
  else
    return true;
}
function checkEvents() {
  var eventsSelected = $("#event-select").val();
  if (eventsSelected.length == 0) {
    alert('Please select an event');
    return false;
  }
}
function checkPhonenumber(mobn) {
  var phoneno = /^\d{10}$/;
  // var mobn = document.getElementById('mob-number');
  if (!phoneno.test(mobn)) {

    // alert("Provide a valid Mobile Number");
    return false;
  }
  else {
    return true;
  }
}

// function myFunction() {
//   return checkEmail() && phonenumber() && checkEvents();
// }


$(document).ready(function () {
  $('#event-select').select2({
    'placeholder': 'Event(s)',
    width: "100%",
  });
  $('#college').select2({
    width: "100%",
  });
});

URL = "https://bits-oasis.org/2018/registrations/";
// URL = "http://172.17.42.109:8000/registrations/";
$(document).ready(function () {
  var xhr = new XMLHttpRequest();
  xhr.open('GET', URL, true);
  xhr.send();

  xhr.onreadystatechange = processRequest;

  function processRequest(e) {

    if (xhr.readyState == 4 && xhr.status == 200) {
      var response = JSON.parse(xhr.responseText);
      var clgs = response.colleges,
        events = response.events;
      var collegeOption = "";
      var eventsOption = "";

      for (var i = 0; i < clgs.length; i++) {
        collegeOption += "<option>" + clgs[i] + "</option>";
      }

      for (var i = 0; i < events.length; i++) {
        eventsOption += "<option id='" + events[i].id + "'>" + events[i].name + "</option>";
      }

      // console.log(collegeOption);
      collegeElem = document.getElementById('college');
      collegeElem.innerHTML += collegeOption;
      // document.getElementById('college').append(collegeOption);
      eventsElem = document.getElementById('event-select');
      eventsElem.innerHTML += eventsOption;
      // console.log(eventsElem.innerHTML);
    }
  }
});

document.getElementById('submit-button').addEventListener('click', function () {
  let reCaptcha = document.getElementById('register-form').elements[document.getElementById('register-form').length- 2].value;
  var eventsSelected = $("#event-select").select2('val');
  var name = document.getElementById('name').value.trim();
  var city = document.getElementById('city').value.trim();
  var phone = document.getElementById('phoneNumber').value.trim();
  var email = document.getElementById('email').value.trim();
  var college = document.getElementById('college').value.trim();
  var head_of_society;
  var year_of_study;
  var gender;
  
  if (name != "" && city != "" && phone != "" && email != "" && college != "") {
    function gender() {
      if (document.getElementById('male').checked == true)
      gender = "male";
      else if (document.getElementById('female').checked == true)
      gender = "female";
      else
      gender = "others";
    }
    gender();
    function head() {
      if (document.getElementById('yes').checked == true)
      head_of_society = true;
      else
      head_of_society = false;
    }
    head();
    function year() {
      if (document.getElementById('one').checked == true)
      year_of_study = 1;
      else if (document.getElementById('two').checked == true)
      year_of_study = 2;
      else if (document.getElementById('three').checked == true)
      year_of_study = 3;
      else if (document.getElementById('four').checked == true)
      year_of_study = 5;
      else if (document.getElementById('five').checked == true)
      year_of_study = 5;
    }
    year();
    // var xhr = new XMLHttpRequest();
    // xhr.open("POST", URL, true);
    
    // xhr.setRequestHeader("Content-Type", "application/json");
    
    // xhr.onreadystatechange = function () {
      //   if (this.readyState == XMLHttpRequest.DONE && this.status == 200 && this.responseText.status == 1) {
        //     console.log(this.responseText);
        //   }
        //   else {
          //     console.log(this.responseText);
          //   }
          // }
    if (checkPhonenumber(phone)) {
      if (checkEmail(email)) {
        if (eventsSelected !== null) {
          if(reCaptcha){
            x = JSON.stringify({
              events: eventsSelected,
              email: email,
              name: name,
              college: college,
              gender: gender,
              city: city,
              phone: phone,
              head_of_society: head_of_society,
              reCaptcha: reCaptcha,
              year_of_study: year_of_study
            });

            $.ajax({
              type: "POST",
              contentType: "application/json",
              url: URL,
              data: x,
              dataType: "json",
              complete: function (data) {
                data = (data.responseJSON);
                if (data.status == 0) {
                  showError('<h1>' + data.message + '</h1><h1>Please try again.</h1>');
                } else {
                    showError('<h1>' + data.message + '</h1>');
                }
              }
            });
          }
          else{
            showError('<h1>Please validate the reCaptcha</h1>');
          }
        }
        else {
          showError('<h1>Please select the event(s) you want to register for</h1>');
        }
      }
      else {
        showError('<h1>Please enter a valid email</h1>');
      }
    }
    else {
      showError('<h1>Please enter a valid phone number</h1>');
    }
  } else {
    showError('<h1>Please fill all the fields.</h1>');
  }

});

  //new