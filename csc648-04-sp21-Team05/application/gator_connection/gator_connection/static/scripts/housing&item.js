


function validate_title()
{
    var str = document.getElementById("title").value;
    var title_message = document.getElementById("title-message");
    if (str.length >= 10){
        title_message.style.display = "inline-block";
        title_message.innerHTML = "<span style='color: green; padding-right: 15px; ' > Title accepted &#9989;</span>";


        document.getElementById("submit-btn").disabled = false;
        return true; 
    }

    else {
        title_message.style.display ="inline-block";
        title_message.innerHTML = "<span style='color: red;'>Title must be more than 10 characters</span>";
        document.getElementById("submit-btn").disabled = true; 
    }
}


function validate_pricing()
{
    var str = document.getElementById("pricing").value;
    var pricing_message = document.getElementById("pricing-message");

     if (str.length < 8 && ((/^\d+(?:\.\d{2})$/.test(str) )) ){
        pricing_message.style.display = "inline-block";
        pricing_message.innerHTML = "<span style='color: green;'> &#9989;</span>";
        document.getElementById("submit-btn").disabled = false;
        return true; 
    }

    else {
        pricing_message.style.display ="inline-block";
        pricing_message.innerHTML = "<span style='color: red;'>Please enter a reasonable amount and correct format, eg : 200.00 </span>";
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
    /*
    if(document.getElementById("zip-code").value(/^\d{5}(-\d{4})?(?!-)$/))
    {
        document.getElementById("zip-message").innerHTML = "<span style='color: green;'>This is right!</span>";
        if(document.getElementById("zip-code").value.includes(isValidZip))
        {
            document.getElementById("submit-btn").disabled = false; 
            return true;
        }

        return true;
    }
    else 
    {
        document.getElementById("zip-message").innerHTML = "<span style='color: red;'>Your input is too long, please reduce the amount </span>";
    }
    */
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


function validate_email(){
    if(document.getElementById("email").value.includes("@mail.sfsu.edu")||document.getElementById("email").value.includes("@sfsu.edu"))
    {
        document.getElementById("email_message").innerHTML = "<span style='color: green;'>This is a valid SFSU email!</span>";
        if((document.getElementById("email").value.includes("@mail.sfsu.edu") ||document.getElementById("email").value.includes("@sfsu.edu") )&& document.getElementById("graduation-date").value.includes("-"))
        {
            return true;
        }

        return true;
    }
    else if(document.getElementById("email").value.length >= 45)
    {
        document.getElementById("email_message").innerHTML = "<span style='color: red;'>Your input is too long, please reduce the amount </span>";
        document.getElementById("student_register_button").disabled = true; 
        return false;
    }
    else
    {
        document.getElementById("email_message").innerHTML = "<span style='color: red;'>This is not a valid SFSU email, Please enter a valid SFSU email </span>";
        document.getElementById("student_register_button").disabled = true; 
        return false;
    }
}

function validate_phone_number()
{
    var str = document.getElementById("phone_number").value;
    var message = document.getElementById("phone_number_message");
    var n = str;
    console.log(document.getElementById("phone_number").value); // javascript
  
    // if ( str.length >= 0 && (/^[0-9]+/.test(str))){
    //     message.style.display = "inline-block";
    //     message.innerHTML = "<span style='color: green;'> Valid number &#9989;</span>";
    //     document.getElementById("submit-btn").disabled = false;
    //     return true; 
    // }

    // else {
    //     message.style.display ="inline-block";
    //     message.innerHTML = "<span style='color: red;'>Number must be more than 2 digits</span>";
    //     document.getElementById("submit-btn").disabled = false; 
    // }
}
