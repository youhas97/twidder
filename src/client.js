displayView = function () {
    // the code required to display a view
};


changeText = function (id, text) {
    // text is a string
    document.getElementById(id).innerHTML = text
}

changeColor = function (id, color) {
    // color is a string
    document.getElementById(id).style.color = color
}

checkPasswords = function () {
    var pw1 = document.getElementById("password");
    var pw2 = document.getElementById("password-repeat");

    if (pw1.value != pw2.value) {
        pw2.setCustomValidity("Passwords do not match.");
    }
    else {
        pw2.setCustomValidity("");
    }
}

submitSignup = function () {

}

window.onload = function () {
    //code that is executed as the page is loaded.
    //You shall put your own custom code here.
    var loginscreen = document.getElementById('login-screen');
    loginscreen.innerHTML = document.getElementById('welcomeview').innerHTML;
    //window.alert() is not allowed to be used in your implementation.
};
