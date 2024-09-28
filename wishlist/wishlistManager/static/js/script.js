function adjustTopbarLayout() {
    var screenWidth = window.innerWidth;
    var topbarLeft = document.getElementById('topbar-left');
    var topbarCenter = document.getElementById('topbar-center');
    var topbarRight = document.getElementById('topbar-right');
    var topbarDropdown = document.getElementById('topbar-dropdown');

    if (screenWidth < 700) { 
        topbarLeft.style.display = 'none';
        topbarCenter.style.display = 'none';
        topbarRight.style.display = 'none';
        topbarDropdown.style.display = 'block';
    } else {
        topbarLeft.style.display = 'block';
        topbarCenter.style.display = 'flex';
        topbarRight.style.display = 'flex';
        topbarDropdown.style.display = 'none';
    }
}

window.onload = adjustTopbarLayout;

window.onresize = adjustTopbarLayout;

