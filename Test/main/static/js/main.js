import { MenuItems, MenuParentItem } from './context_menu.js';
import { DragAndDrop } from './drag_and_drop.js';
import { sendRequest } from './send_http.js';

const context_menu_parent = document.getElementById("context_menu_item_parent");
const context_menu_item = document.getElementById("context_menu_item");

const formFolder = document.getElementById('form-folder-create');
const formFile = document.getElementById('form-file-create');
const menuParent = new MenuParentItem(context_menu_parent);
const dropZone = document.getElementById('drop-zone');

const formPath = document.getElementById('path-form');
const formPathInput = formPath.querySelector("input");
const fileInput = document.getElementById('id_File');
const item_parent = document.querySelector(".items");
const menuItems = new MenuItems(context_menu_item);
const items = document.querySelectorAll(".item");
const parser = new DOMParser();


const createFile = (IDFileFolder, Title) => {
    const html = `
        <div class="item">
        <div class="image-container">
                <img src="/static/images/file-icon.svg">
                </div>
                <div class="title-container">
                <p style="display: none;" class="id">
                    ${IDFileFolder}
                </p>
                <input class="file-input" readonly type="text" maxlength="150" value="${Title}" />
                </div>
        </div>
    `;
    const DOM = convertInnerHTMLToDOMElement(html);
    setMenuItem(DOM);
    return DOM;
};

const createFolder = (IDFileFolder, Title) => {
    const html = `
        <div class="item">
            <div class="image-container">
                <img src="/static/images/folder-icon.svg">
                </div>
                <div class="title-container">
                <p style="display: none;" class="id">
                ${IDFileFolder}
                </p>
                <input class="file-input" readonly type="text" maxlength="150" value="${Title}" />
                </div>
                </div>
                `;
                const DOM = convertInnerHTMLToDOMElement(html);
                setMenuItem(DOM);
    return DOM;
};

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
    });
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
    
    const EnterDown = (event) => {
        if (event.keyCode === 13) {
            input.blur();
        }
    };

    const Blur = function () {
        input.readOnly = true;
        if (finalFunction) {
            finalFunction(this.value);
        }
        input.removeEventListener("keydown", EnterDown);
        input.removeEventListener("blur", Blur);
    };
    
    input.addEventListener("keydown", EnterDown);
    input.addEventListener("blur", Blur);
};

export const openFileFolder = () => {
    console.log(1);
    const origin = window.location.origin;
    window.location.href = `${origin}/home${formPathInput.value}`;
};


const main = () => {
    menuParent.start(item_parent);

    new DragAndDrop(dropZone, fileInput).start();
    
    items.forEach(item => {

        item.addEventListener("dblclick", function() {
            const input = this.querySelector(".file-input");
            formPathInput.value = formPathInput.value === '/' ? 
                `/${input.value}` : `${formPathInput.value}/${input.value}`;
            openFileFolder();
        });

        item.addEventListener('dragstart', (e) => {
            e.dataTransfer.setData('text/plain', e.target.getAttribute('if_file_folder'));
        });

        // Обработчик события dragover
        item.addEventListener('dragover', (e) => {
            e.preventDefault(); // Разрешаем сброс
        });

        // Обработчик события drop
        item.addEventListener('drop', (e) => {
            e.preventDefault(); // Предотвращаем стандартное поведение
            const draggedItemId = e.dataTransfer.getData('text/plain'); // Получаем ID перетаскиваемого элемента
            
            // console.log(draggedItemId.);

            // Проверяем если элемент, на который сбросили, является папкой (is_file = False)
            if (item.getAttribute('id_file') === 'false') {
                console.log('Перетащенный элемент:', draggedItem);
                console.log('На который элемент:', item);
                // Здесь добавьте ваш код для обработки drop-события, например, измените структуру
            } else {
                console.log('Нельзя сбросить на файл:', item);
            }
        });
    });
    
    if (items.length > 0) {
        setMenuItem(items);
    } else {
        console.log("Нет доступных файлов или папок."); // Сообщение в консоль при отсутствии элементов
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
        });
    });
    
    menuItems.get_button("change").addEventListener("submit", function(e) {
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
            });
        });
    });
    
    menuParent.get_button("create_folder").addEventListener("click", (e) => {
        const item = createFolder(null, "");
        item_parent.appendChild(item);
        WorkChangeName(item, HttpCreateFolder);
    });
    
    fileInput.addEventListener('change', () => {
        const url = formFile.getAttribute('action');
        const method = formFile.getAttribute('method');
    
        sendRequest(url, new FormData(formFile), method, true, function() {
            if (this.status !== 200) {
                alert(this.response);
            } else {
                const idFileFolder = this.response.split(':');
                const file = createFile(idFileFolder[0], idFileFolder[1]);
                item_parent.appendChild(file);
            }
        });
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
