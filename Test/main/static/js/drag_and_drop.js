export class DragAndDrop
{
    constructor(dropZone, fileInput)
    {
        this.dropZone = dropZone;
        this.fileInput = fileInput;
    }

    dragover(event)
    {
        event.preventDefault();
        this.dropZone.classList.add("highlight");
    }

    dragleave(event)
    {
        event.preventDefault();
        this.dropZone.classList.remove("highlight");
    }

    drop(event)
    {
        event.preventDefault();
        this.dropZone.classList.remove('highlight');
        let files = event.dataTransfer.files;
        if (files)
        {
            for(let i = 0; i < files.length; i ++){
            let dataTransfer = new DataTransfer()
            dataTransfer.items.add(files.item(i));
                this.fileInput.files = dataTransfer.files;
                const event = new Event('change');
                this.fileInput.dispatchEvent(event);
            }
        }
    }

    start()
    {
        this.dropZone.addEventListener("drop", (e) => this.drop(e));
        this.dropZone.addEventListener("dragover", (e) => this.dragover(e));
        this.dropZone.addEventListener("dragleave", (e) => this.dragover(e));
    }
}