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

submitSignup = function () {
    // validation if passwords are matching and of the correct length.
    var pw1 = document.getElementById("password").value;
    var pw2 = document.getElementById("password-2").value;

    if (pw1 == pw2) {
        var form = document.getElementById("signup-form");
        if (form.checkValidity())
            form.submit();
    }
    else {
        event.preventDefault();
        changeText("signup-header", "Passwords do not match")
        changeColor("signup-header", "red")
        document.getElementById("signup").scrollTop = 0;
        window.setTimeout(function () {
            changeText("signup-header", "Signup")
            changeColor("signup-header", "black")
        }, 3000);
    }
}

window.onload = function () {
    //code that is executed as the page is loaded.
    //You shall put your own custom code here.
    var loginscreen = document.getElementById('login-screen');
    loginscreen.innerHTML = document.getElementById('welcomeview').innerHTML;
    //window.alert() is not allowed to be used in your implementation.
};
