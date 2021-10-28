function validate_description()
{
    var str = document.getElementById("description").value;
    var title_message = document.getElementById("description-message");
    if (str.length >= 20){
        title_message.style.display = "inline-block";
        title_message.innerHTML = "<span style='color: green; padding-right: 15px; ' > Description accepted &#9989;</span>";


        document.getElementById("submit-btn").disabled = false;
        return true; 
    }

    else {
        title_message.style.display ="inline-block";
        title_message.innerHTML = "<span style='color: red;'>Description must be more than 20 characters</span>";
        document.getElementById("submit-btn").disabled = true; 
    }
}

let mailRegex = /^[a-zA-Z][a-zA-Z0-9\-\_\.]+@[a-zA-Z0-9]{2,}\.[a-zA-Z0-9]{2,}$/;
function validate_email()
{
 
    if(document.getElementById("email").value.match(mailRegex))
    {
        document.getElementById("email_message").innerHTML = "<span style='color: green;'>This is a valid email!</span>";
        if((document.getElementById("email").value.match(mailRegex)))
        {
            document.getElementById("submit_btn").disabled = false; 
            return true;
        }

        return true;
    }
    else if(document.getElementById("email").value.length >= 45)
    {
        document.getElementById("email_message").innerHTML = "<span style='color: red;'>Your input is too long, please reduce the amount </span>";
        document.getElementById("submit_btn").disabled = true; 
        return false;
    }
    else
    {
        document.getElementById("email_message").innerHTML = "<span style='color: red;'>This is not a valid email, Please enter a valid email </span>";
        document.getElementById("submit_btn").disabled = true; 
        return false;
    }
}

