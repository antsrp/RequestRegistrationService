function getSelector(){
	return document.getElementById('ending')
}

function showError(){
	selector = getSelector()
	console.log(selector)
	selector.innerText = "Произошла ошибка. Попробуйте оформить обращение позднее."
}

function hideError(){
	selector = getSelector()
	selector.innerText = ""
}

function send(form){
event.preventDefault();
hideError();
const data = new FormData(form) 

var object = Object.fromEntries(data.entries());
var json = JSON.stringify(object);
console.log(json)

fetch("/send", {
    credentials: "same-origin",
    mode: "same-origin",
    method: "post",
    headers: { "Content-Type": "application/json" },
    body: json
})
	.then(resp => {
		if (resp.status === 200) window.location.href = '/success';
		else showError();
	})
}