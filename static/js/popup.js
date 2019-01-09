jQuery(document).ready(function ($) {

    var modal = $('#modal');
    var modalContainer = $('.main-login');
    var register = $('#signup');
    var login = $('#signin');
    var registerLink = $(".register-link");
    var loginLink = $('.login-link');

// Get the <span> element that closes the modal
    var span = $(".close")[0];

// When the user clicks the button, open the modal
    loginLink.onclick = openModal(login);
    registerLink.onclick = openModal(register);

    function openModal(content) {
        modalContainer.html(content);
        content.addClass('active');
        modal.addClass('active');
    }

    function closeModal() {
        modalContainer.html('');
        modal.removeClass('active');
    }

// When the user clicks on <span> (x), close the modal
    span.onclick = closeModal();

// When the user clicks anywhere outside of the modal, close it
    window.onclick = function (event) {
        if (event.target == modal) {
            closeModal();
        }
    };
});