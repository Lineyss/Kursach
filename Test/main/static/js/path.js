import {openFileFolder} from './main.js'

const buttonSend = document.querySelector("#path-form > button");
const buttonBack = document.querySelector(".back-button");
const input = document.getElementById("path");

buttonSend.addEventListener("click", ()=>{
    openFileFolder();
});

if(input.value == '/')
{
    buttonBack.style.display = 'none';
}

buttonBack.addEventListener("click", ()=>{
    let value = input.value.split('/');
    value.pop()
    if (value.length == 1)
    {
        value = '/';
    }
    else
    {
        value = value.join('/');
    }
    input.value = value;
    openFileFolder();
});

input.addEventListener("keydown", (e) => {
    if(e.key === 'Enter')
    {
        openFileFolder();
    }
});