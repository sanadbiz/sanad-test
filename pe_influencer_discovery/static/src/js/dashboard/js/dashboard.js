document.addEventListener('DOMContentLoaded', function() {
    const sidebar = document.getElementById("sidebar");
    const mainContent = document.getElementById("main-content");
    const secondarySidebar = document.getElementById("secondary-sidebar");
    const pinButton = document.getElementById("pinButton");
    const navItems = document.querySelectorAll('.left-nav-arrow');
    const closeIcon = document.getElementById('close-icon');
    const navLinks = document.querySelectorAll(".custom-glow");
    let isPinned = false;
    let activeNavItem = null;
    let isHoveringSecondary = false;

    closeIcon?.addEventListener('click', () => {
            hideSecondarySidebar();
            isHoveringSecondary = false;
            activeNavItem = null;
    });

    const activeLink = localStorage.getItem("activeNavLink");
    if (activeLink) {
        const activeElement = document.querySelector(`a[href="${activeLink}"]`);
        if (activeElement) {
            const img = activeElement.querySelector("img");
            if (img) {
                img.classList.add("glow");
            }
        }
    }

    navLinks.forEach((navLink) => {
        navLink.addEventListener("click", function () {
            navLinks.forEach((link) => {
                const img = link.querySelector("img");
                if (img) {
                    img.classList.remove("glow");
                }
            });

            const img = this.querySelector("img");
            if (img) {
                img.classList.add("glow");
            }

            localStorage.setItem("activeNavLink", this.getAttribute("href"));
        });
    });

    if (pinButton) {
        pinButton.style.display = "flex";
    }

    pinButton?.addEventListener("click", () => {
        isPinned = !isPinned;
        pinButton.classList.toggle("pinned");
        toggleSidebar(isPinned);
    });

    navItems.forEach(item => {
        item.addEventListener('click', (e) => {
            e.preventDefault();

            navItems.forEach(navItem => navItem.classList.remove('active'));
            item.classList.add('active');

            if (activeNavItem === item) {
                hideSecondarySidebar();
                activeNavItem = null;
            } else {
                showSecondarySidebar();
                activeNavItem = item;
            }
        });
    });

    sidebar?.addEventListener("mouseenter", () => {
        if (!isPinned) {
            expandSidebar();
            if (isHoveringSecondary) {
                hideSecondarySidebar();
                isHoveringSecondary = false;
                activeNavItem = null;
            }
        }
    });

    sidebar?.addEventListener("mouseleave", () => {
        if (!isPinned && !isHoveringSecondary) {
            collapseSidebar();
        }
    });

    secondarySidebar?.addEventListener("mouseenter", () => {
            expandSidebar();
            showSecondarySidebar();
            isHoveringSecondary = true;
    });

    secondarySidebar?.addEventListener("mouseleave", () => {
            hideSecondarySidebar();
            isHoveringSecondary = false;
            activeNavItem = null;
    });

    function expandSidebar() {
        sidebar.style.width = "250px";
        mainContent.style.marginRight = "250px";
        navItems.forEach(item => {
            item.style.display = "block";
        });
        mainContent.classList.remove('collapsed');
        if (pinButton) {
            pinButton.style.display = "flex";
        }
    }

    function collapseSidebar() {
        sidebar.style.width = "60px";
        mainContent.style.marginRight = "60px";
        navItems.forEach(item => {
            item.style.display = "none";
        });
        mainContent.classList.add('collapsed');
        if (pinButton && !isPinned) {
            pinButton.style.display = "none";
        }
    }

    function showSecondarySidebar() {
    if (secondarySidebar){
     secondarySidebar.style.width = "252px";
        secondarySidebar.style.right = "250px";
        secondarySidebar.classList.add('active');
        mainContent.style.marginRight = "502px";
    }

    }

    function hideSecondarySidebar() {

    if (secondarySidebar){

        secondarySidebar.style.width = "0";
        secondarySidebar.classList.remove('active');
    }
        mainContent.style.marginRight = sidebar.style.width;
    }

    function toggleSidebar(isPinned) {
        if (isPinned) {
            expandSidebar();
        } else {
            collapseSidebar();
        }
    }

    if (!isPinned) {
        collapseSidebar();
    }
});
