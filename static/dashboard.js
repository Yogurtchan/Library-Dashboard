function showBorrowScrn(){
    borrowscrn = document.getElementsByClassName('dash-borrow')[0];
    borrowscrn.className = "dash-borrow";
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