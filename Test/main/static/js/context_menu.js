export class ContextWorkerBase {
    #buttons = new Map();
    items = [];
    current_element = null;

    constructor(context_menu, id_for_button) {
        if(!context_menu)
        {
            console.error("Context_menu is None")
        }

        this.id_for_button = id_for_button;
        this.context_menu = context_menu;
        this.#get_buttons();
    }

    #get_buttons()
    {
        if(this.context_menu)
        {
            let _buttons = this.context_menu.querySelectorAll(`#${this.id_for_button}`)
            _buttons.forEach(button => {
                let name = button.getAttribute("name");
                if (name)
                {
                    this.#buttons.set(name, button)
                }
            });
        }
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
        if (!this.context_menu.contains(event.target) && this.items.includes(event.target) || event.button === 0) {
            document.removeEventListener("click", this.close_contextmenu.bind(this));
            this.context_menu.style.display = 'none';
        }
    }

    start(item) {
        this.items.push(item);
        item.addEventListener("contextmenu", (e) => this.view_contextmenu(e));
    }
}

export class MenuItems extends ContextWorkerBase {
    save_action = new Map();

    view_contextmenu(event) {
        this.set_oldAction()
        super.view_contextmenu(event);
        let itemElement = this.current_element.closest('.item');
        let id = itemElement.getAttribute('id_file_folder')
        this.context_menu.querySelectorAll("form").forEach(element => {
            let action = element.getAttribute('action');
            this.save_oldAction(element, action);
            action = action.replace('#id', id);
            element.setAttribute('action', action);
        });
    }

    save_oldAction(element, oldAction)
    { 
        this.save_action.set(element, oldAction);
    }

    set_oldAction()
    {
        this.save_action.forEach((value, key, map)=>{
            key.setAttribute("action", value);
        });

        this.save_action.clear();
    }

    close_contextmenu(event)
    {
        if(super.close_contextmenu(event))
        {
            this.set_oldAction();
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
