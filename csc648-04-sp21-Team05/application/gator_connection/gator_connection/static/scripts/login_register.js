

function openLoginForm(event, accountTypeForm) {

    var i, tabContent, tabBtns;

    // Get all forms that have class tab-content
    tabContent = document.getElementsByClassName("login-form-content")

    for(i = 0; i < tabContent.length; i++) {
        tabContent[i].style.display = "none";
    }

    // Get all tab bar btns with class tab-btn and remove the class active if they have it
    tabBtns = document.getElementsByClassName("tab-login-btn")

    for(i = 0; i < tabBtns.length; i++) {
        tabBtns[i].className = tabBtns[i].className.replace(" active", "");
    }

    // Show the current tab by adding class active to the button that caused the event
    document.getElementById(accountTypeForm).style.display = "block";
    event.currentTarget.className += " active";


}

function openRegisterForm(event, accountTypeForm) {
    var i, tabContent, tabBtns;

    // Get all forms that have class tab-content
    tabContent = document.getElementsByClassName("register-form-content")

    for(i = 0; i < tabContent.length; i++) {
        tabContent[i].style.display = "none";
    }

    // Get all tab bar btns with class tab-btn and remove the class active if they have it
    tabBtns = document.getElementsByClassName("tab-register-btn")

    for(i = 0; i < tabBtns.length; i++) {
        tabBtns[i].className = tabBtns[i].className.replace(" active", "");
    }

    // Show the current tab by adding class active to the button that caused the event
    document.getElementById(accountTypeForm).style.display = "block";
    event.currentTarget.className += " active";
}

function updateAdminRegisterForm() {
    // Get dropdown value
    adminType = document.getElementById("admin_type").value;
    console.log(adminType);

    // Get Organization text field
    organizationTextField = document.getElementById("organization");
    if (adminType == "Athletics") {
        organizationTextField.placeholder = "Sport"
    } else if(adminType == "Department") {
        organizationTextField.placeholder = "Department Name"
    } else if(adminType == "Organization") {
        organizationTextField.placeholder = "Organization Name"
    }
}


/* STUDENT REGISTER CHECK'S BEGIN */

function validate_sfsu_email()
{
    /* 
    Function here validates for sfsu email by checking if the input includes string "@mail.sfsu.edu", if it does it returns true, if not false.   
    Also, to check if people go out of order on the registering modal, there is also a check that checks if the other values from the fields are correct. If they are
    it will allow them to register.
    */

    if(document.getElementById("sfsu-email").value.includes("@mail.sfsu.edu")||document.getElementById("sfsu-email").value.includes("@sfsu.edu"))
    {
        document.getElementById("student_email_message").innerHTML = "<span style='color: green;'>This is a valid SFSU email!</span>";
        if((document.getElementById("sfsu-email").value.includes("@mail.sfsu.edu") ||document.getElementById("sfsu-email").value.includes("@sfsu.edu") )&& document.getElementById("graduation-date").value.includes("-") && document.getElementById("student_password").value.length >= 6)
        {
            document.getElementById("student_register_button").disabled = false; 
            return true;
        }

        return true;
    }
    else if(document.getElementById("sfsu-email").value.length >= 45)
    {
        document.getElementById("student_email_message").innerHTML = "<span style='color: red;'>Your input is too long, please reduce the amount </span>";
        document.getElementById("student_register_button").disabled = true; 
        return false;
    }
    else
    {
        document.getElementById("student_email_message").innerHTML = "<span style='color: red;'>This is not a valid SFSU email, Please enter a valid SFSU email </span>";
        document.getElementById("student_register_button").disabled = true; 
        return false;
    }
}


