import { MenuItems, MenuParentItem } from './context_menu.js'
import { DragAndDrop } from './drag_and_drop.js'
import { sendRequest } from './send_http.js'

const context_menu_parent = document.getElementById("context_menu_item_parent");
const context_menu_item = document.getElementById("context_menu_item");
const dropZone = document.getElementById('drop-zone');
const fileInput = document.getElementById('id_File');
const formFile = document.getElementById('form-file');
const items = document.querySelector(".items");
const menuItems = new MenuItems(context_menu_item);
const menuParent = new MenuParentItem(context_menu_parent);

menuParent.start(items);

new DragAndDrop(dropZone, fileInput).start();

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
                <input type="text" maxlength="150" value="${Title}" />
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
                <input type="text" maxlength="100" value="${Title}" />
            </div>
        </div>
    `
}

const setMenuItem = (items) => {
    if (items) {
        if (Array.isArray(items) || items instanceof NodeList) {
            items.forEach(element => {
                console.log(element);
                menuItems.start(element);
            });
        } else {
            menuItems.start(items);
        }
    }
}
const WorkChangeName = (item, finalFunction) => {
    let input = item.querySelector("#fileTitle");
    input.readOnly=false;
    input.select();
    input.focus();

    input.addEventListener("keydown", EnterDown);
    input.addEventListener("blur", Blur);

    function EnterDown(event)
    {
        if (event.keyCode === 13) {
            input.blur();
        }
    }

    function Blur()
    {
        console.log(this.value);

        if(finalFunction)
        {
            finalFunction();
        }
        
        this.removeEventListener("keydown", EnterDown);
        this.removeEventListener("blur", Blur);
    }
}

setMenuItem(document.querySelectorAll(".item"));

menuItems.get_button("change").addEventListener("click", (e)=>{
    let item = menuItems.current_element.closest(".item");
    WorkChangeName(item);
});


menuParent.get_button("create_folder").addEventListener("click", (e)=>{
    let item = createFolder(None, "");
    WorkChangeName(item);
});

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
            console.log(idFileFolder);
            let text = createFile(idFileFolder[0], idFileFolder[1]);
            items.innerHTML = items.innerHTML + text;
        }
    })
});
