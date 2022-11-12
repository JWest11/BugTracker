class Search {

    currentString = ""

    constructor(arrayLength, prefix) {
        this.arrayLength = arrayLength
        this.prefix = prefix
        this.createControler()
    }

    renderItems() {
        for (let i=0; i<this.arrayLength; i++) {
            let element = document.getElementById(`${this.prefix}${i}`);
            if (element.innerText.includes(this.currentString)) {
                element.style.display = "";
            } else {
                element.style.display = "none";
            }
        };
    };

    createControler() {
        let element = document.getElementById(`${this.prefix}Control`)
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
            this.currentString = e.target.value
            this.renderItems()
        })
    };
}