function validate_graduation_date()
{
     /* 
    Function here validates for a valid graduation date by checking if the input includes string "-", if it does it returns true, if not false.   
    Also, to check if people go out of order on the registering modal, there is also a check that checks if the other values from the fields are correct. If they are
    it will allow them to register.
    */

    if(document.getElementById("graduation-date").value.includes("-"))
    {
        document.getElementById("student_graduation_date_message").innerHTML = "<span style='color: green;'>Thank you for putting in your graduation date!</span>";
     
        if((document.getElementById("sfsu-email").value.includes("@mail.sfsu.edu") ||document.getElementById("sfsu-email").value.includes("@sfsu.edu") ) && document.getElementById("graduation-date").value.includes("-") && document.getElementById("student_password").value.length >= 6)
        {
            console.log("inside if of graduation date");
            document.getElementById("student_register_button").disabled = false; 
            return true;
        }

        return true;
    }
    else
    {
        document.getElementById("student_graduation_date_message").innerHTML = "<span style='color: red;'>Please enter a valid graduation date</span>";
        return false;
    }    
}


function validate_student_fields(){
    
    /* 
    Function here validates for all the other fields. If all the checks pass, it will allow people to register 
    Slight bug, but not too much too worry about, but if people go out of order, all the innerHTML's will write up, since we need the boolean value.
    */

    var sfsu_email_check = validate_sfsu_email();
    var graduation_date_check = validate_graduation_date();
    var student_password_check = false;

    if(document.getElementById("student_password").value.length <= 6 )
    {
        // if password is less than length 7, will pop out error messages
        // also disables the button on register, and greys it out, so people cant register
        console.log("less than 7");
        document.getElementById("student_password_message").innerHTML = "<span style='color: red;'> Password must at least be 7 characters! </span>";    
        student_password_check = false; 
    }
    else
    {
        // if password is length 7 or more, will make the disabled on the button false, and popout, this password is great!
        document.getElementById("student_password_message").innerHTML = "<span style='color: green;'>This password is great!</span>";
        student_password_check = true;
    }

    
    if(sfsu_email_check && student_password_check && graduation_date_check == true)
    {
        // if all checks pass, it will allow people to register
        document.getElementById("student_register_button").disabled = false;
        document.getElementById("student_register_button").style.backgroundColor = "rgb(131, 6, 131)"; 
    }
    else
    {
        document.getElementById("student_register_button").disabled = true; 
     
    }

}

/* STUDENT REGISTER CHECK'S END */

/* ------------------------------------------------------------------------------------------------------------------------------------------------------------------- */

/* ADMIN  REGISTER CHECK'S BEGIN */


function validate_admin_email()
{
    /* 
    Function here validates for a valid email by checking if the input includes a valid email format, if it does it returns true, if not false.   
    Also, to check if people go out of order on the registering modal, there is also a check that checks if the other values from the fields are correct. If they are
    it will allow them to register.
    */
    var regex = /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$/;
  

    if(regex.test(document.getElementById("admin-email").value))
    {
      
       document.getElementById("admin_email_message").innerHTML = "<span style='color: green;'>This email format works!</span>";

       if(document.getElementById("admin_password").value.length >= 7 && document.getElementById("admin-position").value.length >= 4 && 
       document.getElementById("organization").value.length >= 4 && regex.test(document.getElementById("admin-email").value ))
       {
           document.getElementById("admin_register_button").disabled = false;
           document.getElementById("admin_register_button").style.backgroundColor = "rgb(131, 6, 131)"; 
           return true;

       }
       else
       {
           document.getElementById("admin_register_button").disabled = true; 
           //return statement is to end function
           return false;
       }
      
     
    }
    else if(document.getElementById("admin-email").value.length >= 45)
    {
        document.getElementById("admin_email_message").innerHTML = "<span style='color: red;'>Your input is too long, please reduce the amount!</span>";
        document.getElementById("admin_register_button").disabled = true; 
        //return statement is to end function
        return false;
    }
    else
    {
      
        document.getElementById("admin_email_message").innerHTML = "<span style='color: red;'>Please enter a valid email</span>";

        if(document.getElementById("admin_password").value.length >= 7 && document.getElementById("admin-position").value.length >= 4 && 
        document.getElementById("organization").value.length >= 4 && regex.test(document.getElementById("admin-email").value ))
        {
            document.getElementById("admin_register_button").disabled = false;
            document.getElementById("admin_register_button").style.backgroundColor = "rgb(131, 6, 131)"; 
            return true;

        }
        else
        {
            document.getElementById("admin_register_button").disabled = true; 
            //return statement is to end function
            return false;
        }
        
    }
}

