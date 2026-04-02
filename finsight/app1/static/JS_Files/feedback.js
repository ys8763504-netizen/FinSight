function validateForm(){
    let name = document.getElementById("name").value.trim()
    let email = document.getElementById("email").value.trim()
    let type = document.getElementById("type").value
    let message = document.getElementById("message").value.trim()
    let error = document.getElementById("error")

    if(name === "" || email === "" || type === "" || message === ""){
        error.innerText = "All fields are required"
        return false
    }

    if(!email.includes("@")){
        error.innerText = "Enter valid email"
        return false
    }

    if(message.length < 5){
        error.innerText = "Message too short"
        return false
    }

    let rating = document.getElementById("rating").value

    if(rating == 0){
        document.getElementById("rating_error").innerText = "Please select rating"
        return false
    }

    return true
}
let stars = document.querySelectorAll(".star")
let ratingInput = document.getElementById("rating")

stars.forEach(star => {
    star.addEventListener("click", function(){

        let value = this.getAttribute("data-value")
        ratingInput.value = value

        // reset all
        stars.forEach(s => s.classList.remove("active"))

        // highlight selected
        for(let i=0; i<value; i++){
            stars[i].classList.add("active")
        }
    })
})
