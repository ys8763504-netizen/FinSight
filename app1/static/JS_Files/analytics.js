
function sendMessage(){

let input = document.getElementById("userInput")
let message = input.value

if(message.trim() === ""){
return
}

let chatBody = document.getElementById("chatBody")

chatBody.innerHTML += `<div class="user-msg">${message}</div>`

fetch(`/finsight_agent/?message=${message}`)
.then(res=>res.json())
.then(data=>{

chatBody.innerHTML += `<div class="bot-msg">${data.reply}</div>`

chatBody.scrollTop = chatBody.scrollHeight

})

input.value=""

}
function ask(question){

document.getElementById("userInput").value = question
sendMessage()

}