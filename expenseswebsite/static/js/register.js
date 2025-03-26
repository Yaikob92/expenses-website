const usernameField = document.querySelector("#usernameField")
const feedBackArea = document.querySelector(".invalid_feedback")
const EamilfeedBackArea = document.querySelector(".emailfeedBackArea")
const passwordField = document.querySelector("#passwordField")
const emailField = document.querySelector("#emailField")
const usernameSuccessOutput = document.querySelector(".usernameSuccessOutput")
const emailSuccessOutput = document.querySelector(".emailSuccessOutput")
const showPasswordToggle = document.querySelector(".showPasswordToggle")
const submitBtn = document.querySelector(".submit-btn")

const handleToggleInput = (e) => {
  if (showPasswordToggle.textContent === "SHOW"){
    showPasswordToggle.textContent="HIDE"
    passwordField.setAttribute("type","text")
  }else{
    showPasswordToggle.textContent="SHOW"
    passwordField.setAttribute("type","password")
  }
};

showPasswordToggle.addEventListener("click",handleToggleInput)

emailField.addEventListener("keyup",(e)=>{
  const emailVal = e.target.value;
  emailSuccessOutput.style.display="block";
  emailSuccessOutput.textContent = `Checking ${emailVal}`
  emailField.classList.remove("is-invalid");
  EamilfeedBackArea.style.display="none";
  if (emailVal.length > 0){
    fetch("/authentication/validate-email",{
      body:JSON.stringify({email:emailVal}),
      method:"POST"
    })
    .then((res)=>res.json())
    .then((data)=>{
      console.log("data",data);
      emailSuccessOutput.style.display="none";
      if (data.email_error){
        submitBtn.disabled = true;
        emailField.classList.add("is-invalid")
        EamilfeedBackArea.style.display="block";
        EamilfeedBackArea.innerHTML = `<p>${data.email_error}</p>`
      }else{
        submitBtn.removeAttribute("disabled")
      }
    });
  }
});

usernameField.addEventListener("keyup",(e)=>{
  const usernameVal = e.target.value;
  usernameSuccessOutput.style.display="block";
  usernameSuccessOutput.textContent = `Checking ${usernameVal}`
  usernameField.classList.remove("is-invalid");
  feedBackArea.style.display="none";
  
// an API call using fetch
  if (usernameVal.length > 0){
    fetch("/authentication/validate-username",{
      body:JSON.stringify({username:usernameVal}),
      method:"POST",
    })
      .then((res) => res.json())
      .then((data) => {
        console.log("data",data);
        usernameSuccessOutput.style.display="none";
        if(data.username_error){
          usernameField.classList.add("is-invalid");
          feedBackArea.style.display="block"
          feedBackArea.innerHTML = `<p>${data.username_error}</p>`
          submitBtn.disabled = true;
        }else{
          submitBtn.removeAttribute("disabled");
        }
      });
  }
});
