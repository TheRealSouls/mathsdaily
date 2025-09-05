const sidebar = document.getElementById("ham-menu");

const showSideBar = () => {
    sidebar.style.transform = 'translateX(-250px)';
}

const hideSideBar = () => {
    sidebar.style.transform = 'translateX(250px)';
}