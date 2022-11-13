class SearchPagination {

    searchString = "";
    pageCount = 0;
    currentItemIndexes = [];
    currentPage = 0;


    constructor (itemCount, itemsPerPage, prefix) {
        this.itemsPerPage = itemsPerPage;
        this.itemCount = itemCount;
        this.prefix = prefix;
        this.createControllers();
        this.setSearchString("");
    };

    render() {
        this.hideAll();
        const N = this.currentItemIndexes.length;
        for (let i=0; i<this.itemsPerPage; i++) {
            let i2 = this.currentPage * this.itemsPerPage + i;
            if (i2 >= N) {break;};
            let elementIndex = this.currentItemIndexes[i2];
            let element = document.getElementById(`${this.prefix}${elementIndex}`);
            element.style.display = "";
        };
        this.renderPageNumbers();

    };

    hideAll() {
        for (let i=0; i<this.itemCount; i++) {
            let element = document.getElementById(`${this.prefix}${i}`);
            element.style.display = "none";
        };
    };

    setSearchString(newSearchString) {
        this.searchString = newSearchString;
        this.setCurrentItemIndexes();
        this.setPageCount();
        this.render();
    };

    setCurrentItemIndexes() {
        this.currentItemIndexes = [];
        for (let i=0; i<this.itemCount; i++) {
            let element = document.getElementById(`${this.prefix}${i}`);
            if (element.innerText.includes(this.searchString)) {
                this.currentItemIndexes.push(i);
            };
        };
    };

    setPageCount() {
        let c = this.currentItemIndexes.length;
        this.pageCount = Math.floor(c/this.itemsPerPage);
        this.currentPage = 0;
    };

    nextPage() {
        if (this.currentPage !== this.pageCount) {
            this.currentPage += 1;
            this.render();
        };
    };

    previousPage() {
        if (this.currentPage !== 0) {
            this.currentPage -= 1;
            this.render();
        };
    };

    renderPageNumbers() {
        let element = document.getElementById(`${this.prefix}PageCountContainer`)
        element.innerText = `${this.currentPage+1}/${this.pageCount+1}`
    };

    createControllers() {
        let element = document.getElementById(`${this.prefix}SearchControl`)
        element.innerHTML = `
			<div class="input-group borderDark">
		        <div class="input-group-prepend">
		            <span class="input-group-text">
						<i class="mdi mdi-magnify"></i>
					</span>
				</div>
				<input id="${this.prefix}SearchInput" type="text" placeholder="Search" class="form-control">
		    </div>
        `;

        document.getElementById(`${this.prefix}SearchInput`).addEventListener('change', (e) => {
            this.setSearchString(e.target.value);
        });

        element = document.getElementById(`${this.prefix}PageControl`)
        element.innerHTML = `
            <button class="btn btn-light btn-sm" id="${this.prefix}PreviousPage">Prev</button>
                <div>
                    <p id="${this.prefix}PageCountContainer" class="pl-2 pr-2">${this.currentPage+1}/${this.pageCount+1}</p>
                </div>
            <button class="btn btn-light btn-sm" id="${this.prefix}NextPage">Next</button>
        `;
        document.getElementById(`${this.prefix}PreviousPage`).addEventListener('click', ()=>{this.previousPage()});
	    document.getElementById(`${this.prefix}NextPage`).addEventListener('click', ()=>{this.nextPage()});
    };


    
};