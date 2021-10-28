function announcements_change_searchbar_placeholder()
{
  /* 
  function is responsible for changing the search bar placeholder based
  on the dropdown bar value
  */
  var dropdown_value = document.getElementById('select_announcements').value;
  console.log(dropdown_value);
  if(dropdown_value == 'athletics')
  {
    console.log('in athelitics');
    document.getElementById('announcements_searchbar').placeholder = 'Search for Athletic Clubs!';
  }
  else if(dropdown_value == 'department')
  {
    console.log('in department');
    document.getElementById('announcements_searchbar').placeholder = 'Search for Department things!';
  }
  else if (dropdown_value == 'organization')
  {
    console.log('in organization');
    document.getElementById('announcements_searchbar').placeholder = 'Search for Organization Clubs!';
  }

}


function switchAnnouncementForm(event, announcementTypeForm) {
var i, tabContent, tabBtns;

// Get all forms that have class tab-content
tabContent = document.getElementsByClassName("announcements-form-content");


for(i = 0; i < tabContent.length; i++) {
  // sets all the displays to none
    tabContent[i].style.display = "none";
}

for(i = 0; i < tabContent.length; i++) {
  /*
  if account type form matches tabContent[i].id, changes the display to "block"
  which shows the appropriate form
  */
    if(announcementTypeForm == tabContent[i].id)
    {
      tabContent[i].style.display = "block";
    }   
}

// Get all tab bar btns with class tab-btn and remove the class active if they have it
tabBtns = document.getElementsByClassName("tab-announcements-btn")

for(i = 0; i < tabBtns.length; i++) {
    console.log(tabBtns[i]);
    tabBtns[i].className = tabBtns[i].className.replace(" active", "");
}

// adds active to the current form
event.currentTarget.className += " active";

}


function validate_sport()
{
  var str = document.getElementById("sport").value;
  var sport_message = document.getElementById("sport-message");
  if (str.length >= 3){
    sport_message.style.display = "inline-block";
    sport_message.innerHTML = "<span style = 'color: green; padding-right: 15px '> Sport accepted &#9989;</span>";

    disableSubmitBtn(false);
    return true;
  }
   else{
    sport_message.style.display ="inline-block";
    sport_message.innerHTML = "<span style= 'color: red;'> Sport title must be more than 3 characters</span>";
    disableSubmitBtn(true);
  }
}

function validate_department()
{
  var str = document.getElementById("department").value;
  var department_message = document.getElementById("department-message");
  if (str.length >= 5){
    department_message.style.display = "inline-block";
    department_message.innerHTML = "<span style = 'color: green; padding-right: 15px '> Department accepted &#9989;</span>";

    disableSubmitBtn(false);
    return true;
  }
   else{
    department_message.style.display ="inline-block";
    department_message.innerHTML = "<span style= 'color: red;'> Department title must be more than 3 characters</span>";
    disableSubmitBtn(true);
  }
}


function validate_organization_title(){
  var str = document.getElementById("organization_title").value;
  var organization_title_message = document.getElementById("organization-message");
  if (str.length >= 3){
      organization_title_message.style.display = "inline-block";
      organization_title_message.innerHTML = "<span style='color: green; padding-right: 18px; ' > Title for organization looks good! &#9989;</span>";

    disableSubmitBtn(false);
    return true;
  }
   else{
    organization_message.style.display ="inline-block";
    organization_title_message.innerHTML = "<span style= 'color: red;'> Organization title must be more than 3 characters</span>";
    disableSubmitBtn(true);
  }
}



function validate_description(){
  var str = document.getElementById("description").value;
  var description_message = document.getElementById("description-message");
  if (str.length >= 20){
      description_message.style.display = "inline-block";
      description_message.innerHTML = "<span style='color: green; padding-right: 18px; ' > Description looks good! &#9989;</span>";


      disableSubmitBtn(false);
      return true; 
  }

  else {
      description_message.style.display ="inline-block";
      description_message.innerHTML = "<span style='color: red;'> Please write a description of at least 20 characters</span>";
      disableSubmitBtn(true); 
  }
}

function validate_organization_description(){
  var str = document.getElementById("organization_description").value;
  var organization_description_message = document.getElementById("organization-description-message");
  if (str.length >= 20){
      organization_description_message.style.display = "inline-block";
      organization_description_message.innerHTML = "<span style='color: green; padding-right: 18px; ' > Description looks good! &#9989;</span>";


      disableSubmitBtn(false);
      return true; 
  }

  else {
      organization_description_message.style.display ="inline-block";
      organization_description_message.innerHTML = "<span style='color: red;'> Please write a description of at least 20 characters</span>";
      disableSubmitBtn(true); 
  }
}

function validate_department_description(){
  var str = document.getElementById("department_description").value;
  var department_description_message = document.getElementById("department-description-message");
  if (str.length >= 20){
      department_description_message.style.display = "inline-block";
      department_description_message.innerHTML = "<span style='color: green; padding-right: 18px; ' > Description looks good! &#9989;</span>";


      disableSubmitBtn(false);
      return true; 
  }

  else {
      department_description_message.style.display ="inline-block";
      department_description_message.innerHTML = "<span style='color: red;'> Please write a description of at least 20 characters</span>";
      disableSubmitBtn(true); 
  }
}

function disableSubmitBtn(disabled) {
  btns = document.getElementsByClassName("submit_btn");
  btnLength = btns.length;

  for(let i = 0; i < btnLength; i++) {
    console.log(btns[i]);
    btns[i].disabled = disabled;
  }

  return
}