function validate_admin_type()
{
    
    /* 
    Function here validates for the admin type(sport, organization, department) by checking if the input is at least 5 characters, if it does it returns true, if not false.   
    Also, to check if people go out of order on the registering modal, there is also a check that checks if the other values from the fields are correct. If they are
    it will allow them to register.
    */
    console.log(document.getElementById("organization").value);
    var regex = /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$/;


    if(document.getElementById("organization").value.length <= 3)
    {
    
        document.getElementById("admin_type_message").innerHTML = "<span style='color: red;'>This field must be 4 or more characters!</span>";

        if(document.getElementById("admin_password").value.length >= 7 && document.getElementById("admin-position").value.length >= 4 && 
        document.getElementById("organization").value.length >= 4 && regex.test(document.getElementById("admin-email").value ))
        {
            document.getElementById("admin_register_button").disabled = false;
            document.getElementById("admin_register_button").style.backgroundColor = "rgb(131, 6, 131)"; 
            return true;

        }
        else
        {
            document.getElementById("admin_register_button").disabled = true; 
            //return statement is to end function
            return false;
        }
        
    }
    else if(document.getElementById("organization").value.length >= 45)
    {
        document.getElementById("admin_type_message").innerHTML = "<span style='color: red;'>Your input is too long, please reduce the amount!</span>";
        document.getElementById("admin_register_button").disabled = true; 
        //return statement is to end function
        return false;
    }
    else
    {
     
        document.getElementById("admin_type_message").innerHTML = "<span style='color: green;'>Thank you for putting in the right amount!</span>";

        if(document.getElementById("admin_password").value.length >= 7 && document.getElementById("admin-position").value.length >= 4 && 
        document.getElementById("organization").value.length >= 4 && regex.test(document.getElementById("admin-email").value ))
        {
            document.getElementById("admin_register_button").disabled = false;
            document.getElementById("admin_register_button").style.backgroundColor = "rgb(131, 6, 131)"; 
            return true;

        }
        else
        {
            document.getElementById("admin_register_button").disabled = true; 
            //return statement is to end function
            return false;
        }
         
    }

}



function validate_admin_position()
{
    
    /* 
    Function here validates for the admin type(sport, organization, department) by checking if the input is at least 5 characters, if it does it returns true, if not false.   
    Also, to check if people go out of order on the registering modal, there is also a check that checks if the other values from the fields are correct. If they are
    it will allow them to register.
    */

    var regex = /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$/;

    if(document.getElementById("admin-position").value.length <= 3)
    {
   
        document.getElementById("admin_position_message").innerHTML = "<span style='color: red;'>This field must be more 4 or more characters!</span>";

        if(document.getElementById("admin_password").value.length >= 7 && document.getElementById("admin-position").value.length >= 4 && 
        document.getElementById("organization").value.length >= 4 && regex.test(document.getElementById("admin-email").value ))
        {
            document.getElementById("admin_register_button").disabled = false;
            document.getElementById("admin_register_button").style.backgroundColor = "rgb(131, 6, 131)"; 
            return true;

        }
        else
        {
            document.getElementById("admin_register_button").disabled = true; 
            //return statement is to end function
            return false;
        }
        
   
    }
    else if(document.getElementById("admin-position").value.length >= 45)
    {
        document.getElementById("admin_position_message").innerHTML = "<span style='color: red;'>Your input is too long, please reduce the amount!</span>";
        document.getElementById("admin_register_button").disabled = true; 
        //return statement is to end function
        return false;
    }
    else
    {
    
        document.getElementById("admin_position_message").innerHTML = "<span style='color: green;'>Thank you for putting in your position!</span>";

        if(document.getElementById("admin_password").value.length >= 7 && document.getElementById("admin-position").value.length >= 4 && 
        document.getElementById("organization").value.length >= 4 && regex.test(document.getElementById("admin-email").value ))
        {
            document.getElementById("admin_register_button").disabled = false;
            document.getElementById("admin_register_button").style.backgroundColor = "rgb(131, 6, 131)"; 
            return true;

        }
        else
        {
            document.getElementById("admin_register_button").disabled = true; 
            //return statement is to end function
            return false;
        }
        
    
    }

}




