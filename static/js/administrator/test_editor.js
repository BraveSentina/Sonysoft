let add_option_btn = $('#add-option-btn');
let options_container = $('.options-container')[0];
let option_delete = $('.option-delete');

$(add_option_btn).click(function (e) { 
    let option_container = document.createElement('div');
    option_container.className = 'option-container';
    
    option_container.innerHTML = `
    <input class="option" type="radio" name="option" onchange="updateCorrectAnswerInput(event)">
    <input class="option-text" type="text" name="option_text" id="" placeholder="Enter your option">
    <button class="bin-container" onclick="binClickHandler(event)" type="button">
        <i class="fas fa-trash bin"></i>
    </button>
    `
    options_container.appendChild(option_container);

    for(var i=0;i<option_container.length;i++){
        option_container[i].index = i;
    }
});

function binClickHandler(e){
    if(e.target.parentNode.parentNode.index == 0){
        // e.preventDefault();
        return;
    }
    console.log('index is '+e.target.parentNode.parentNode.index);
    e.target.parentNode.parentNode.remove();
    console.log("Called");
}

function updateCorrectAnswerInput(e){
    let correct_option = document.getElementById('correct_option');
    let options_container = $('.options-container');
    let option = $('.option');

    for(let i=0;i<option.length;i++){
        option[i].index = i;
    }

   index = e.target.index;
   correct_option.value = index;
}

document.getElementById('marks').addEventListener('keypress',validateNumber)


function validateNumber(evt) {
    console.log('called');
    var theEvent = evt || window.event;
    // Handle paste
    if (theEvent.type === 'paste') {
        key = evt.clipboardData.getData('text/plain');
    } else {
    // Handle key press
        var key = theEvent.keyCode || theEvent.which;
        key = String.fromCharCode(key);
    }
    var regex = /[0-9]|\./;
    if( !regex.test(key) ) {
      theEvent.returnValue = false;
      if(theEvent.preventDefault) theEvent.preventDefault();
    }
  }

option_delete[0].value = 0;
