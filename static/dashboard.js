function showBorrowScrn(){
    borrowscrn = document.getElementsByClassName('dash-borrow')[0];
    borrowscrn.className = "dash-borrow";
    // getBook();
}

function hideBorrowScrn(){
    borrowscrn = document.getElementsByClassName('dash-borrow')[0];
    borrowscrn.className = borrowscrn.className + " hidden";
}

function showRetDate(){
    retbox = document.getElementById('returnbox');
    retbox.style.display = 'block';
}

function hideRetDate(){
    retbox = document.getElementById('returnbox');
    retbox.style.display = 'none';
}

// function showReturnScrn(){
//     borrowscrn = document.getElementsByClassName('dash-return')[0];
//     borrowscrn.className = "dash-return";
// }

// function hideReturnScrn(){
//     borrowscrn = document.getElementsByClassName('dash-return')[0];
//     borrowscrn.className = borrowscrn.className + " hidden";
// }

// function getBook() {
//     console.log(1);
//     var xhr = new XMLHttpRequest();
//     console.log(2);
//     xhr.open('GET','https://raw.githubusercontent.com/Yogurtchan/Library-Dashboard/eduard-database-functions/static/books.json',true);
//     console.log(3);
//     xhr.onload = function() {
//         console.log(xhr.responseText);
//         if(this.status == 200) {
//             console.log('poop');
//         } else {
//             console.log('bad poop');
//         }
//     }
//     xhr.send();
//     console.log(4);
// }