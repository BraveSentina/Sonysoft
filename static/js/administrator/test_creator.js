function validateInteger(event){
    let key = event.key;

    if(key == '-'){
        event.preventDefault();
    }
     let string = ""+event.target.value;
    //  console.log(string.length);

     if(string.length > 2){
        event.preventDefault();
     }
}

function validatePercentage(event){
    let key = event.key;

    if(key == '-'){
        event.preventDefault();
    }
     let string = ""+event.target.value;
    //  console.log(string.length);

     if(string.length > 2 || parseInt(string)>99){
        event.preventDefault();
     }
    //  console.log(string);
}

