function validate_name()
{
  var str = document.getElementById("name").value;
  var name_message = document.getElementById("name-message");
  if (str.length >= 5){
    name_message.style.display = "inline-block";
    name_message.innerHTML = "<span style = 'color: green; padding-right: 15px '> Restaurant Name accepted &#9989;</span>";

    document.getElementById("submit-btn").disabled = false;
    return true;
  }
   else{
    name_message.style.display ="inline-block";
    name_message.innerHTML = "<span style= 'color: red;'> Restaurant Name must be more than 5 characters</span>";
    document.getElementById("submit-btn").disabled = true;
  }
}


function validate_zip_code()
{
    var str = document.getElementById("zip-code").value;
    var zip_message = document.getElementById("zip-message");
    if (((/^[0-9]{5}$/.test(str) ))){
        zip_message.style.display = "inline-block";
        zip_message.innerHTML = "<span style='color: green;'> Valid Zip-code &#9989;</span>";
        document.getElementById("submit-btn").disabled = false;
        return true; 
    }

    else {
        zip_message.style.display ="inline-block";
        zip_message.innerHTML = "<span style='color: red;'>Zipcode must contain 5 digits</span>";
        document.getElementById("submit-btn").disabled = true; 
    }
}

function validate_number(){
    var str = document.getElementById("number").value;
    var number_message = document.getElementById("number-message");
    //if (((/^[0-9]{10}$/.test(str))) && str.length >= 2){
    if ( str.length >= 2 && (/^[0-9]+/.test(str))){
        number_message.style.display = "inline-block";
        number_message.innerHTML = "<span style='color: green;'> Valid number &#9989;</span>";
        document.getElementById("submit-btn").disabled = false;
        return true; 
    }

    else {
        number_message.style.display ="inline-block";
        number_message.innerHTML = "<span style='color: red;'>Number must be more than 2 digits</span>";
        document.getElementById("submit-btn").disabled = true; 
    }
}


function validate_street()
{
    var str = document.getElementById("street").value;
    var street_message = document.getElementById("street-message");
    if (str.length >= 7){
        street_message.style.display = "inline-block";
        street_message.innerHTML = "<span style='color: green; padding-right: 15px; ' > valid address &#9989;</span>";


        document.getElementById("submit-btn").disabled = false;
        return true; 
    }

    else {
        street_message.style.display ="inline-block";
        street_message.innerHTML = "<span style='color: red;'>Street adress  must be more than 7  characters</span>";
        document.getElementById("submit-btn").disabled = true; 
    }
}

function validate_city()
{
    var str = document.getElementById("city").value;
    var city_message = document.getElementById("city-message");
    if (str.length >= 5){
        city_message.style.display = "inline-block";
        city_message.innerHTML = "<span style='color: green; padding-right: 15px; ' > City validated &#9989;</span>";


        document.getElementById("submit-btn").disabled = false;
        return true; 
    }

    else {
        city_message.style.display ="inline-block";
        city_message.innerHTML = "<span style='color: red;'>City must be more than 5  characters</span>";
        document.getElementById("submit-btn").disabled = true; 
    }
}

function validate_description(){
    var str = document.getElementById("description").value;
    var description_message = document.getElementById("description-message");
    if (str.length >= 20){
        description_message.style.display = "inline-block";
        description_message.innerHTML = "<span style='color: green; padding-right: 15px; ' > Description looks good! &#9989;</span>";


        document.getElementById("submit-btn").disabled = false;
        return true; 
    }

    else {
        description_message.style.display ="inline-block";
        description_message.innerHTML = "<span style='color: red;'> Please write a description of at least 20 characters</span>";
        document.getElementById("submit-btn").disabled = true; 
    }
}
