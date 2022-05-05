const btn_url = document.querySelector(".btn_url")
const btn_file = document.querySelector(".btn_file")
const file = document.querySelector(".file")
const url = document.querySelector(".url")

btn_url.addEventListener("click",()=>{
	url.style.display = 'block'
	file.style.display = 'none'
	url.required=true
	file.required=false
		console.log("url",url.required)
	console.log("file",file.required)
})
btn_file.addEventListener("click",()=>{
	url.required=false
	file.required=true
	console.log("url",url.required)
	console.log("file",file.required)
	url.style.display = 'none'
	file.style.display = 'block'
})