function validate_admin_fields(){

    var regex = /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$/;
    if(document.getElementById("admin_password").value.length <= 6 )
    {
        // if password is less than length 7, will pop out error messages
        // also disables the button on register, and greys it out, so people cant register
    
        document.getElementById("admin_password_message").innerHTML = "<span style='color: red;'> Password must at least be 7 characters! </span>";    
       
    }
    else
    {
        // if password is length 7 or more, will make the disabled on the button false, and popout, this password is great!
        document.getElementById("admin_password_message").innerHTML = "<span style='color: green;'>This password is great!</span>";
     
    }

    if(document.getElementById("admin_password").value.length >= 7 && document.getElementById("admin-position").value.length >= 3 && 
    document.getElementById("organization").value.length >= 3 && regex.test(document.getElementById("admin-email").value ))
    {
        // if all checks pass, it will allow people to register
        document.getElementById("admin_register_button").disabled = false;
        document.getElementById("admin_register_button").style.backgroundColor = "rgb(131, 6, 131)"; 
        //return statement is to end function
        return true;
    }
    else
    {
        document.getElementById("admin_register_button").disabled = true; 
         //return statement is to end function
         return false;
     
    }

}


/* ADMIN  REGISTER CHECK'S END */

/* ------------------------------------------------------------------------------------------------------------------------------------------------------------------- */

/* SUPER USER REGISTER CHECK'S BEGIN */


function validate_super_user_email()
{
     /* 
    Function here validates for a valid email by checking if the input includes a valid email format, if it does it returns true, if not false.   
    Also, to check if people go out of order on the registering modal, there is also a check that checks if the other values from the fields are correct. If they are
    it will allow them to register.
    */
    var regex = /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$/;
    if(regex.test(document.getElementById("super-user-email").value))
    {
        document.getElementById("super_user_email_message").innerHTML = "<span style='color: green;'>This email format works!</span>";
    }
    else if(document.getElementById("super-user-email").value.length >= 45)
    {
        document.getElementById("super_user_email_message").innerHTML = "<span style='color: red;'>Your input is too long, please reduce the amount! </span>";
    }
    else
    {
        document.getElementById("super_user_email_message").innerHTML = "<span style='color: red;'>This email format is not valid </span>";
    }

    if(document.getElementById("super_user_password").value.length >= 7 && regex.test(document.getElementById("super-user-email").value))
    {
        document.getElementById("super_user_register_button").disabled = false;
        document.getElementById("super_user_register_button").style.backgroundColor = "rgb(131, 6, 131)"; 
    }
    else
    {
        document.getElementById("super_user_register_button").disabled = true; 
    }

}


function validate_super_user_fields(){


    var regex = /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$/;
    if(document.getElementById("super_user_password").value.length <= 6 )
    {
        // if password is less than length 7, will pop out error messages
        // also disables the button on register, and greys it out, so people cant register
    
        document.getElementById("super_user_password_message").innerHTML = "<span style='color: red;'> Password must at least be 7 characters! </span>";    
       
    }
    else
    {
        // if password is length 7 or more, will make the disabled on the button false, and popout, this password is great!
        document.getElementById("super_user_password_message").innerHTML = "<span style='color: green;'>This password is great!</span>";
     
    }

    if(document.getElementById("super_user_password").value.length >= 7 && regex.test(document.getElementById("super-user-email").value))
    {
        document.getElementById("super_user_register_button").disabled = false;
        document.getElementById("super_user_register_button").style.backgroundColor = "rgb(131, 6, 131)"; 
    }
    else
    {
        document.getElementById("super_user_register_button").disabled = true; 
    }   
}

/* SUPER USER REGISTER CHECK'S END */


/* ------------------------------------------------------------------------------------------------------------------------------------------------------------------- */

/* STUDENT LOGIN BEGINS */

