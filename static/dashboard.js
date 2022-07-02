function showBorrowScrn(){
    borrowscrn = document.getElementsByClassName('dash-borrow')[0];
    borrowscrn.className = "dash-borrow";
    getBook();
}

function hideBorrowScrn(){
    borrowscrn = document.getElementsByClassName('dash-borrow')[0];
    borrowscrn.className = borrowscrn.className + " hidden";
}

function showReturnScrn(){
    borrowscrn = document.getElementsByClassName('dash-return')[0];
    borrowscrn.className = "dash-return";
}

function hideReturnScrn(){
    borrowscrn = document.getElementsByClassName('dash-return')[0];
    borrowscrn.className = borrowscrn.className + " hidden";
}

function getBook() {
    var xhr = new XMLHttpRequest();
    xhr.open('GET','books.json',true);
    xhr.onload = () => {
        console.log(this.status);
        if(this.status == 200) {
            console.log('poop');
        } else {
            console.log('bad poop');
        }
    }
}