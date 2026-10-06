document.addEventListener("DOMContentLoaded", () => {

    const mobileMenu = document.getElementById("mobileMenu");
    const sidebar = document.getElementById("sidebar");

    if (mobileMenu && sidebar) {

        mobileMenu.addEventListener("click", () => {

            sidebar.classList.toggle("open");

        });

    }

    const currentPath = window.location.pathname;

    document.querySelectorAll(".nav-item").forEach(item => {

        const href = item.getAttribute("href");

        if (!href) {
            return;
        }

        const linkPath =
            new URL(href, window.location.origin).pathname;

        if (currentPath === linkPath) {

            item.classList.add("active");

        }

    });

    document.querySelectorAll(".nav-item").forEach(item => {

        item.addEventListener("click", () => {

            if (sidebar) {
                sidebar.classList.remove("open");
            }

        });

    });

});