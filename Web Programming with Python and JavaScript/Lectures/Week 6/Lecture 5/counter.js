if (!localStorage.getItem('counter')){
    localStorage.setItem('counter', 0);
}
function count(){
    let counter = localStorage.getItem('counter') 
    counter++;
    document.querySelector("h1").innerHTML = counter;
    localStorage.setItem('counter', counter);
}
document.addEventListener('DOMContentLoaded', function(){  //When the whole document done loading (the whole html script)then run the fucntion() 
    document.querySelector("h1").innerHTML = localStorage.getItem("counter");
    document.querySelector("button").onclick = count;

})