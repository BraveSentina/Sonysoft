let username = document.getElementById('username');
let firstname = document.getElementById('fname')
let lastname = document.getElementById('lname')
let password1 = document.getElementById('password1');
let password2 = document.getElementById('password2');
let checkbox = document.getElementById('checkbox');
let signup_btn = document.getElementById('signup-btn');
let validate_lists = document.getElementsByClassName("validate-lists")[0];

let upper_flag = true;
let lower_flag = true;
let character_flag = true;
let number_flag = true;
let length_flag = true;

let upper_error = document.getElementsByClassName("error")[0];
let lower_error = document.getElementsByClassName("error")[1];
let character_error = document.getElementsByClassName("error")[2];
let number_error = document.getElementsByClassName("error")[3];
let length_error = document.getElementsByClassName("error")[4];

function upperCaseValidation(){
    let string = password1.value;
    let rule = /^[A-Z]+$/

    for(i=0;i<string.length;i++){
        if(string.charAt(i).match(rule)){
           upper_flag = false
           upper_error.style.color = 'green'
           return true;
        }
     }
    upper_flag = true
    upper_error.style.color = 'red'
    return false;
}

function lowerCaseValidation(){
    let string = password1.value;
    let rule = /^[a-z]+$/

    for(i=0;i<string.length;i++){
        if(string.charAt(i).match(rule)){
           lower_flag = false
           lower_error.style.color = 'green'
           return true;
        }
     }
    lower_flag = true
    lower_error.style.color = 'red'
    return false;
}

function characterValidation(){
    let string = password1.value;
    let rule = /^[^\w\s]+$/

    for(i=0;i<string.length;i++){
       if(string.charAt(i).match(rule)){
          character_flag = false
          character_error.style.color = 'green'
        //   character_error.style.display = 'block'
          return true;
       }
    }
    character_flag = true
    character_error.style.color = 'red'
    // check5.style.display = 'none'
    return false;
 }

function numberValidation(){
   let string = password1.value;
   let rule = /^[0-9]+$/

   for(i=0;i<string.length;i++){
      if(string.charAt(i).match(rule)){
         number_flag = false;
         number_error.style.color = 'green'
         return true;
      }
   }
   number_flag = true
   number_error.style.color = 'red'
   // check5.style.display = 'none'
   return false;
}

function lengthValidation(){
   let string = password1.value;

   if(string.length >=6 ){
      length_flag = false
      length_error.style.color = 'green'
      return true;
   }

   length_flag = true
   length_error.style.color = 'red'
   return false;

}

$(password1).keyup(function (e) { 
   upperCaseValidation();
   lowerCaseValidation();
   characterValidation();
   numberValidation();
   lengthValidation();

   if((upper_flag == false) && (lower_flag == false) && (number_flag == false) && (character_flag == false) && (length_flag == false)){
      validate_lists.style.display = 'none';
   }
   else{
      validate_lists.style.display = 'block';
   }
});

$(checkbox).change(function (e) { 
   if(checkbox.checked == true){
      signup_btn.style.display = 'block';
   }
   else{
      signup_btn.style.display = 'none';
   }
   
});

function validatePassword(){
   if(password1.value != password2.value){
      password2.setCustomValidity("Passwords dont match")
      return false;
   }
   else{
      password2.setCustomValidity('')
      return true;
   }
}

function validateUsername(){
   let string = username.value;
   let count = 0
   let c_flag = false;
   let rule = /^[^a-zA-Z0-9]+$/
   for(let i=0;i<string.length-1;i++){
      if(string.charAt(i) == string.charAt(i+1)){
         count++;
      }
   }

   if(string.length == 1){
      username.setCustomValidity("Enter more characters")
      return;
   }else{
      username.setCustomValidity('')
   }

   // Code to detect frequent letter
   if(count==string.length-1 && string.length>1){
      username.setCustomValidity("Too frequent letters used, give unique name")
      return;
   }else{
      username.setCustomValidity('')
   }

   // Code to detect all special symbols in username
   let isTrue = rule.test(string);
   if(isTrue){
      username.setCustomValidity('Include different key combinations like letters, numbers')
      return;
   }
   else{
      username.setCustomValidity('');
   }

   rule = /^[^0-9]+$/

   if(!isNaN(string) && string.length > 1){
      username.setCustomValidity('All are numbers')
      return;
   }else{
      username.setCustomValidity('')
   }

   // Atleast one text 
   rule = /^[a-zA-Z]+$/

   for(i=0;i<string.length;i++){
      if((string.charAt(i).match(rule)) && string.length > 1){
         c_flag = true;
      }
   }

   if(c_flag){
      username.setCustomValidity('')
   }else{
      username.setCustomValidity("Include atleast one alphabet");
      return;
   }
}

function validateFirstname(event){
   // alert(event.keyCode);
   let ascii = event.keyCode;
   let string = firstname.value;
   let count = 0
   let c_flag = false;
   let rule = /^[A-Za-z]+$/
   for(let i=0;i<string.length-1;i++){
      if(string.charAt(i) == string.charAt(i+1)){
         count++;
      }
   }

   if((ascii >= 65 && ascii <= 90) || ascii==8 || ascii == 13){
      firstname.setCustomValidity('')
   }
   else{
      event.preventDefault();
   }

   if(string.length == 1){
      firstname.setCustomValidity("Enter more characters")
      return;
   }else{
      firstname.setCustomValidity('')
   }

   // Code to detect frequent letter
   if(count==string.length-1 && string.length>1){
      firstname.setCustomValidity("Too frequent letters used, give unique name")
      return;
   }else{
      firstname.setCustomValidity('')
   }
}
function validateLastname(event){
   // alert(event.keyCode);
   let ascii = event.keyCode;
   let string = lastname.value;
   let count = 0
   let c_flag = false;
   let rule = /^[A-Za-z]+$/
   for(let i=0;i<string.length-1;i++){
      if(string.charAt(i) == string.charAt(i+1)){
         count++;
      }
   }

   if((ascii >= 65 && ascii <= 90) || ascii==8 || ascii == 13){
      lastname.setCustomValidity('')
   }
   else{
      event.preventDefault();
   }

   // if(string.length == 1){
   //    lastname.setCustomValidity("Enter more characters")
   //    return;
   // }else{
   //    lastname.setCustomValidity('')
   // }

   // Code to detect frequent letter
   if(count==string.length-1 && string.length>1){
      lastname.setCustomValidity("Too frequent letters used, give unique name")
      return;
   }else{
      lastname.setCustomValidity('')
   }
}

signup_btn.style.display = 'none';
password1.onchange = validatePassword
password2.onkeyup = validatePassword
username.onchange = validateUsername
username.onkeyup = validateUsername

$(username).on('input', function () {
   validateUsername();
});

document.getElementById('form').onsubmit = () =>{
   validatePassword();
   validateUsername();

  if(upperCaseValidation() == false || lowerCaseValidation() == false || characterValidation() == false || lengthValidation() == false || numberValidation() == false){
   password1.style.background = "#f7d7d7"; 
   password2.style.background = "#f7d7d7";   
  
   return false;
  }
}