function validate_student_email_login()
{
    /*
    Function checks if the email is a valid sfsu email. Furthermore, after it checks, if the password and email are valid,
    it allows them to login
    */
    if(document.getElementById("student_email_login").value.includes("@mail.sfsu.edu") || document.getElementById("student_email_login").value.includes("@sfsu.edu"))
    {
        document.getElementById("student_email_login_message").innerHTML = "<span style='color: green;'>This is a valid SFSU email!</span>";
    }
    else
    {
        document.getElementById("student_email_login_message").innerHTML = "<span style='color: red;'>This is not a valid SFSU email!</span>";
    }

    if(document.getElementById("student_password_login").value.length >= 7 && (document.getElementById("student_email_login").value.includes("@mail.sfsu.edu") || document.getElementById("student_email_login").value.includes("@sfsu.edu")))
    {
        document.getElementById("student_login_button").disabled = false;
        document.getElementById("student_login_button").style.backgroundColor = "rgb(131, 6, 131)"; 
    }
    else
    {
        document.getElementById("student_login_button").disabled = true; 
    }   

}


function validate_student_password_login()
{
    /*
    Function checks if the password is the right length. Furthermore, after it checks, if the password and email are valid,
    it allows them to register
    */
    if(document.getElementById("student_password_login").value.length <= 6 )
    {
        document.getElementById("student_password_login_message").innerHTML = "<span style='color: red;'>Password length must be at least 7 characters!</span>";
      
    }
    else
    {
        document.getElementById("student_password_login_message").innerHTML = "<span style='color: green;'>This is a valid password length!</span>";
    }

    if(document.getElementById("student_password_login").value.length >= 7 && (document.getElementById("student_email_login").value.includes("@mail.sfsu.edu") || document.getElementById("student_email_login").value.includes("@sfsu.edu")))
    {
        document.getElementById("student_login_button").disabled = false;
        document.getElementById("student_login_button").style.backgroundColor = "rgb(131, 6, 131)"; 
    }
    else
    {
        document.getElementById("student_login_button").disabled = true; 
    }   
}
/* STUDENT LOGIN ENDS */

/* ------------------------------------------------------------------------------------------------------------------------------------------------------------------- */



/* ADMIN LOGIN BEGINS */

function validate_admin_email_login()
{
    /*
    Function checks if the email is a valid sfsu email. Furthermore, after it checks, if the password and email are valid,
    it allows them to login
    */
    var regex = /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$/;
    if(regex.test(document.getElementById("admin_email_login").value))
    {
        document.getElementById("admin_email_login_message").innerHTML = "<span style='color: green;'>This is a valid email!</span>";
    }
    else
    {
        document.getElementById("admin_email_login_message").innerHTML = "<span style='color: red;'>This is not a valid email!</span>";
    }

    if(document.getElementById("admin_password_login").value.length >= 7 && regex.test(document.getElementById("admin_email_login").value))
    {
        document.getElementById("admin_login_button").disabled = false;
        document.getElementById("admin_login_button").style.backgroundColor = "rgb(131, 6, 131)"; 
    }
    else
    {
        document.getElementById("admin_login_button").disabled = true; 
    }   

}


function validate_admin_password_login()
{
    /*
    Function checks if the password is the right length. Furthermore, after it checks, if the password and email are valid,
    it allows them to login
    */
    var regex = /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$/;

    if(document.getElementById("admin_password_login").value.length <= 6 )
    {
        document.getElementById("admin_password_login_message").innerHTML = "<span style='color: red;'>Password length must be at least 7 characters!</span>";
    }
    else
    {
        document.getElementById("admin_password_login_message").innerHTML = "<span style='color: green;'>This is a valid password length!</span>";
    }

    if(document.getElementById("admin_password_login").value.length >= 7 && regex.test(document.getElementById("admin_email_login").value))
    {
        document.getElementById("admin_login_button").disabled = false;
        document.getElementById("admin_login_button").style.backgroundColor = "rgb(131, 6, 131)"; 
    }
    else
    {
        document.getElementById("admin_login_button").disabled = true; 
    }   
}
/* ADMIN LOGIN ENDS */

