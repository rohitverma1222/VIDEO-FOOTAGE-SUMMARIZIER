let sidebar = document.querySelector(".sidebar");
let sidebarBtn = document.querySelector(".sidebarBtn");
sidebarBtn.onclick = function() {
  sidebar.classList.toggle("active");
  if(sidebar.classList.contains("active")){
  sidebarBtn.classList.replace("bx-menu" ,"bx-menu-alt-right");
}else
  sidebarBtn.classList.replace("bx-menu-alt-right", "bx-menu");
}

// popUp

let closebtn=document.querySelector(".close")
let modelPopup=document.querySelector(".log_out")
let popUp=document.querySelector(".pop-up")
let yesBtn=document.querySelector(".yes")
closebtn.addEventListener("click",()=>{
  popUp.style.display="none";
})
yesBtn.addEventListener("click",()=>{
  popUp.style.display="none";
})

modelPopup.addEventListener("click",()=>{
  popUp.style.display="";
})


