let loading_font = $('.loading-font')[0];
let proceed_link = $('.proceed-link')[0];
let timer = 3000;
let elem = document.documentElement;

function showProceedLink(){
    loading_font.style.display = 'none';
    proceed_link.style.display = 'block';
}

setTimeout(showProceedLink,timer);

console.log("Hi");
console.log('hrello'+navigator.platform);