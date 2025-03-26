const usernameField = document.querySelector("#usernameField");
const feedBackArea = document.querySelector(".invalid_feedback")
const emailField = document.querySelector("#emailField")
const emailfeedBackArea = document.querySelector(".emailfeedBackArea")
const passwordField = document.querySelector("#passwordField")
const usernameSuccessOutput = document.querySelector(".usernameSuccessOutput")
const emailSuccessOutput = document.querySelector(".emailSuccessOutput")
const showPasswordToggle = document.querySelector(".showPasswordToggle")

const handleToggleInput=(e)=>{
  if (showPasswordToggle.textContent==="SHOW") {
    showPasswordToggle.textContent = "HIDE";
    passwordField.setAttribute("type","text");
  } else {
    showPasswordToggle.textContent = "SHOW";
    passwordField.setAttribute("type","password");
  }
};


showPasswordToggle.addEventListener('click',handleToggleInput);



emailField.addEventListener('keyup',(e)=>{
  const emailval = e.target.value;


  emailSuccessOutput.style.display='block'
  emailSuccessOutput.textContent=`Checking ${emailval}`
  
  emailField.classList.remove("is-invalid");
  emailfeedBackArea.style.display="none";
  if(emailval.length > 0){
    fetch("/authentication/validate_email",{
      body:JSON.stringify({email:emailval}),
      method:"POST",
    })
  .then((res)=>res.json())
  .then((data)=>{
    console.log('data',data);
    emailSuccessOutput.style.display='none'
    if(data.email_error){
      emailField.classList.add('is-invalid');
      emailfeedBackArea.style.display="block";
      emailfeedBackArea.innerHTML=`<p>${data.email_error}</p>`
    }
  });
  }
});

usernameField.addEventListener('keyup',(e)=>{
  const usernameVal = e.target.value;

  usernameSuccessOutput.style.display='block'

  usernameSuccessOutput.textContent=`Checking ${usernameVal}`

  usernameField.classList.remove("is-invalid");
  feedBackArea.style.display="none";

  if(usernameVal.length > 0) {
    fetch("/authentication/validate_username",{
      body:JSON.stringify({username:usernameVal}),
      method:"POST",
    })
    .then((res)=>res.json())
    .then((data)=>{
      console.log('data',data)
      usernameSuccessOutput.style.display='none'
      if (data.username_error){
        usernameField.classList.add("is-invalid");
        feedBackArea.style.display="block";
        feedBackArea.innerHTML = `<p>${data.username_error}</p>`
      }
    });
  } 
});


