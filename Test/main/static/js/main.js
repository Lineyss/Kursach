import { MenuItems, MenuParentItem } from './context_menu.js';
import { DragAndDrop } from './drag_and_drop.js';
import { sendRequest } from './send_http.js';

const context_menu_parent = document.getElementById("context_menu_item_parent");
const formMoveFileFolder = document.getElementById('form-move-file-folder');
const context_menu_item = document.getElementById("context_menu_item");
const formFolder = document.getElementById('form-folder-create');
const formFile = document.getElementById('form-file-create');
const menuParent = new MenuParentItem(context_menu_parent, 'context_menu_button_parents');
const dropZone = document.getElementById('drop-zone');
const formPath = document.getElementById('path-form');
const formPathInput = formPath.querySelector("input");
const fileInput = document.getElementById('id_File');
const item_parent = document.querySelector(".items");
const menuItems = new MenuItems(context_menu_item, 'context_menu_button_item');
const items = document.querySelectorAll(".item");
const load = document.querySelector(".loader");
const parser = new DOMParser();
const formAddTegFile = document.getElementById('add-teg-file-folder');

let teg_id = null;
let selected_teg = null;
let file_folder_id = null;

const csrf_token = document.querySelector('input[name="csrfmiddlewaretoken"]').value;


const createFile = (IDFileFolder, Title) => {
    const html = `
        <div class="item">
            <form id="add-teg" class="teg-container" action="/teg/add/${IDFileFolder}" method="POST">
                <input type="hidden" name="csrfmiddlewaretoken" value="${csrf_token}"/>
                <button type="submit" class="button add-teg">
                    +
                </button>
            </form>
            <div id_file="True" class="image-container" id_file_folder="${IDFileFolder}" draggable="True">
                <img draggable="False" src="/static/images/file-icon.svg">
            </div>
            <div class="title-container">
                <input class="file-input" readonly type="text" maxlength="150" value="${Title}" />
            </div>
        </div>
    `;
    const DOM = convertInnerHTMLToDOMElement(html);
    setMenuItem(DOM);
    baseEvent(DOM);
    return DOM;
};


const createFolder = (IDFileFolder, Title) => {
    const html = `
        <div class="item">
            <form id="add-teg" class="teg-container" action="/teg/add/${IDFileFolder}" method="POST">
                <input type="hidden" name="csrfmiddlewaretoken" value="${csrf_token}"/>
                <button type="submit" class="button add-teg">
                    +
                </button>
            </form>
            <div id_file="False" class="image-container" id_file_folder="${IDFileFolder}" draggable="True">
                <img draggable="False" src="/static/images/folder-icon.svg">
            </div>
            <div class="title-container">
                <input class="file-input" readonly type="text" maxlength="150" value="${Title}" />
            </div>
        </div>
        `;
    const DOM = convertInnerHTMLToDOMElement(html);
    setMenuItem(DOM);
    baseEvent(DOM);
    return DOM;
};

const baseEvent = (item) => {
    item.addEventListener("dblclick", function() {
        const input = this.querySelector(".file-input");
        formPathInput.value = formPathInput.value === '/' ? 
            `/${input.value}` : `${formPathInput.value}/${input.value}`;
        openFileFolder();
    });

    item.addEventListener('dragstart', (e) => {
        e.dataTransfer.setData('text/plain', e.target.getAttribute('id_file_folder'));
    });

    item.addEventListener('dragover', (e) => {
        e.preventDefault();
    });

    item.addEventListener('drop', (e) => {
        e.preventDefault();
        const draggedItemId = e.dataTransfer.getData('text/plain');
        let draggedItem = document.querySelector(`.item[id_file_folder="${draggedItemId}"]`)
        let is_file = item.getAttribute('is_file');

        console.log(item);
        console.log(draggedItem)
        

        if (is_file === 'False') {
            let action = `${formMoveFileFolder.getAttribute('action')}/${draggedItem.getAttribute('id_file_folder')}/${item.getAttribute('id_file_folder')}`;

            sendRequest(action, new FormData(formMoveFileFolder), formMoveFileFolder.getAttribute('method'), false, function (){
                if(this.status==200)
                {
                    draggedItem.remove();
                }
                else
                {
                    alert('Не удалось переместить элемент')
                }
            }, startLoad, endLoad);
        }
    });
}

const setMenuItem = (items) => {
    if (items) {
        if (Array.isArray(items) || items instanceof NodeList) {
            items.forEach(element => {
                menuItems.start(element);
            });
        } else {
            menuItems.start(items);
        }
    }
};

