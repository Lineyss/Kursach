class ContextWorkerBase {
    #buttons = new Map();
    items = [];

    constructor(context_menu) {
        if(!context_menu)
        {
            throw new Error("Context_menu is None")
        }

        this.context_menu = context_menu;
        this.#get_buttons();
        console.log(this.#buttons)
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

        this.context_menu.style.left = event.clientX + "px";
        this.context_menu.style.top = event.clientY + "px";
        this.context_menu.style.display = "block";

        document.addEventListener("click", this.close_contextmenu.bind(this));
    }

    close_contextmenu(event) {
        if (!this.context_menu.contains(event.target) && event.target !== this.item || event.button === 0) {
            this.context_menu.style.display = "none";
            document.removeEventListener("click", this.close_contextmenu.bind(this));
        }
    }

    start(item) {
        this.items.push(item);
        item.addEventListener("contextmenu", (e) => this.view_contextmenu(e));
    }
}

export class MenuItems extends ContextWorkerBase {
    view_contextmenu(event) {
        super.view_contextmenu(event);
        let itemElement = event.target.closest('.item');
        itemElement = itemElement.querySelector(".title-container");
        console.log(itemElement);
        let idElement = itemElement.querySelector("#id");
        console.log(idElement);
        if (idElement) {
            let id = idElement.textContent.trim();

            this.context_menu.querySelectorAll("form").forEach(element => {
                let action = element.getAttribute('action');
                action = action.replace('#id', id);
                element.setAttribute('action', action);
            });
        }
    }
}

export class MenuParentItem extends ContextWorkerBase {
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
}
