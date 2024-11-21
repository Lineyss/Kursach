import { MenuItems, MenuParentItem } from './context_menu.js'
import { DragAndDrop } from './drag_and_drop.js'
import { sendRequest } from './send_http.js'

const createFile = (IDFileFolder, Title) => {
    return `
        <div class="item">
            <div class="image-container">
                <img src="/static/images/file-icon.svg">
            </div>
            <div class="title-container">
                <p style="display: none;" id="id">
                    ${
                        IDFileFolder
                    }
                </p>
                <input type="text" maxlength="150" value=${Title} />
            </div>
        </div>
    `
}

const createFolder = (IDFileFolder, Title) => {
    return `
        <div class="item">
            <div class="image-container">
                <img src="/static/images/folder-icon.svg">
            </div>
            <div class="title-container">
                <p style="display: none;" id="id">
                    ${
                        IDFileFolder
                    }
                </p>
                <input type="text" maxlength="150" value=${Title} />
            </div>
        </div>
    `
}

const context_menu_parent = document.getElementById("context_menu_item_parent");
const context_menu_item = document.getElementById("context_menu_item");
const dropZone = document.getElementById('drop-zone');
const fileInput = document.getElementById('id_File');
const formFile = document.getElementById('form-file');
const items = document.querySelector(".items");

const menuParent = new MenuParentItem(context_menu_parent);
const menuItem = new MenuItems(context_menu_item);
new DragAndDrop(dropZone, fileInput).start();
const parser = new DOMParser();

document.querySelectorAll(".item").forEach(element => {
    menuItem.start(element);
});

menuParent.start(items);

menuParent.get_button("create_folder").addEventListener("click", (e)=>{
    let folder = createFolder(1, "asd");
    folder = parser.parseFromString(folder, "text/html").body.firstElementChild
    items.appendChild(folder); 
    menuItem.start(folder);
});

// menuParent.get_button("change").addEventListener("click", ()=>{
//     if(menuItem.current_element)
//     {
//         console.log(menuItem.current_element);
//     }
// });

fileInput.addEventListener('change', () => {
    let url = formFile.getAttribute('action')
    let method = formFile.getAttribute('method')
    sendRequest(url, new FormData(formFile), method, true, function() {
        let data = this.response;

        if(this.status != 200)
        {
            alert(data);
        }
        else
        {
            let idFileFolder = data.split(':');
            let text = createFile(idFileFolder[0], idFileFolder[1]);
            items.innerHTML = items.innerHTML + text;
        }
    })
});