const HttpCreateFolder = (Title) => {
    const url = formFolder.getAttribute("action");
    const method = formFolder.getAttribute("method");
    const input = formFolder.querySelector("#id_Title");
    input.value = Title;
    
    sendRequest(url, new FormData(formFolder), method, false, function() {
        if (this.status !== 200) {
            alert(this.response);
        } else {
            const idFileFolder = this.response.split(':');
            const folder = createFolder(idFileFolder[0], idFileFolder[1]);
            item_parent.removeChild(item_parent.lastChild)
            item_parent.appendChild(folder);
        }
    },
    startLoad, endLoad);
};

const convertInnerHTMLToDOMElement = (innerHtml) => {
    const doc = parser.parseFromString(innerHtml, 'text/html');
    return doc.body.firstChild;
};

const WorkChangeName = (item, finalFunction) => {
    const input = item.querySelector(".file-input");
    input.readOnly = false;
    input.select();
    input.focus();
    
    input.addEventListener("keydown", (e) => {
        if(e.key === 'Enter'){
            input.blur();
        }
    });
    
    input.addEventListener("blur", function() {
        input.readOnly = true;
        if (finalFunction) {
            finalFunction(this.value);
        }
    });
};

const startLoad = () => {
    load.style.display = 'block !important';
};

const endLoad = () => {
    load.style.display = 'none !important';
};


export const openFileFolder = () => {
    const origin = window.location.origin;
    window.location.href = `${origin}/home${formPathInput.value}`;
};


const main = () => {
    menuParent.start(item_parent);

    new DragAndDrop(dropZone, fileInput).start();

    document.querySelectorAll(".add-teg").forEach(element => {
        element.addEventListener("click", function(){
            file_folder_id = this.closest(".item").getAttribute('id_file_folder');
            if(teg_id)
            {
                let action = `${formAddTegFile.getAttribute('action')}/${teg_id}/${file_folder_id}`;
                let method = formAddTegFile.getAttribute('method');

                sendRequest(action, new FormData(formAddTegFile), method, false, function() {
                    if (this.status == 200)
                    {
                        location.reload();
                    }
                    else
                    {
                        alert('Не удалось установить тег =(');
                    }
                });
            }
        });
    });

    document.querySelectorAll(".tag-card").forEach(element => {
        element.addEventListener("click", function () {
            teg_id = this.getAttribute('id');

            if (selected_teg)
            {
                selected_teg.classList.remove('select-teg');
            }

            this.classList.add('select-teg');
            selected_teg = this;
        });
    });

    items.forEach(item => {
        baseEvent(item);
    });
    
    if (items.length > 0) {
        setMenuItem(items);
    } else {
        console.log("Нет доступных файлов или папок.");
    }
    
    menuItems.get_button("delete").addEventListener("submit", function (e) {
        e.preventDefault();
    
        const item = menuItems.current_element.closest(".item");
        const action = this.getAttribute("action");
        const method = this.getAttribute("method");
    
        const form = new FormData(this);
    
        sendRequest(action, form, method, false, function() {
            if (this.status === 200) {
                item.remove();
            } else {
                alert("Не удалось удалить. Попробуйте позже =(");
            }
        }, startLoad, endLoad);
    });
    
    menuItems.get_button("change").addEventListener("submit", function(e) {
        try
        {
            e.preventDefault();
            const form = this;
            const item = menuItems.current_element.closest(".item");
            WorkChangeName(item, function(title) {
                const url = `${form.getAttribute("action")}/${title}`;
        
                sendRequest(url, new FormData(form), form.getAttribute("method"), false, function() {
                    if (this.status === 200) {
                        const input = item.querySelector(".file-input");
                        const idFileFolder = this.response.split(':');
                        input.value = idFileFolder[1];
                    } else {
                        alert("Не удалось изменить название, попробуйте позже =(");
                    }
                }, startLoad, endLoad);
            });
        }
        catch
        {

        }
    });
    
    menuParent.get_button("create_folder").addEventListener("click", (e) => {
        const item = createFolder(null, "");
        item_parent.appendChild(item);
        WorkChangeName(item, HttpCreateFolder);
    });
    
    fileInput.addEventListener('change', () => {
        const url = formFile.getAttribute('action');
        const method = formFile.getAttribute('method');
    
        sendRequest(url, new FormData(formFile), method, false, function() {
            if (this.status !== 200) {
                alert(this.response);
            } else {
                const idFileFolder = this.response.split(':');
                const file = createFile(idFileFolder[0], idFileFolder[1]);
                item_parent.appendChild(file);
            }
        }, startLoad, endLoad);
    });
}

try
{
    main();
}
catch(Error)
{
    console.error(Error)
}