/* ------------------------------------------------------------------------------------------------------------------------------------------------------------------- */


/* SUPER USER LOGIN BEGINS */

function validate_super_user_email_login()
{
    /*
    Function checks if the email is a valid sfsu email. Furthermore, after it checks, if the password and email are valid,
    it allows them to login
    */
    var regex = /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$/;
    if(regex.test(document.getElementById("super_user_email_login").value))
    {
        document.getElementById("super_user_email_login_message").innerHTML = "<span style='color: green;'>This is a valid email!</span>";
    }
    else
    {
        document.getElementById("super_user_email_login_message").innerHTML = "<span style='color: red;'>This is not a valid email!</span>";
    }

    if(document.getElementById("super_user_password_login").value.length >= 7 && regex.test(document.getElementById("super_user_email_login").value))
    {
        document.getElementById("super_user_login_button").disabled = false;
        document.getElementById("super_user_login_button").style.backgroundColor = "rgb(131, 6, 131)"; 
    }
    else
    {
        document.getElementById("super_user_login_button").disabled = true; 
    }   

}


function validate_super_user_password_login()
{
    /*
    Function checks if the password is the right length. Furthermore, after it checks, if the password and email are valid,
    it allows them to login
    */
    var regex = /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$/;

    if(document.getElementById("super_user_password_login").value.length <= 6 )
    {
        document.getElementById("super_user_password_login_message").innerHTML = "<span style='color: red;'>Password length must be at least 7 characters!</span>";
    }
    else
    {
        document.getElementById("super_user_password_login_message").innerHTML = "<span style='color: green;'>This is a valid password length!</span>";
    }

    if(document.getElementById("super_user_password_login").value.length >= 7 && regex.test(document.getElementById("super_user_email_login").value))
    {
        document.getElementById("super_user_login_button").disabled = false;
        document.getElementById("super_user_login_button").style.backgroundColor = "rgb(131, 6, 131)"; 
    }
    else
    {
        document.getElementById("super_user_login_button").disabled = true; 
    }   
}
/* SUPER USER LOGIN ENDS */







// Jquery Dependency

$("input[data-type='currency']").on({
    keyup: function() {
      formatCurrency($(this));
    },
    blur: function() { 
      formatCurrency($(this), "blur");
    }
});


function formatNumber(n) {
  // format number 1000000 to 1,234,567
  return n.replace(/\D/g, "").replace(/\B(?=(\d{3})+(?!\d))/g, ",")
}


function formatCurrency(input, blur) {
  // appends $ to value, validates decimal side
  // and puts cursor back in right position.
  
  // get input value
  var input_val = input.val();
  
  // don't validate empty input
  if (input_val === "") { return; }
  
  // original length
  var original_len = input_val.length;

  // initial caret position 
  var caret_pos = input.prop("selectionStart");
    
  // check for decimal
  if (input_val.indexOf(".") >= 0) {

    // get position of first decimal
    // this prevents multiple decimals from
    // being entered
    var decimal_pos = input_val.indexOf(".");

    // split number by decimal point
    var left_side = input_val.substring(0, decimal_pos);
    var right_side = input_val.substring(decimal_pos);

    // add commas to left side of number
    left_side = formatNumber(left_side);

    // validate right side
    right_side = formatNumber(right_side);
    
    // On blur make sure 2 numbers after decimal
    if (blur === "blur") {
      right_side += "00";
    }
    
    // Limit decimal to only 2 digits
    right_side = right_side.substring(0, 2);

    // join number by .
    input_val = "$" + left_side + "." + right_side;

  } else {
    // no decimal entered
    // add commas to number
    // remove all non-digits
    input_val = formatNumber(input_val);
    input_val = "$" + input_val;
    
    // final formatting
    if (blur === "blur") {
      input_val += ".00";
    }
  }
  
  // send updated string to input
  input.val(input_val);

  // put caret back in the right position
  var updated_len = input_val.length;
  caret_pos = updated_len - original_len + caret_pos;
  input[0].setSelectionRange(caret_pos, caret_pos);
}