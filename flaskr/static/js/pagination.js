class Pagination {

    currentPage = 0;

    constructor(arrayLength, maxItemsPerPage, idPrefix) {
        let c = Math.ceil(arrayLength/maxItemsPerPage)
        this.pageCount = c > 0 ? c : 1;
        this.itemCount = arrayLength;
        this.idPrefix = idPrefix;
        this.itemsPerPage = maxItemsPerPage;
        this.renderPage();
        this.createButtons();
    }

    renderPage() {
        this.hideAll();
        for (let i=0; i<this.itemsPerPage; i++) {
            let currentItem = this.currentPage * this.itemsPerPage + i;
            let element = document.getElementById(`${this.idPrefix}${currentItem}`);
            if (element) {
                element.style.display = "";
            };
        };
    };

    hideAll() {
        for (let i=0; i<this.itemCount; i++) {
            let element = document.getElementById(`${this.idPrefix}${i}`);
            element.style.display = "none";
        };
    };

    nextPage() {
        if (this.currentPage < this.pageCount-1) {
            this.currentPage += 1;
        };
        this.renderPage();
        this.updatePageCounter();
    };

    previousPage() {
        if (this.currentPage >= 1) {
            this.currentPage -= 1;
        };
        this.renderPage();
        this.updatePageCounter();
    };

    updatePageCounter() {
        let element = document.getElementById(`${this.idPrefix}PageCountContainer`);
        element.innerHTML = `<p class="pl-2 pr-2">${this.currentPage+1}/${this.pageCount}</p>`;
    };

    createButtons() {
        let element = document.getElementById(`${this.idPrefix}Control`)
        element.innerHTML = `
        <button class="btn btn-light btn-sm" id="${this.idPrefix}Prev">Prev</button>
        <div id="${this.idPrefix}PageCountContainer">
        <p class="pl-2 pr-2">${this.currentPage+1}/${this.pageCount}</p>
        </div>
        <button class="btn btn-light btn-sm" id="${this.idPrefix}Next">Next</button>
        `;
        document.getElementById(`${this.idPrefix}Prev`).addEventListener('click', ()=>{this.previousPage()});
	    document.getElementById(`${this.idPrefix}Next`).addEventListener('click', ()=>{this.nextPage()});

    };

};