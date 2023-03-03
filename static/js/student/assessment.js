console.log("Script is active");
let elem = document.documentElement;
let full_screen_btn = $('.full-screen-btn')[0];

function openfullscreen(){
    if(elem.requestFullscreen){
        elem.requestFullscreen();
    }
    else if(elem.mozRequestFullScreen){
        elem.mozRequestFullScreen();
    }
    else if(elem.webkitRequestFullscreen){
        elem.webkitRequestFullscreen();
    }
    else if(elem.msRequestFullscreen){
        elem.msRequestFullscreen();
    }
}

function exitFullScreen(){
    if(document.exitFullscreen){
        elem.exitFullscreen();
    }
    else if(document.mozCancelFullScreen){
        document.mozCancelFullScreen();
    }
    else if(document.webkitExitFullscreen){
        elem.webkitExitFullscreen();
    }
    else if(elem.msRequestFullscreen){
        elem.msRequestFullscreen();
    }
    //window.close();
}

$(full_screen_btn).click(function (e) { 
    openfullscreen();

});



