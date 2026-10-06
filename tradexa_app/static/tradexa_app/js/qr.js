document.addEventListener("DOMContentLoaded", () => {


const printButton = document.getElementById("printPackages");

if (printButton) {

    printButton.addEventListener("click", () => {
        window.print();
    });

}


});
