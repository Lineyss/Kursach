class ContextWorkerBase {
    #buttons = new Map();
    items = [];
    clone_context_menu = null;

    constructor(context_menu) {
        if(!context_menu)
        {
            throw new Error("Context_menu is None")
        }

        this.context_menu = context_menu;
        this.#get_buttons();
    }

    #get_buttons()
    {
        let _buttons = this.context_menu.querySelectorAll("#context_menu_button")
        _buttons.forEach(button => {
            let name = button.getAttribute("name");
            if (name)
            {
                this.#buttons.set(name, button)
            }
        });
    }

    get_button(Name)
    {
        return this.#buttons.get(Name);
    }

    view_contextmenu(event) {
        event.preventDefault();
        
        this.current_element = event.target;

        this.copy_context_menu = this.context_menu.cloneNode(true);

        this.copy_context_menu.style.left = event.clientX + "px";
        this.copy_context_menu.style.top = event.clientY + "px";
        this.copy_context_menu.style.display = "block";
        document.body.appendChild(this.copy_context_menu);

        document.addEventListener("click", this.close_contextmenu.bind(this));
    }

    close_contextmenu(event) {
        if (!this.context_menu.contains(event.target) && event.target !== this.item || event.button === 0) {
            this.copy_context_menu.remove();
            document.removeEventListener("click", this.close_contextmenu.bind(this));
        }
    }

    // Сюда добавлять события для кнопок
    set_button_event()
    {

    }

    start(item) {
        this.items.push(item);
        item.addEventListener("contextmenu", (e) => this.view_contextmenu(e));
        this.set_button_event();
    }
}

export class MenuItems extends ContextWorkerBase {
    view_contextmenu(event) {
        super.view_contextmenu(event);
        let itemElement = event.target.closest('.item');
        itemElement = itemElement.querySelector(".title-container");
        
        let idElement = itemElement.querySelector("#id");

        if (idElement) {
            let id = idElement.textContent.trim();
            this.copy_context_menu.querySelectorAll("form").forEach(element => {
                let action = element.getAttribute('action');
                action = action.replace('#id', id);
                element.setAttribute('action', action);
            });
        }
    }

    set_button_event()
    {

    }
}

export class MenuParentItem extends ContextWorkerBase {
    parser = new DOMParser();
    view_contextmenu(event) {
        for(let i = 0; i < this.items.length; i++)
        {
            if(event.target === this.items[i])
            {
                super.view_contextmenu(event);
                break;
            }
        }
    }

    set_button_event()
    {
        get_button("create_folder").addEventListener("click", (e)=>{
            let folder = createFolder(1, "asd");
            folder = this.parser.parseFromString(folder, "text/html").body.firstElementChild
            items.appendChild(folder); 
        });
    }
}
