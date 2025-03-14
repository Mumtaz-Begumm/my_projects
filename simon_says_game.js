let gameseq=[];
let userseq=[];
let level=0;
let started=false;
let colors=["yellow","red","purple","green"];

document.addEventListener("keypress",function(){
    if(started==false){
        console.log("game started");
        started=true;
        levelup();
    }    
});

let h2=document.querySelector("h2");
function levelup(){
    userseq=[];
    level++;
    h2.innerText=`level: ${level}`;
    randIdx=Math.floor(Math.random()*3);
    randColor=colors[randIdx];
    gameseq.push(randColor);
    randBtn=document.querySelector(`.${randColor}`)
    gameflash(randBtn);
}
function gameflash(btn){
    btn.classList.add("flash");
    setTimeout(function(){
        btn.classList.remove("flash");
    },200);
}
function userflash(btn){
    btn.classList.add("userflash");
    setTimeout(function(){
        btn.classList.remove("userflash");
    },200);
};

function checkAns(idx){
    if(gameseq[idx]===userseq[idx]){
        if(userseq.length==gameseq.length){
            setTimeout(levelup,1000);
        } 
    }
    else{
        h2.innerHTML=`game over! your score was <b>${level}</b> press any key to start again`;
        let body= document.querySelector("body");
        body.style.backgroundColor="red";
        setTimeout(function(){
            body.style.backgroundColor="white";
        },200);
        reset();
    }
}

function btnpress(){
    let btn=this;
    userflash(btn);
    let userColor=btn.getAttribute("id");
    userseq.push(userColor);
    checkAns(userseq.length-1);
}
let allbtns=document.querySelectorAll(".btn");
for(btn of allbtns){
    btn.addEventListener("click",btnpress);
};

function reset(){
    started=false;
    gameseq=[];
    userseq=[];
    level=0;
}