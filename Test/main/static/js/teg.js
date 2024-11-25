import { ContextWorkerBase } from './context_menu.js'
import { sendRequest } from './send_http.js';

const content_container = document.querySelector('.content-container');
const teg_update_form = document.getElementById('change-teg-form');
const contextMenu = document.getElementById('context_menu_teg');
const teg_cards = document.querySelectorAll('.tag-card');
const input_title = document.getElementById('id_Title');
const input_color = document.getElementById('id_Color');
const parser = new DOMParser();

let context = new ContextWorkerBase(contextMenu, 'context_menu_button')

let old_action = null;
let selected_item = null;

function rgbToHex(rgb) {
    const rgbValues = rgb.match(/\d+/g);

    const hex = rgbValues.map(value => {
        const hexValue = parseInt(value).toString(16);
        return hexValue.length === 1 ? '0' + hexValue : hexValue;
    }).join('');

    return `#${hex}`;
}

const convertInnerHTMLToDOMElement = (innerHtml) => {
    const doc = parser.parseFromString(innerHtml, 'text/html');
    return doc.body.firstChild;
};

const createTeg = (id, title, color) =>
{
    let html = `
        <div class="tag-card" id="${id}}">
            <div class="bookmark" style="background: ${color};"></div>
            <div class="tag-title" title="${title}">${title}</div>
        </div>
    `;

    let DOM = convertInnerHTMLToDOMElement(html);
    context.start(DOM);
    setEvent(DOM);

    return DOM;
}

const setEvent = (element) => {
    element.addEventListener('click', function (){
        let action = teg_update_form.getAttribute('action')
        old_action = action;
        action += this.getAttribute('id');
    
        teg_update_form.setAttribute('action', action);
        input_title.value = this.querySelector('.tag-title').getAttribute('title');
        let bookmarkStyle = this.querySelector('.bookmark').style.backgroundColor;
    
        const hexColor = rgbToHex(bookmarkStyle);
        input_color.value = hexColor;
        selected_item = this;
    });
}

teg_cards.forEach(element => {
    context.start(element);
    setEvent(element);
});

context.get_button('delete').addEventListener('submit', function (e) {
    e.preventDefault();
    
    let item = context.current_element.closest(".tag-card");
    let action = this.getAttribute('action') + context.current_element.closest(".tag-card").getAttribute('id');
    let method = this.getAttribute('method');

    sendRequest(action, new FormData(this), method, false, function ()
    {
        console.log(this.status);
        if (this.status == 200)
        {
            item.remove();
        }
        else
        {
            alert('Не удалось удалить тег =(')
        }
    });
});

teg_update_form.addEventListener('submit', function (e) {
    e.preventDefault();
    let form = this;
    sendRequest(this.getAttribute('action'), new FormData(this), this.getAttribute('method'), false, function () {
        console.log(this.status);
        if (this.status == 200)
        {
            form.setAttribute('action', old_action);
            form.reset();
            let body = JSON.parse(this.response);
            console.log(selected_item);
            selected_item.querySelector('.bookmark').style.backgroundColor = body.color;
            let title = selected_item.querySelector('.tag-title');
            title.setAttribute('title', body.title);
            title.innerHTML = body.title;
        }
        else
        {
            alert('Не удалось обновить тег =(')
        }
    });
});